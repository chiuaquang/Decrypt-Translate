#!/usr/bin/env python3
"""
dat_tool.py — Tool dịch ngược file .dat (XOR 0xFF + JSON)
Chạy: python3 dat_tool.py
"""

import sys, os, json, copy, time

# ══════════════════════════════════════════════════════════════
#  XOR codec
# ══════════════════════════════════════════════════════════════

def xor_ff(data: bytes) -> bytes:
    return bytes(b ^ 0xFF for b in data)

def decode_dat(path: str) -> dict:
    with open(path, 'rb') as f:
        raw = f.read()
    return json.loads(xor_ff(raw).decode('utf-8'))

def encode_dat(obj: dict, path: str):
    text = json.dumps(obj, ensure_ascii=False, indent=2)
    raw = xor_ff(text.encode('utf-8'))
    with open(path, 'wb') as f:
        f.write(raw)

# ══════════════════════════════════════════════════════════════
#  Helpers
# ══════════════════════════════════════════════════════════════

CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
DIM    = "\033[2m"

def p(msg, color=''): print(f"{color}{msg}{RESET}")
def ok(msg):    p(f"  ✓ {msg}", GREEN)
def warn(msg):  p(f"  ⚠ {msg}", YELLOW)
def err(msg):   p(f"  ✗ {msg}", RED)
def info(msg):  p(f"  {msg}", CYAN)
def hr():       p("─" * 52, DIM)

def ask(prompt, default=''):
    try:
        val = input(f"{CYAN}{prompt}{RESET}").strip()
        return val if val else default
    except (KeyboardInterrupt, EOFError):
        print(); p("\nĐã hủy.", YELLOW); sys.exit(0)

def confirm(msg):
    r = ask(f"{msg} [y/N]: ").lower()
    return r in ('y', 'yes', 'có', 'co')

def find_dats(folder: str) -> list[str]:
    """Tìm tất cả .dat trong folder (không đệ quy)."""
    try:
        files = [f for f in os.listdir(folder) if f.lower().endswith('.dat')]
        return sorted([os.path.join(folder, f) for f in files])
    except Exception as e:
        return []

def write_list_txt(out_folder: str, entries: list[dict]):
    """
    list.txt format:
      <tên file .dat>|<đường dẫn .dat gốc>|<tên file .json>
    """
    path = os.path.join(out_folder, 'list.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# dat_tool list — KHÔNG xóa/sửa file này\n")
        f.write("# dat_name|dat_original_path|json_name\n")
        for e in entries:
            f.write(f"{e['dat_name']}|{e['dat_path']}|{e['json_name']}\n")
    return path

def read_list_txt(folder: str) -> list[dict]:
    path = os.path.join(folder, 'list.txt')
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy list.txt trong: {folder}")
    entries = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            parts = line.split('|')
            if len(parts) == 3:
                entries.append({
                    'dat_name':  parts[0],
                    'dat_path':  parts[1],
                    'json_name': parts[2],
                })
    return entries

# ══════════════════════════════════════════════════════════════
#  Core operations
# ══════════════════════════════════════════════════════════════

def process_decode(dat_paths: list[str], out_folder: str):
    """Decode danh sách .dat → JSON vào out_folder, tạo list.txt."""
    os.makedirs(out_folder, exist_ok=True)
    entries = []
    total = len(dat_paths)

    p(f"\nDecode {total} file → {out_folder}", BOLD)
    hr()

    ok_count = 0
    for i, dat_path in enumerate(dat_paths, 1):
        dat_name  = os.path.basename(dat_path)
        stem      = os.path.splitext(dat_name)[0]
        json_name = f"{stem}.json"
        json_path = os.path.join(out_folder, json_name)

        sys.stdout.write(f"  [{i}/{total}] {dat_name} ... ")
        sys.stdout.flush()

        try:
            obj = decode_dat(dat_path)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=2)

            # Đếm chuỗi JP
            count = count_jp_strings(obj)
            print(f"{GREEN}OK{RESET} ({count:,} chuỗi JP)")
            entries.append({
                'dat_name':  dat_name,
                'dat_path':  dat_path,
                'json_name': json_name,
            })
            ok_count += 1
        except Exception as e:
            print(f"{RED}LỖI: {e}{RESET}")

    list_path = write_list_txt(out_folder, entries)
    hr()
    ok(f"Hoàn thành {ok_count}/{total} file")
    ok(f"list.txt → {list_path}")
    info(f"Mở các file .json trong: {out_folder}")
    info("Dịch xong → chọn Option 3 để encode lại")


def process_encode(json_folder: str):
    """Đọc list.txt → encode từng JSON → ghi lại .dat gốc."""
    try:
        entries = read_list_txt(json_folder)
    except FileNotFoundError as e:
        err(str(e)); return

    if not entries:
        warn("list.txt trống."); return

    total = len(entries)
    p(f"\nEncode {total} file → ghi lại .dat gốc", BOLD)
    hr()

    ok_count = 0
    for i, e in enumerate(entries, 1):
        json_path = os.path.join(json_folder, e['json_name'])
        dat_path  = e['dat_path']
        dat_name  = e['dat_name']

        sys.stdout.write(f"  [{i}/{total}] {e['json_name']} → {dat_name} ... ")
        sys.stdout.flush()

        if not os.path.exists(json_path):
            print(f"{RED}LỖI: không tìm thấy {json_path}{RESET}")
            continue

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                obj = json.load(f)

            # Backup .dat gốc lần đầu
            bak = dat_path + '.bak'
            if not os.path.exists(bak):
                import shutil
                shutil.copy2(dat_path, bak)

            encode_dat(obj, dat_path)
            size = os.path.getsize(dat_path)
            print(f"{GREEN}OK{RESET} ({size/1024:.0f} KB)")
            ok_count += 1
        except Exception as e_:
            print(f"{RED}LỖI: {e_}{RESET}")

    hr()
    ok(f"Hoàn thành {ok_count}/{total} file")
    if ok_count > 0:
        info("File .dat gốc đã được backup thành .dat.bak")


