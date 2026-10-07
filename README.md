<div align="center">

# 🎮 Unity DAT Tool

### Công cụ Việt hóa game Unity — chạy trực tiếp trên **Termux / Android**

*Trích xuất văn bản → dịch → đóng gói lại → sửa font — tất cả trong một file Python duy nhất, không cần PC.*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Android%20%7C%20Linux-green?logo=android&logoColor=white)](https://termux.dev/)
[![Deps](https://img.shields.io/badge/Dependencies-Chuẩn%20thư%20viện-orange)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

</div>

---

## ✨ Tính năng

| # | Chức năng | Mô tả |
|---|-----------|-------|
| 1–3 | 📦 **File .dat** | Decode `.dat` (XOR/JSON) → JSON, encode ngược lại |
| 4–5 | 📦 **File PFS** | Giải nén / đóng gói lại `.pfs` (Artemis pf6/pf8) |
| 6 | 🔍 **Trích văn bản Unity** | Deep extract từ `data.unity3d` → JSON (chỉ trường `text`) |
| 7 | 📥 **Đóng gói lại Unity** | Vá JSON đã dịch vào bundle gốc (giữ nguyên cấu trúc, có `.bak`) |
| 8 | 🔤 **NFD test** | Chuyển JSON sang Unicode decomposed để test font |
| 9 | 🎨 **Thay font game** | Kiểu anylang: bỏ font TTF/OTF vào thư mục, tool tự đè vào mọi font gốc |
| 10 | 💬 **Sửa font TMP** | Bật Dynamic cho TextMeshPro → hết lỗi **□** ở chữ hội thoại |

> **100% thư viện chuẩn Python** — không cần `pip install` gì cả. Copy 1 file `.py` vào điện thoại là chạy.

---

## 🚀 Cài đặt & chạy

### Trên Termux (Android)

```bash
# 1. Cài Termux từ F-Droid, mở lên gõ:
pkg install python -y

# 2. Copy file dat_tool_unity.py vào máy (ví dụ: thư mục Download)

# 3. Chạy:
cd /sdcard/Download
python dat_tool_unity.py
```

### Trên Linux / PC

```bash
python3 dat_tool_unity.py
```

Không cần quyền root, không cần internet sau khi đã có file.

---

## 🗺️ Quy trình Việt hóa chuẩn

```
 ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐    ┌─────────┐
 │ Option 6│───▶│  DỊCH  │───▶│Option 10│───▶│ Option 9 │───▶│Option 7 │
 │trích text│   │  JSON   │    │sửa font │    │thay font│    │đóng gói │
 └─────────┘    └─────────┘    │  TMP □  │    │ thường   │    └─────────┘
                               └──────────┘    └──────────┘
```

### Bước 1 — Trích văn bản (Option 6)

Nhập đường dẫn tới thư mục `Data` của game (chứa `data.unity3d`), hoặc trỏ thẳng vào file `.unity3d` / `.assets`.

Tool sẽ quét sâu mọi MonoBehaviour và xuất ra các file JSON — **mỗi JSON chỉ có trường `text`**:

```json
{
  "file": "level50",
  "obj_index": 76,
  "path_id": 77,
  "entries": [
    { "kind": "monobehaviour", "offset": 44, "text": "Hello, son. How has it been?" }
  ]
}
```

### Bước 2 — Dịch

Dịch nội dung trường `"text"` sang tiếng Việt. **Giữ nguyên mọi thứ khác** — không thêm trường mới, không đổi cấu trúc.

> ⚠️ Tool có chế độ kiểm tra: nếu JSON chứa trường lạ như `translation` thì sẽ cảnh báo.

### Bước 3 — Sửa font hội thoại (Option 10) 💬

Chữ hội thoại trong game Unity thường dùng **TextMeshPro**, atlas của nó chỉ chứa ký tự ASCII nên chữ Việt hiện thành `□`.

Option 10 sẽ:
- Tự tìm mọi font TMP đang ở chế độ Static
- Bật **Dynamic mode** + trỏ về font có đủ tiếng Việt
- Game sẽ tự vẽ thêm glyph Việt lúc chạy — chữ ASCII vẫn giữ nguyên style gốc

### Bước 4 — Thay font thường (Option 9) 🎨

Theo phong cách [anylang](https://github.com/giveptr/anylang):

1. Tải font có đủ tiếng Việt (Be Vietnam Pro, Noto Sans, Open Sans…)
2. Bỏ tất cả file `.ttf` / `.otf` vào **một thư mục**
3. Nhập đường dẫn thư mục đó vào tool

Tool tự đè font mới vào **tất cả** font gốc trong game (giữ nguyên tên để game vẫn load đúng), kiểm tra độ phủ tiếng Việt U+1EA0–U+1EF9 trước khi thay.

### Bước 5 — Đóng gói lại (Option 7)

Nhập thư mục chứa JSON đã dịch. Tool vá từng chuỗi vào đúng vị trí, rebuild bundle và **tự backup `.bak`**.

> ✅ Đã kiểm chứng: giữ nguyên `data_off` gốc nên game không bị crash sau khi vá.

---

## 🧰 Chi tiết từng Option

<details>
<summary><b>1–3. File .dat (XOR / JSON)</b></summary>

- **Option 1:** Decode 1 file `.dat` → JSON
- **Option 2:** Decode cả thư mục → JSON hàng loạt
- **Option 3:** Encode JSON đã dịch → file `.dat` gốc
</details>

<details>
<summary><b>4–5. File PFS (Artemis pf6/pf8)</b></summary>

- **Option 4:** Giải nén `.pfs` / `.pfs.000` → thư mục
- **Option 5:** Đóng gói lại tất cả → `.pfs` + `.pfs.000` gốc
</details>

<details>
<summary><b>6–7. Unity deep extract / repack</b></summary>

- **Option 6:** Trích sâu Unity → JSON văn bản game
  - Hỗ trợ UnityFS bundle (`data.unity3d`) và file `.assets` rời
  - Parser SerializedFile chịu được cả file `nobj=0` (tự fallback quét entries)
  - Xuất JSON gọn: metadata + `"text"`
- **Option 7:** Đóng gói lại Unity ← JSON đã dịch
  - Patch từng chuỗi MonoBehaviour đúng offset
  - Tự động bỏ qua TextAsset kỹ thuật (bảng ngắt dòng…) — không crash
  - Backup `.bak` trước khi ghi, verify cấu trúc sau rebuild
</details>

<details>
<summary><b>8. NFD test (thử nghiệm)</b></summary>

Chuyển text trong JSON sang dạng Unicode decomposed (NFD). Chỉ dùng để **test** khi nghi font thiếu glyph precomposed. Sao lưu JSON trước khi chạy.
</details>

<details>
<summary><b>9. Thay font game (kiểu anylang)</b></summary>

- Nhập thư mục chứa `.ttf` / `.otf` → tool tự thay vào mọi Unity Font (class 128)
- Đọc tên font từ bảng SFNT `name`, đọc metrics từ `head`/`hhea`
- Chỉ cập nhật `m_LineSpacing` / `m_Ascent` / `m_Descent` khi metrics cũ khớp font cũ (logic anylang)
- Kiểm tra độ phủ tiếng Việt **thật** qua cmap (glyphID ≠ 0), không đoán mò
</details>

<details>
<summary><b>10. Sửa font TextMeshPro (chữ hội thoại □)</b></summary>

- Quét mọi TMP FontAsset (nhận diện qua `m_Version` + `m_SourceFontFileGUID`)
- Tìm Font nguồn có đủ tiếng Việt trong cùng file `.assets`
- Ghi `m_SourceFontFile` → PPtr tới font nguồn, `m_AtlasPopulationMode` → Dynamic (1)
- Verify đọc lại sau rebuild, backup `.bak` trước khi ghi

*Nên chạy sau Option 9 để font nguồn chắc chắn đủ Việt.*
</details>

---

## 📱 Yêu cầu hệ thống

| | |
|---|---|
| **Python** | 3.8+ (chỉ dùng thư viện chuẩn) |
| **Thiết bị** | Android + Termux, hoặc bất kỳ Linux/PC nào |
| **Dung lượng** | File tool ~110 KB, 1 file duy nhất |
| **Quyền** | Không cần root |

---

## ⚠️ Lưu ý

- Luôn **sao lưu** file gốc / thư mục JSON trước khi chạy các option ghi file (tool cũng tự tạo `.bak`).
- JSON dịch: chỉ sửa trường `"text"`, không thêm trường mới.
- Option 8 (NFD) chỉ là công cụ test, không phải cách sửa font chính thức.
- Option 9 + 10 thay đổi font game — test kỹ trong game sau khi áp dụng.

---

## 🙏 Ghi nhận

- Ý tưởng thay font tham khảo từ [anylang](https://github.com/giveptr/anylang) (MIT).
- Cấu trúc TMP_FontAsset tham khảo source TextMeshPro (Unity).

---

<div align="center">

*Viết bằng Python thuần khiết — cho những người Việt hóa game chỉ bằng chiếc điện thoại.* 📱🇻🇳

</div>
