"""
src/csv_service.py
Dịch vụ xử lý đọc/ghi file CSV và tích hợp với CSDL.
"""

import csv
import os
import psycopg2
from models import Book
from database import add_book, get_all_books_with_category


def import_books_from_csv(file_path):
    """
    Đọc dữ liệu từ file CSV, validate qua class Book và chèn vào CSDL PostgreSQL.
    Bỏ qua các dòng dữ liệu không hợp lệ hoặc bị lỗi CSDL (ví dụ trùng mã sách).
    
    :param file_path: Đường dẫn tới file CSV (ví dụ: 'data/import_books.csv')
    :return: (thanh_cong, thất_bai) Số lượng dòng xử lý thành công và thất bại
    """
    if not os.path.exists(file_path):
        print(f"❌ Không tìm thấy file tại đường dẫn: {file_path}")
        return 0, 0

    success_count = 0
    fail_count = 0

    print(f"\n⏳ Bắt đầu đọc dữ liệu từ file: {file_path}...")
    
    with open(file_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        
        for index, row in enumerate(reader, start=2):  # start=2 vì dòng 1 là Header
            try:
                # 1. Ép kiểu dữ liệu từ chuỗi trong CSV
                ma_sach = row.get("ma_sach", "").strip()
                ten_sach = row.get("ten_sach", "").strip()
                tac_gia = row.get("tac_gia", "").strip()
                nam_xb = int(row.get("nam_xb", 0))
                gia_bia = float(row.get("gia_bia", 0.0))
                ma_the_loai = row.get("ma_the_loai", "").strip()

                # 2. Khởi tạo đối tượng Book (Tự động kích hoạt validation trong __init__)
                book = Book(
                    ma_sach=ma_sach,
                    ten_sach=ten_sach,
                    tac_gia=tac_gia,
                    nam_xb=nam_xb,
                    gia_bia=gia_bia,
                    ma_the_loai=ma_the_loai
                )

                # 3. Ghi vào CSDL PostgreSQL
                add_book(book)
                success_count += 1

            except ValueError as ve:
                # Bắt lỗi validation dữ liệu từ Class Book hoặc lỗi ép kiểu (int/float)
                fail_count += 1
                print(f"⚠️ Dòng {index} [Lỗi dữ liệu]: {ve} -> Bỏ qua dòng này.")

            except psycopg2.Error as db_err:
                # Bắt lỗi CSDL (ví dụ trùng khóa chính ma_sach, hoặc vi phạm khóa ngoại ma_the_loai)
                fail_count += 1
                print(f"⚠️ Dòng {index} [Lỗi CSDL]: {db_err.pgerror or db_err} -> Bỏ qua dòng này.")

            except Exception as e:
                fail_count += 1
                print(f"⚠️ Dòng {index} [Lỗi không xác định]: {e} -> Bỏ qua dòng này.")

    print("\n--- BÁO CÁO TỔNG KẾT IMPORT ---")
    print(f"✅ Thêm thành công: {success_count} dòng")
    print(f"❌ Thất bại / Bỏ qua: {fail_count} dòng")
    
    return success_count, fail_count

"""
src/csv_service.py - Bổ sung hàm export_books_to_csv
"""

def export_books_to_csv(output_path):
    """
    Truy vấn dữ liệu từ CSDL (kèm Tên thể loại) và xuất ra file CSV.
    
    :param output_path: Đường dẫn file CSV đầu ra (ví dụ: 'data/export_books.csv')
    :return: True nếu xuất file thành công, False nếu có lỗi
    """
    try:
        # 1. Lấy dữ liệu sách từ PostgreSQL (đã INNER JOIN với bảng categories)
        books = get_all_books_with_category()

        if not books:
            print("⚠️ CSDL hiện không có bản ghi nào để xuất ra file CSV.")

        # 2. Đảm bảo thư mục chứa file đầu ra tồn tại
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # 3. Định nghĩa tiêu đề cột cho file CSV đầu ra
        fieldnames = ["ma_sach", "ten_sach", "tac_gia", "nam_xb", "gia_bia", "ma_the_loai", "ten_the_loai"]

        # 4. Ghi dữ liệu vào file CSV với utf-8-sig (để mở không bị lỗi font trên Excel)
        with open(output_path, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Ghi dòng Header
            writer.writeheader()
            
            # Ghi danh sách bản ghi
            for b in books:
                # Chuyển đổi gia_bia về float để định dạng số sạch trong CSV
                b_copy = dict(b)
                b_copy["gia_bia"] = float(b_copy["gia_bia"])
                writer.writerow(b_copy)

        print(f"✅ Xuất dữ liệu ra file thành công: {output_path} ({len(books)} bản ghi)")
        return True

    except Exception as e:
        print(f"❌ Lỗi khi xuất file CSV: {e}")
        return False

if __name__ == "__main__":
    # Test thử hàm import nếu file data/import_books.csv đã tồn tại
    import_path = os.path.join("data", "import_books.csv")
    export_path = os.path.join("data", "export_books.csv")
    # import_books_from_csv(import_path)
    export_books_to_csv(export_path)
