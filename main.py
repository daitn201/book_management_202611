"""
main.py
Kịch bản kiểm thử tích hợp toàn bộ hệ thống Quản lý Sách Thư viện (Đề 06)
"""

import os
from src.database import (
    init_db,
    get_all_books_with_category,
    update_book,
    delete_book
)
from src.csv_service import import_books_from_csv, export_books_to_csv


def display_book_list(title="DANH SÁCH SÁCH TRONG CSDL"):
    """Hàm hỗ trợ in danh sách sách đẹp mắt ra màn hình Console."""
    print(f"\n================ {title} ================")
    books = get_all_books_with_category()
    
    if not books:
        print("📭 Cơ sở dữ liệu hiện chưa có cuốn sách nào.")
        print("=" * (35 + len(title)))
        return

    print(f"{'STT':<4} | {'Mã Sách':<8} | {'Tên Sách':<32} | {'Tác Giả':<20} | {'Năm XB':<6} | {'Giá Bìa (VNĐ)':<13} | {'Thể Loại'}")
    print("-" * 110)
    
    for idx, b in enumerate(books, start=1):
        print(
            f"{idx:<4} | {b['ma_sach']:<8} | {b['ten_sach']:<32} | "
            f"{b['tac_gia']:<20} | {b['nam_xb']:<6} | "
            f"{float(b['gia_bia']):>13,.0f} | {b['ten_the_loai']} ({b['ma_the_loai']})"
        )
    print("=" * 110)


def main():
    print("🚀 BẮT ĐẦU KỊCH BẢN KIỂM THỬ TÍCH HỢP HỆ THỐNG QUẢN LÝ SÁCH")
    
    # -------------------------------------------------------------------
    # BƯỚC 1: Khởi tạo CSDL PostgreSQL và nạp dữ liệu Thể loại mẫu
    # -------------------------------------------------------------------
    print("\n[BƯỚC 1] Khởi tạo CSDL & Nạp bảng Thể loại mẫu...")
    init_db()

    # -------------------------------------------------------------------
    # BƯỚC 2: Import dữ liệu từ file CSV vào CSDL
    # -------------------------------------------------------------------
    import_path = os.path.join("data", "import_books.csv")
    print(f"\n[BƯỚC 2] Import dữ liệu từ file CSV: {import_path}")
    import_books_from_csv(import_path)

    # Hiển thị danh sách sách sau khi import
    display_book_list("DANH SÁCH SÁCH SAU KHI IMPORT CSV")

    # -------------------------------------------------------------------
    # BƯỚC 3: Thử nghiệm hàm Update (Cập nhật thông tin sách BK001)
    # -------------------------------------------------------------------
    print("\n[BƯỚC 3] Kiểm thử Cập nhật (Update) sách BK001...")
    update_book(
        ma_sach="BK001",
        tac_gia="Nguyễn Văn A (Đã Chỉnh Sửa)",
        gia_bia=175000.0
    )
    display_book_list("DANH SÁCH SÁCH SAU KHI UPDATE BK001")

    # -------------------------------------------------------------------
    # BƯỚC 4: Thử nghiệm hàm Delete (Xóa sách BK004)
    # -------------------------------------------------------------------
    print("\n[BƯỚC 4] Kiểm thử Xóa (Delete) sách BK004...")
    delete_book("BK004")
    display_book_list("DANH SÁCH SÁCH SAU KHI XÓA BK004")

    # -------------------------------------------------------------------
    # BƯỚC 5: Export dữ liệu toàn bộ CSDL hiện tại ra file CSV mới
    # -------------------------------------------------------------------
    export_path = os.path.join("data", "export_books.csv")
    print(f"\n[BƯỚC 5] Export dữ liệu ra file CSV: {export_path}")
    export_books_to_csv(export_path)

    print("\n🎉 HOÀN THÀNH KỊCH BẢN KIỂM THỬ TÍCH HỢP HỆ THỐNG!")


if __name__ == "__main__":
    main()