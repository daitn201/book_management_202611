# Đề 06: Hệ Thống Quản Lý Sách Thư Viện (Library Book Management)

Hệ thống quản lý sách thư viện được xây dựng bằng ngôn ngữ **Python (OOP)** và cơ sở dữ liệu **PostgreSQL**, hỗ trợ kiểm tra dữ liệu đầu vào (Validation), thao tác CRUD an toàn và dịch vụ xử lý file CSV (Import/Export).

---

## 👨‍💻 Thông Tin Học Viên
- **Họ và tên:** Tạ Ngọc Đại
- **Đề tài:** Quản lý Sách Thư viện (Đề 06)
- **Công nghệ sử dụng:** Python 3.15.1, PostgreSQL, `psycopg2-binary`, VS Code, DBeaver.

---

## 📁 Cấu Trúc Dự Án

```text
book_management/
├── data/
│   ├── import_books.csv       # File dữ liệu mẫu đầu vào (có dòng hợp lệ & lỗi)
│   └── export_books.csv       # File xuất dữ liệu từ CSDL (tự động tạo)
├── docs/
│   └── DESIGN.md              # Sơ đồ DFD, Database Schema & Class Design
├── src/
│   ├── __init__.py
│   ├── models.py              # Định nghĩa Class Book & Logic Validation
│   ├── database.py            # Kết nối PostgreSQL & các hàm DDL/CRUD
│   └── csv_service.py         # Dịch vụ Import/Export dữ liệu CSV
├── .gitignore                 # Cấu hình bỏ qua các file rác Git
├── main.py                    # File kịch bản kiểm thử tích hợp toàn bộ hệ thống
└── README.md                  # Tài liệu hướng dẫn dự án
```

## ⚙️ Hướng Dẫn Cài Đặt & Chạy Dự Án

### 1. Yêu cầu hệ thống
- Python 3.15.1 trở lên.
- PostgreSQL Database Server đã được cài đặt và dịch vụ đang chạy trên `localhost:5432`.
- Đã tạo sẵn cơ sở dữ liệu `library_db` trên PostgreSQL (qua DBeaver hoặc pgAdmin).

### 2. Cài đặt thư viện phụ thuộc
Mở Terminal tại thư mục gốc của dự án (`book_management/`) và thực thi lệnh cài đặt driver kết nối PostgreSQL:

```bash
pip install psycopg2-binary
```

### 3. Lệnh thực thi kiểm thử toàn bộ hệ thống
```bash
python main.py