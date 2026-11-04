## 2. Thiết kế Lược đồ CSDL (Database Schema - PostgreSQL)

Hệ thống quản lý sách gồm 2 bảng có quan hệ **1 - N** (Một thể loại chứa nhiều cuốn sách):

### Bảng 1: `categories` (Bảng cha - Danh mục thể loại)
Bảng lưu trữ danh mục thể loại sách trong hệ thống.

| Tên cột (Column) | Kiểu dữ liệu (Data Type) | Ràng buộc (Constraints) | Mô tả chi tiết |
| :--- | :--- | :--- | :--- |
| `ma_the_loai` | `VARCHAR(10)` | `PRIMARY KEY` | Mã thể loại sách (Khóa chính, VD: 'TL01', 'TL02') |
| `ten_the_loai` | `VARCHAR(100)` | `NOT NULL` | Tên thể loại sách |

*Dữ liệu mẫu khởi tạo tự động:*
- `'TL01'` - `'Công nghệ thông tin'`
- `'TL02'` - `'Kinh tế - Kỹ năng'`

---

### Bảng 2: `books` (Bảng con - Danh mục sách)
Bảng lưu trữ thông tin các đầu sách hiện có trong kho thư viện.

| Tên cột (Column) | Kiểu dữ liệu (Data Type) | Ràng buộc (Constraints) | Mô tả chi tiết |
| :--- | :--- | :--- | :--- |
| `ma_sach` | `VARCHAR(20)` | `PRIMARY KEY` | Mã sách (Khóa chính, bắt đầu bằng 'BK') |
| `ten_sach` | `VARCHAR(255)` | `NOT NULL` | Tên đầu sách |
| `tac_gia` | `VARCHAR(150)` | `NOT NULL` | Tên tác giả |
| `nam_xb` | `INTEGER` | `NOT NULL, CHECK (nam_xb >= 1900 AND nam_xb <= 2026)` | Năm xuất bản (1900 - 2026) |
| `gia_bia` | `NUMERIC(12, 2)` | `NOT NULL, CHECK (gia_bia >= 0)` | Giá bìa sách (Số thực >= 0) |
| `ma_the_loai` | `VARCHAR(10)` | `NOT NULL, REFERENCES categories(ma_the_loai)` | Khóa ngoại (FK) tham chiếu bảng `categories` |

---

### Câu lệnh SQL tạo Bảng (DDL Scripts)

```sql
-- 1. Tạo bảng thể loại sách (Bảng cha)
CREATE TABLE IF NOT EXISTS categories (
    ma_the_loai VARCHAR(10) PRIMARY KEY,
    ten_the_loai VARCHAR(100) NOT NULL
);

-- Chèn dữ liệu mẫu nếu chưa có
INSERT INTO categories (ma_the_loai, ten_the_loai)
VALUES 
    ('TL01', 'Công nghệ thông tin'),
    ('TL02', 'Kinh tế - Kỹ năng')
ON CONFLICT (ma_the_loai) DO NOTHING;

-- 2. Tạo bảng sách (Bảng con)
CREATE TABLE IF NOT EXISTS books (
    ma_sach VARCHAR(20) PRIMARY KEY,
    ten_sach VARCHAR(255) NOT NULL,
    tac_gia VARCHAR(150) NOT NULL,
    nam_xb INTEGER NOT NULL CHECK (nam_xb >= 1900 AND nam_xb <= 2026),
    gia_bia NUMERIC(12, 2) NOT NULL CHECK (gia_bia >= 0),
    ma_the_loai VARCHAR(10) NOT NULL,
    FOREIGN KEY (ma_the_loai) REFERENCES categories(ma_the_loai) ON DELETE RESTRICT
);