"""
src/database.py
Mục đích: Test kết nối tới PostgreSQL
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Cấu hình thông số kết nối PostgreSQL của máy bạn
DB_CONFIG = {
    "dbname": "library_db",    
    "user": "postgres",        
    "password": "postgres123", 
    "host": "localhost",
    "port": "5432"
}

def get_connection():
    """Tạo và trả về kết nối tới CSDL PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"❌ Lỗi kết nối CSDL PostgreSQL: {e}")
        raise e


def init_db():
    """
    Khởi tạo lược đồ CSDL:
    1. Tạo bảng categories (Thể loại)
    2. Chèn 2 thể loại mẫu (TL01, TL02)
    3. Tạo bảng books (Sách - khóa ngoại ON DELETE RESTRICT)
    """
    # 1. SQL Tạo bảng categories
    create_categories_sql = """
    CREATE TABLE IF NOT EXISTS categories (
        ma_the_loai VARCHAR(10) PRIMARY KEY,
        ten_the_loai VARCHAR(100) NOT NULL
    );
    """

    # 2. SQL Chèn 2 thể loại mẫu (Bỏ qua nếu đã tồn tại)
    insert_categories_sql = """
    INSERT INTO categories (ma_the_loai, ten_the_loai)
    VALUES 
        ('TL01', 'Công nghệ thông tin'),
        ('TL02', 'Kinh tế - Kỹ năng')
    ON CONFLICT (ma_the_loai) DO NOTHING;
    """

    # 3. SQL Tạo bảng books
    create_books_sql = """
    CREATE TABLE IF NOT EXISTS books (
        ma_sach VARCHAR(20) PRIMARY KEY,
        ten_sach VARCHAR(255) NOT NULL,
        tac_gia VARCHAR(150) NOT NULL,
        nam_xb INTEGER NOT NULL CHECK (nam_xb >= 1900 AND nam_xb <= 2026),
        gia_bia NUMERIC(12, 2) NOT NULL CHECK (gia_bia >= 0),
        ma_the_loai VARCHAR(10) NOT NULL,
        FOREIGN KEY (ma_the_loai) REFERENCES categories(ma_the_loai) ON DELETE RESTRICT
    );
    """

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Thực thi tạo bảng categories
            cursor.execute(create_categories_sql)
            
            # Thực thi chèn 2 thể loại mẫu
            cursor.execute(insert_categories_sql)
            
            # Thực thi tạo bảng books
            cursor.execute(create_books_sql)
            
            # Luyện commit giao dịch vào DB
            conn.commit()
            print("✅ Khởi tạo lược đồ CSDL & chèn dữ liệu thể loại mẫu thành công!")
    except Exception as e:
        conn.rollback()
        print(f"❌ Lỗi khởi tạo CSDL: {e}")
        raise e
    finally:
        conn.close()

