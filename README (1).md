<div align="center">

# 🎮 Unity DAT Tool

### Công cụ Việt hóa game Unity — chạy trực tiếp trên **Termux / Android**

*Trích xuất văn bản → dịch → đóng gói lại → sửa font — tất cả trong một file Python duy nhất, không cần PC.*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Android%20%7C%20Linux-green?logo=android&logoColor=white)](https://termux.dev/)
[![Deps](https://img.shields.io/badge/Dependencies-Chuẩn%20thư%20viện-orange)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

</div>

## Lưu ý được làm bằng Muse AI
Theo tôi muse AI làm có vẻ tệ lắm ở những code Dự án Manhwa của tôi nó vô cùng tự hại không thông minh bằng Cloude
---

## ✨ Tính năng

| # | Chức năng | Mô tả |
|---|-----------|-------|
| 1–3 | 📦 **File .dat** | Decode `.dat` (XOR/JSON) → JSON, encode ngược lại |
| 4–5 | 📦 **File PFS** | Giải nén / đóng gói lại `.pfs` (Artemis pf6/pf8) |
| 6 | 🔍 **Trích văn bản Unity PC** | Deep extract từ thư mục game PC (`*_Data`, `data.unity3d`, `.bundle`, `.assets`) → JSON (chỉ trường `text`) |
| 7 | 🔍 **Trích văn bản Unity APK** | Mở thẳng file `.apk`, tự giải `data.unity3d` + bundle Addressables + `.assets` bên trong → JSON |
| 8 | 📥 **Đóng gói lại Unity PC** | Vá JSON đã dịch vào file game PC gốc (giữ nguyên cấu trúc, có `.bak`) |
| 9 | 📥 **Đóng gói lại Unity APK** | Vá JSON đã dịch vào các file đã giải từ APK, rồi **tự gói lại thành APK mới** (chưa ký) |
| 10 | 🔤 **NFD test** | Chuyển JSON sang Unicode decomposed để test font |
| 11 | 🎨 **Thay font game** | Kiểu anylang: bỏ font TTF/OTF vào thư mục, tool tự đè vào mọi font gốc |
| 12 | 💬 **Sửa font TMP** | Bật Dynamic cho TextMeshPro → hết lỗi **□** ở chữ hội thoại |
| 13 | 📱 **Đóng gói APK đúng cách** | Gói 1 file đã vá rời vào APK (STORED + căn lề 4096) → fix game chạy chậm / lag cảm ứng |

> **100% thư viện chuẩn Python** — không cần `pip install` gì cả. Copy 1 file `.py` vào điện thoại là chạy.

### 🧠 Đã tích hợp kĩ năng dịch Unity thực tế

- **Quét MỌI kho text, không sót một kho nào:** MonoBehaviour, TextAsset, sheet Utage, **Lean Localization CSV**, kịch bản **Naninovel**, bảng **Utage TSV** (chỉ cột English), bảng **Unity Localization** nằm trong bundle **Addressables (`.bundle`)**, text cứng trong TMP — và **mọi bản sao** của cùng một bảng text (`sharedassets` / `resources` / `level*`), vì vá thiếu một bản sao là game vẫn hiện text cũ ở một số màn.
- **Lọc code 3 lớp:** lọc symbol kiểu anylang (camelCase, tên file, biểu thức…) → lọc theo **ngữ cảnh + tần suất toàn file** (lệnh `If`, `Wait`, `smile3`, tham số Live2D, tên kiểu .NET, tên font TMP…) → đọc chuỗi bằng `_read_ustr_text` chống byte điều khiển nuốt mất thoại phía sau.
- **Audit từ đơn UI:** chuỗi 1 từ bị lọc code nhưng trông như nhãn UI (`Mii`, `Next`, `Punch`, `Hide`…) không bị vứt hẳn — chúng xuất hiện trong JSON với cờ `"ui_audit": true`. Là nhãn thật thì dịch, là code thì giữ nguyên. Khi đóng gói, mục `ui_audit` chỉ được vá khi bạn đã sửa text.
- **Lean CSV tách ở dấu phẩy ĐẦU TIÊN** — giá trị chứa dấu phẩy không bị cắt cụt (lỗi kinh điển khi parse bằng csv).
- **Naninovel:** giữ nguyên dòng nhãn `#` (cả `# ~hash` lẫn `# label`), comment `;` và lệnh `@` — chỉ xuất dòng thoại.
- **Sync catalog Addressables:** đóng gói xong 1 bundle Addressables, tool in ra `m_Crc` (crc32 của toàn bộ stream đã giải nén) và `m_BundleSize` cần cập nhật vào `catalog.json` — không sync là game báo *No translation found*.
- **Kiểm tra kí tự bản dịch:** sau khi đóng gói, tool liệt kê toàn bộ kí tự khác nhau bản dịch đã dùng (kể cả dấu câu / kí hiệu) để đối chiếu với font — thiếu dù 1 kí tự là hiện □ trong game.
- **Đóng gói APK (Option 9/13):** file dữ liệu Unity để dạng **STORED + căn lề 4096** (kiểu zipalign `-p`) để game không bị chậm / chạm lâu mới ăn; tắt được `android:debuggable`. APK xuất ra **chưa có chữ ký — phải ký lại (v1+v2+v3)** mới cài được.

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

### Bản PC

```
 ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐    ┌─────────┐
 │ Option 6│───▶│  DỊCH  │───▶│Option 12│───▶│ Option 11│───▶│Option 8 │
 │trích PC │   │  JSON   │    │sửa font │    │thay font │    │gói PC   │
 └─────────┘    └─────────┘    │  TMP □  │    │ thường   │    └─────────┘
                               └─────────┘    └──────────┘
```

### Bản APK (Android)

```
 ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐    ┌─────────┐    ┌────────┐
 │ Option 7│───▶│  DỊCH  │───▶│Option 12│───▶│ Option 11│───▶│Option 9 │───▶│ KÝ APK │
 │trích APK│   │  JSON   │    │sửa font │    │thay font │    │gói APK  │    │v1+v2+v3│
 └─────────┘    └─────────┘    │  TMP □  │    │ thường   │    └─────────┘    └────────┘
                               └─────────┘    └──────────┘
```

> Option 11/12 chạy trên **file** `data.unity3d` / `.assets`: bản PC trỏ vào file trong thư mục game, bản APK trỏ vào file đã giải ra trong thư mục `unity_apk_work` (Option 7 tạo), xong đóng gói bằng Option 9.

### Bước 1 — Trích văn bản (Option 6 cho PC / Option 7 cho APK)

- **PC (6):** nhập đường dẫn thư mục game (chứa `*_Data`), thư mục `*_Data`, hoặc trỏ thẳng vào file `.unity3d` / `.bundle` / `.assets`.
- **APK (7):** nhập đường dẫn file `.apk`. Tool tự giải các file Unity bên trong ra thư mục `unity_apk_work` (kèm `apk_manifest.txt` ghi rõ file nào nằm ở đâu trong APK) rồi trích như bản PC. **APK gốc không bị sửa ở bước này.**

Tool quét sâu mọi kho text và xuất ra các file JSON — **mỗi JSON chỉ có trường `text`** để sửa:

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

Các mục đặc biệt trong JSON:

| Cờ / loại | Ý nghĩa |
|---|---|
| `"ui_audit": true` | Từ đơn bị bộ lọc code rà lại — kiểm tra: nhãn UI thì dịch, code thì giữ nguyên |
| `"kind": "textasset_line"` | 1 dòng của kho text dạng dòng (Lean CSV / Naninovel / Utage TSV) — cứ sửa `text`, tool tự dựng lại đúng cấu trúc khi đóng gói |

### Bước 2 — Dịch

Dịch nội dung trường `"text"` sang tiếng Việt. **Giữ nguyên mọi thứ khác** — không thêm trường mới, không đổi cấu trúc.

> ⚠️ Tool có chế độ kiểm tra: nếu JSON chứa trường lạ như `translation` thì sẽ cảnh báo.

### Bước 3 — Sửa font hội thoại (Option 12) 💬

Chữ hội thoại trong game Unity thường dùng **TextMeshPro**, atlas của nó chỉ chứa ký tự ASCII nên chữ Việt hiện thành `□`.

Option 12 sẽ:
- Tự tìm mọi font TMP đang ở chế độ Static
- Bật **Dynamic mode** + trỏ về font có đủ tiếng Việt
- Game sẽ tự vẽ thêm glyph Việt lúc chạy — chữ ASCII vẫn giữ nguyên style gốc

### Bước 4 — Thay font thường (Option 11) 🎨

Theo phong cách [anylang](https://github.com/giveptr/anylang):

1. Tải font có đủ tiếng Việt (Be Vietnam Pro, Noto Sans, Open Sans…)
2. Bỏ tất cả file `.ttf` / `.otf` vào **một thư mục**
3. Nhập đường dẫn thư mục đó vào tool

Tool tự đè font mới vào **tất cả** font gốc trong game (giữ nguyên tên để game vẫn load đúng), kiểm tra độ phủ tiếng Việt U+1EA0–U+1EF9 trước khi thay.

### Bước 5 — Đóng gói lại (Option 8 cho PC / Option 9 cho APK)

- **PC (8):** nhập thư mục `unity_text` (Option 6 tạo). Tool vá từng chuỗi vào đúng vị trí, rebuild bundle/file và **tự backup `.bak`**, ghi thẳng vào file game.
- **APK (9):** nhập thư mục `unity_text_apk` (Option 7 tạo). Tool vá vào các file trong `unity_apk_work`, rồi **tự gói lại vào APK gốc** thành file `*_VI_unsigned.apk`. **Phải ký lại APK (v1+v2+v3)** bằng Uber APK Signer / MT Manager rồi mới cài được; ký bằng key khác bản gốc thì gỡ bản gốc trước khi cài.

> ✅ Đã kiểm chứng: giữ nguyên `data_off` gốc nên game không bị crash sau khi vá.
>
> ⚠️ Nếu bundle vừa vá là bundle **Addressables**, tool sẽ in `m_Crc` + `m_BundleSize` mới — nhớ cập nhật 2 giá trị này vào `catalog.json` của game, nếu không game sẽ không nạp được bản dịch.

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
<summary><b>6–9. Unity: trích / đóng gói — PC và APK riêng từng số</b></summary>

- **Option 6 — Trích văn bản Unity PC:** thư mục game / `*_Data` / file `.unity3d` / `.bundle` / `.assets` → JSON
  - Hỗ trợ UnityFS bundle (`data.unity3d`, `.bundle` Addressables) và file `.assets` / `level*` rời
  - Quét mọi kho text + mọi bản sao của bảng text; lọc code 3 lớp + audit từ đơn UI
  - Parser SerializedFile chịu được cả file `nobj=0` (tự fallback quét entries)
- **Option 7 — Trích văn bản Unity APK:** nhập file `.apk` → tự giải file Unity bên trong ra `unity_apk_work` + `apk_manifest.txt` → JSON trong `unity_text_apk`
- **Option 8 — Đóng gói lại Unity PC:** vá JSON đã dịch vào file game PC gốc
  - Patch từng chuỗi MonoBehaviour đúng offset; dựng lại nguyên script cho kho text dạng dòng (Lean CSV / Naninovel / Utage TSV)
  - Tự động bỏ qua chuỗi code bị sửa nhầm (trừ mục `ui_audit` bạn chủ động sửa)
  - Backup `.bak` trước khi ghi, verify cấu trúc sau rebuild, in CRC/size để sync catalog Addressables + danh sách kí tự bản dịch đã dùng
- **Option 9 — Đóng gói lại Unity APK:** như Option 8 nhưng vá vào file đã giải từ APK, xong **tự gói lại thành APK mới** `*_VI_unsigned.apk` (STORED + căn lề 4096, tắt được debuggable) — ký lại rồi cài
</details>

<details>
<summary><b>10. NFD test (thử nghiệm)</b></summary>

Chuyển text trong JSON (`unity_text` / `unity_text_apk`) sang dạng Unicode decomposed (NFD). Chỉ dùng để **test** khi nghi font thiếu glyph precomposed. Sao lưu JSON trước khi chạy.
</details>

<details>
<summary><b>11. Thay font game (kiểu anylang)</b></summary>

- Nhập thư mục chứa `.ttf` / `.otf` → tool tự thay vào mọi Unity Font (class 128) trong file `data.unity3d` / `.assets` bạn trỏ vào
- Đọc tên font từ bảng SFNT `name`, đọc metrics từ `head`/`hhea`
- Chỉ cập nhật `m_LineSpacing` / `m_Ascent` / `m_Descent` khi metrics cũ khớp font cũ (logic anylang)
- Kiểm tra độ phủ tiếng Việt **thật** qua cmap (glyphID ≠ 0), không đoán mò
</details>

<details>
<summary><b>12. Sửa font TextMeshPro (chữ hội thoại □)</b></summary>

- Quét mọi TMP FontAsset (nhận diện qua `m_Version` + `m_SourceFontFileGUID`)
- Tìm Font nguồn có đủ tiếng Việt trong cùng file `.assets`
- Ghi `m_SourceFontFile` → PPtr tới font nguồn, `m_AtlasPopulationMode` → Dynamic (1)
- Verify đọc lại sau rebuild, backup `.bak` trước khi ghi

*Nên chạy sau Option 11 để font nguồn chắc chắn đủ Việt.*
</details>

<details>
<summary><b>13. Đóng gói APK đúng cách (thủ công)</b></summary>

- Dùng khi bạn chỉ có **1 file đã vá rời** (vd `data.unity3d`) và muốn nhét vào APK: tool lưu file dữ liệu Unity dạng STORED + căn lề 4096, tắt được `android:debuggable`, bỏ chữ ký cũ
- Trường hợp đóng gói thường từ JSON hãy dùng **Option 9** (đã bao gồm bước này)
- APK xuất ra chưa ký → ký lại (v1+v2+v3) rồi cài
</details>

---

## 📱 Yêu cầu hệ thống

| | |
|---|---|
| **Python** | 3.8+ (chỉ dùng thư viện chuẩn) |
| **Thiết bị** | Android + Termux, hoặc bất kỳ Linux/PC nào |
| **Dung lượng** | File tool ~165 KB, 1 file duy nhất |
| **Quyền** | Không cần root |

---

## ⚠️ Lưu ý

- Luôn **sao lưu** file gốc / thư mục JSON trước khi chạy các option ghi file (tool cũng tự tạo `.bak`).
- JSON dịch: chỉ sửa trường `"text"`, không thêm trường mới.
- Mục `"ui_audit": true`: chỉ sửa khi chắc chắn đó là nhãn UI — sửa nhầm chuỗi code sẽ làm game lỗi.
- Option 10 (NFD) chỉ là công cụ test, không phải cách sửa font chính thức.
- Option 11 + 12 thay đổi font game — test kỹ trong game sau khi áp dụng.
- Bundle Addressables: sau Option 8/9 nhớ sync `m_Crc` / `m_BundleSize` vào `catalog.json` theo số tool in ra.
- APK do Option 9/13 xuất ra **chưa có chữ ký** — không ký lại sẽ không cài được.

---

## 🙏 Ghi nhận

- Ý tưởng thay font tham khảo từ [anylang](https://github.com/giveptr/anylang) (MIT).
- Cấu trúc TMP_FontAsset tham khảo source TextMeshPro (Unity).

---

<div align="center">

*Viết bằng Python thuần khiết — cho những người Việt hóa game chỉ bằng chiếc điện thoại.* 📱🇻🇳

</div>
