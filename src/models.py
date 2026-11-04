"""
src/models.py
Định nghĩa Lớp Book và logic kiểm tra hợp lệ dữ liệu (Validation Rules)
"""

class Book:
    """
    Lớp đại diện cho đối tượng Sách trong hệ thống Quản lý Thư viện.
    """
    def __init__(self, ma_sach: str, ten_sach: str, tac_gia: str, nam_xb: int, gia_bia: float, ma_the_loai: str):
        self.ma_sach = ma_sach
        self.ten_sach = ten_sach
        self.tac_gia = tac_gia
        self.nam_xb = nam_xb
        self.gia_bia = gia_bia
        self.ma_the_loai = ma_the_loai
        
        # Tự động kích hoạt kiểm tra tính hợp lệ ngay khi khởi tạo đối tượng
        self._validate()

    def _validate(self) -> None:
        """
        Phương thức private kiểm tra các rào chắn hợp lệ dữ liệu.
        Kích hoạt ValueError nếu có bất kỳ thuộc tính nào vi phạm quy tắc.
        """
        # 1. Kiểm tra Mã sách: Bắt buộc chuỗi và bắt đầu bằng 'BK'
        if not isinstance(self.ma_sach, str) or not self.ma_sach.strip().startswith("BK"):
            raise ValueError(f"Mã sách '{self.ma_sach}' không hợp lệ: Bắt buộc phải bắt đầu bằng 'BK'.")

        # 2. Kiểm tra Tên sách: Không được để trống
        if not isinstance(self.ten_sach, str) or not self.ten_sach.strip():
            raise ValueError("Tên sách không được để trống hoặc chỉ chứa khoảng trắng.")

        # 3. Kiểm tra Tác giả: Không được để trống
        if not isinstance(self.tac_gia, str) or not self.tac_gia.strip():
            raise ValueError("Tác giả không được để trống hoặc chỉ chứa khoảng trắng.")

        # 4. Kiểm tra Năm xuất bản: Số nguyên từ 1900 đến 2026
        try:
            nam_xb_int = int(self.nam_xb)
        except (ValueError, TypeError):
            raise ValueError(f"Năm xuất bản '{self.nam_xb}' phải là một số nguyên.")
            
        if not (1900 <= nam_xb_int <= 2026):
            raise ValueError(f"Năm xuất bản {nam_xb_int} không hợp lệ: Phải nằm trong khoảng từ 1900 đến 2026.")
        self.nam_xb = nam_xb_int

        # 5. Kiểm tra Giá bìa: Số thực hoặc nguyên >= 0
        try:
            gia_bia_float = float(self.gia_bia)
        except (ValueError, TypeError):
            raise ValueError(f"Giá bìa '{self.gia_bia}' phải là số.")
            
        if gia_bia_float < 0:
            raise ValueError(f"Giá bìa {gia_bia_float} không hợp lệ: Giá bìa không được nhỏ hơn 0.")
        self.gia_bia = gia_bia_float

        # 6. Kiểm tra Mã thể loại: Không được để trống
        if not isinstance(self.ma_the_loai, str) or not self.ma_the_loai.strip():
            raise ValueError("Mã thể loại không được để trống.")

    def to_dict(self) -> dict:
        """
        Chuyển đổi thông tin đối tượng Book thành Dictionary.
        Phục vụ cho việc ghi file CSV hoặc phản hồi dữ liệu API.
        """
        return {
            "ma_sach": self.ma_sach.strip(),
            "ten_sach": self.ten_sach.strip(),
            "tac_gia": self.tac_gia.strip(),
            "nam_xb": self.nam_xb,
            "gia_bia": self.gia_bia,
            "ma_the_loai": self.ma_the_loai.strip()
        }

    def __str__(self) -> str:
        """
        Định dạng chuỗi hiển thị thông tin sách trực quan ra màn hình Console.
        """
        return (f"Book(Mã: '{self.ma_sach}', Tên: '{self.ten_sach}', "
                f"Tác giả: '{self.tac_gia}', Năm XB: {self.nam_xb}, "
                f"Giá: {self.gia_bia:,.0f} VNĐ, Mã TL: '{self.ma_the_loai}')")