def add_book(book):
    """
    Thêm một bản ghi sách mới từ đối tượng Book vào CSDL PostgreSQL.
    :param book: Đối tượng thuộc lớp Book (từ src.models)
    :return: True nếu thêm thành công, Raise Exception nếu thất bại.
    """
    insert_sql = """
    INSERT INTO books (ma_sach, ten_sach, tac_gia, nam_xb, gia_bia, ma_the_loai)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(insert_sql, (
                book.ma_sach,
                book.ten_sach,
                book.tac_gia,
                book.nam_xb,
                book.gia_bia,
                book.ma_the_loai
            ))
            conn.commit()
            print(f"✅ Thêm thành công sách: {book.ma_sach} - {book.ten_sach}")
            return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Lỗi khi thêm sách {book.ma_sach}: {e}")
        raise e
    finally:
        conn.close()

"""
src/database.py - Bổ sung hàm get_all_books_with_category
"""

def get_all_books_with_category():
    """
    Truy vấn lấy toàn bộ danh sách sách kết hợp INNER JOIN với bảng categories.
    :return: List chứa các Dictionary thông tin sách kèm 'ten_the_loai'.
    """
    select_join_sql = """
    SELECT 
        b.ma_sach,
        b.ten_sach,
        b.tac_gia,
        b.nam_xb,
        b.gia_bia,
        b.ma_the_loai,
        c.ten_the_loai
    FROM books b
    INNER JOIN categories c ON b.ma_the_loai = c.ma_the_loai
    ORDER BY b.ma_sach ASC;
    """
    
    conn = get_connection()
    try:
        # Sử dụng RealDictCursor để kết quả trả về dạng dictionary theo tên cột
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(select_join_sql)
            books = cursor.fetchall()
            return books
    except psycopg2.Error as e:
        print(f"❌ Lỗi truy vấn danh sách sách: {e}")
        raise e
    finally:
        conn.close()

"""
src/database.py - Bổ sung hàm update_book
"""

def update_book(ma_sach, ten_sach=None, tac_gia=None, nam_xb=None, gia_bia=None, ma_the_loai=None):
    """
    Cập nhật thông tin sách theo mã sách. Chỉ cập nhật các trường được truyền giá trị vào.
    
    :param ma_sach: Mã sách cần cập nhật (bắt buộc)
    :param ten_sach: Tên sách mới (tùy chọn)
    :param tac_gia: Tác giả mới (tùy chọn)
    :param nam_xb: Năm xuất bản mới (tùy chọn)
    :param gia_bia: Giá bìa mới (tùy chọn)
    :param ma_the_loai: Mã thể loại mới (tùy chọn)
    :return: True nếu cập nhật thành công, False nếu không tìm thấy ma_sach.
    """
    # Xây dựng động câu lệnh SET dựa trên các tham số được truyền vào
    update_fields = []
    params = []

    if ten_sach is not None:
        update_fields.append("ten_sach = %s")
        params.append(ten_sach)
    if tac_gia is not None:
        update_fields.append("tac_gia = %s")
        params.append(tac_gia)
    if nam_xb is not None:
        update_fields.append("nam_xb = %s")
        params.append(nam_xb)
    if gia_bia is not None:
        update_fields.append("gia_bia = %s")
        params.append(gia_bia)
    if ma_the_loai is not None:
        update_fields.append("ma_the_loai = %s")
        params.append(ma_the_loai)

    if not update_fields:
        print("⚠️ Không có thông tin nào được yêu cầu cập nhật.")
        return False

    # Ghép các trường cần update và thêm ma_sach vào điều kiện WHERE
    sql = f"UPDATE books SET {', '.join(update_fields)} WHERE ma_sach = %s;"
    params.append(ma_sach)

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, tuple(params))
            row_count = cursor.rowcount
            conn.commit()

            if row_count > 0:
                print(f"✅ Cập nhật thành công thông tin cho sách mã: {ma_sach}")
                return True
            else:
                print(f"⚠️ Không tìm thấy sách có mã {ma_sach} để cập nhật.")
                return False
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Lỗi khi cập nhật sách {ma_sach}: {e}")
        raise e
    finally:
        conn.close()

"""
src/database.py - Bổ sung hàm delete_book
"""

def delete_book(ma_sach):
    """
    Xóa một bản ghi sách khỏi CSDL PostgreSQL theo mã sách.
    
    :param ma_sach: Mã sách cần xóa (ví dụ: 'BK001')
    :return: True nếu xóa thành công, False nếu không tìm thấy mã sách.
    """
    delete_sql = "DELETE FROM books WHERE ma_sach = %s;"
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(delete_sql, (ma_sach,))
            row_count = cursor.rowcount
            conn.commit()

            if row_count > 0:
                print(f"✅ Đã xóa thành công sách mã: {ma_sach}")
                return True
            else:
                print(f"⚠️ Không tìm thấy sách có mã {ma_sach} để xóa.")
                return False
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Lỗi khi xóa sách {ma_sach}: {e}")
        raise e
    finally:
        conn.close()        

if __name__ == "__main__":
    init_db()
    from models import Book
    
    # 1. Thử xóa cuốn sách BK001
    print("\n--- THỰC THI XÓA SÁCH BK001 ---")
    delete_book("BK001")

    # 2. In lại danh sách sách sau khi xóa
    print("\n--- DANH SÁCH SÁCH TRONG CSDL SAU KHI XÓA ---")
    books = get_all_books_with_category()
    if not books:
        print("📭 Cơ sở dữ liệu hiện không có sách nào.")
    else:
        for b in books:
            print(f"[{b['ma_sach']}] {b['ten_sach']} - Tác giả: {b['tac_gia']}")