def count_jp_strings(obj) -> int:
    count = [0]
    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, str) and v and any('\u3040' <= c <= '\u9fff' or '\u4e00' <= c <= '\u9fff' for c in v):
                    count[0] += 1
                else:
                    walk(v)
        elif isinstance(node, list):
            for i in node: walk(i)
    walk(obj)
    return count[0]

# ══════════════════════════════════════════════════════════════
#  Menu
# ══════════════════════════════════════════════════════════════

def banner():
    print()
    p("╔══════════════════════════════════════════════╗", CYAN)
    p("║      DAT TOOL — Dịch game .dat (XOR/JSON)   ║", CYAN)
    p("╠══════════════════════════════════════════════╣", CYAN)
    p("║  1. Decode 1 file .dat  → JSON               ║", CYAN)
    p("║  2. Decode cả thư mục   → JSON               ║", CYAN)
    p("║  3. Encode JSON đã dịch → .dat gốc           ║", CYAN)
    p("║  0. Thoát                                    ║", CYAN)
    p("╚══════════════════════════════════════════════╝", CYAN)
    print()

def option1():
    hr()
    p("OPTION 1 — Decode 1 file .dat", BOLD)
    hr()
    info("Ví dụ: /storage/emulated/0/Download/GameData/data_scenario.dat")
    dat_path = ask("Nhập đường dẫn file .dat: ")

    if not dat_path:
        warn("Chưa nhập đường dẫn."); return
    if not os.path.isfile(dat_path):
        err(f"Không tìm thấy file: {dat_path}"); return
    if not dat_path.lower().endswith('.dat'):
        warn("File không phải .dat, vẫn thử decode...")

    # Thư mục output
    default_out = os.path.join(os.path.dirname(dat_path), 'dat_decoded')
    out_folder  = ask(f"Thư mục lưu JSON [{default_out}]: ", default_out)

    process_decode([dat_path], out_folder)


def option2():
    hr()
    p("OPTION 2 — Decode tất cả .dat trong thư mục", BOLD)
    hr()
    info("Ví dụ: /storage/emulated/0/Download/GameData/File")
    folder = ask("Nhập đường dẫn thư mục chứa .dat: ")

    if not folder:
        warn("Chưa nhập đường dẫn."); return
    if not os.path.isdir(folder):
        err(f"Không tìm thấy thư mục: {folder}"); return

    dat_paths = find_dats(folder)
    if not dat_paths:
        warn(f"Không tìm thấy file .dat nào trong: {folder}"); return

    p(f"\nTìm thấy {len(dat_paths)} file .dat:", GREEN)
    for p_ in dat_paths:
        info(f"  {os.path.basename(p_)}")

    if not confirm(f"\nDecode {len(dat_paths)} file?"):
        warn("Đã hủy."); return

    default_out = os.path.join(folder, 'dat_decoded')
    out_folder  = ask(f"Thư mục lưu JSON [{default_out}]: ", default_out)

    process_decode(dat_paths, out_folder)


def option3():
    hr()
    p("OPTION 3 — Encode JSON đã dịch → trả lại .dat gốc", BOLD)
    hr()
    info("Nhập thư mục chứa file JSON đã dịch + list.txt")
    info("Ví dụ: /storage/emulated/0/Download/GameData/File/dat_decoded")
    json_folder = ask("Nhập đường dẫn thư mục JSON: ")

    if not json_folder:
        warn("Chưa nhập đường dẫn."); return
    if not os.path.isdir(json_folder):
        err(f"Không tìm thấy thư mục: {json_folder}"); return

    # Đọc list.txt để preview
    try:
        entries = read_list_txt(json_folder)
    except FileNotFoundError as e:
        err(str(e))
        info("Hãy chạy Option 1 hoặc 2 trước để tạo list.txt")
        return

    if not entries:
        warn("list.txt trống."); return

    p(f"\nTìm thấy {len(entries)} file trong list.txt:", GREEN)
    for e in entries[:5]:
        info(f"  {e['json_name']} → {e['dat_path']}")
    if len(entries) > 5:
        info(f"  ... và {len(entries)-5} file khác")

    warn("\n  File .dat gốc sẽ bị GHI ĐÈ (có backup .dat.bak tự động)")
    if not confirm("Tiếp tục encode?"):
        warn("Đã hủy."); return

    process_encode(json_folder)


def main():
    banner()
    while True:
        choice = ask("Chọn [0-3]: ")
        if   choice == '1': option1()
        elif choice == '2': option2()
        elif choice == '3': option3()
        elif choice == '0':
            p("\nTạm biệt!", CYAN); break
        else:
            warn("Chọn 0, 1, 2 hoặc 3.")
        print()
        banner()

if __name__ == '__main__':
    main()
