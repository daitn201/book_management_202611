### Bảng Quy tắc Kiểm tra Hợp lệ (Validation Rules)

Mọi bản ghi dữ liệu (nhập tay từ console hoặc đọc từ file CSV) bắt buộc phải vượt qua các quy tắc bên dưới trước khi khởi tạo đối tượng:

| Thuộc tính | Quy tắc Kiểm tra (Rule) | Lỗi bắn ra khi vi phạm (`ValueError`) |
| :--- | :--- | :--- |
| `ma_sach` | Khác rỗng, phải bắt đầu bằng tiền tố `'BK'` | `ValueError("Mã sách '{self.ma_sach}' không hợp lệ: Bắt buộc phải bắt đầu bằng 'BK'.'")` |
| `ten_sach` | Khác rỗng, không chứa toàn khoảng trắng | `ValueError("Tên sách không được để trống hoặc chỉ chứa khoảng trắng.")` |
| `tac_gia` | Khác rỗng, không chứa toàn khoảng trắng | `ValueError("Tác giả không được để trống hoặc chỉ chứa khoảng trắng.")` |
| `nam_xb` | Là số nguyên** | `ValueError("Năm xuất bản '{self.nam_xb}' phải là một số nguyên.")` |
| `nam_xb` | Là số nguyên trong khoảng **1900 đến 2026** | `Năm xuất bản {nam_xb_int} không hợp lệ: Phải nằm trong khoảng từ 1900 đến 2026.` |
| `gia_bia` | Là số thực/nguyên ** | `ValueError("Giá bìa '{self.gia_bia}' phải là số.")` |
| `gia_bia` | Là số thực/nguyên có giá trị **`>= 0`** | `ValueError("Giá bìa không được nhỏ hơn 0")` |
| `ma_the_loai` | Khác rỗng, không chứa toàn khoảng trắng | `ValueError("Mã thể loại không được để trống")` |