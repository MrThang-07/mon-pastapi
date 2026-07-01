from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# CƠ SỞ DỮ LIỆU GIẢ LẬP
products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]

# Pydantic Model để nhận và kiểm soát dữ liệu đầu vào
class ProductUpdate(BaseModel):
    code: str
    name: str
    price: float
    stock: int


# ==============================================================================
# PHẦN 1: PHÂN TÍCH & ĐỀ XUẤT ĐA GIẢI PHÁP
#
# 1. Phân tích Input/Output:
#    - Input: Path Parameter `product_id` (int) và Request Body (JSON) gồm:
#             code (str), name (str), price (float), stock (int).
#    - Output thành công: Trả về thông tin sản phẩm sau khi cập nhật (HTTP 200 OK).
#    - Output thất bại: Trả về lỗi HTTPException (400 hoặc 404) kèm lý do chi tiết 
#                       (Không tìm thấy sản phẩm, Trùng mã code, Giá trị âm...).
#
# 2. Đề xuất 2 giải pháp xử lý dữ liệu:
#    - Giải pháp 1 (Duyệt List): Dùng vòng lặp `for` quét qua từng item trong mảng `products`
#                  để tìm `product_id` trùng khớp. Ưu điểm là dữ liệu giữ nguyên dạng mảng,
#                  gần gũi với mảng JSON gốc.
#    - Giải pháp 2 (Dùng Dict): Chuyển đổi cấu trúc danh sách thành Dictionary với Key là 
#                  `id` của sản phẩm. Khi cập nhật chỉ cần truy xuất trực tiếp qua `dict[product_id]`.
# ==============================================================================


# ==============================================================================
# PHẦN 2: SO SÁNH & LỰA CHỌN GIẢI PHÁP
#
# | Tiêu chí          | Giải pháp 1: Duyệt list          | Giải pháp 2: Dùng dict           |
# |-------------------|----------------------------------|----------------------------------|
# | Tốc độ tìm kiếm   | Chậm (Phải quét tuần tự O(n))    | Rất nhanh (Truy xuất trực tiếp O(1))|
# | Bộ nhớ            | Tiết kiệm, giữ nguyên dữ liệu    | Tốn thêm bộ nhớ để map lại key   |
# | Dễ hiểu           | Rất dễ hiểu, trực quan cho người mới| Phức tạp hơn ở bước cấu trúc dữ liệu|
# | Dễ bảo trì        | Trung bình                       | Cao khi hệ thống mở rộng dữ liệu |
# | Bối cảnh phù hợp  | Dữ liệu ít, danh sách nhỏ        | Dữ liệu lớn, tần suất đọc ghi cao|
#
# KẾT LUẬN LỰA CHỌN: Do phạm vi bài học quản lý danh sách sản phẩm nhỏ (In-memory list),
# giải pháp 1 (Duyệt List) được ưu tiên lựa chọn vì giữ code ngắn gọn, dễ kiểm soát logic.
# ==============================================================================


# ==============================================================================
# PHẦN 3: TRIỂN KHAI CODE (Giải pháp Duyệt List tối giản)
# ==============================================================================
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_data: ProductUpdate):
    
    # --- BƯỚC 1: KIỂM TRA TÍNH HỢP LỆ CỦA DỮ LIỆU ĐẦU VÀO (RÀNG BUỘC NGHIỆP VỤ) ---
    if not updated_data.name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name cannot be empty")
        
    if updated_data.price <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price must be greater than 0")
        
    if updated_data.stock < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock must be greater than or equal to 0")

    # --- BƯỚC 2: TÌM SẢN PHẨM CẦN SỬA (BẪY 1: SẢN PHẨM KHÔNG TỒN TẠI) ---
    target_product = None
    for p in products:
        if p.get("id") == product_id:
            target_product = p
            break
            
    if not target_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # --- BƯỚC 3 (BẪY 2): KIỂM TRA MÃ SẢN PHẨM BỊ TRÙNG VỚI SẢN PHẨM KHÁC ---
    for p in products:
        # Nếu mã 'code' trùng với một sản phẩm trong hệ thống, NHƯNG đó phải là sản phẩm khác (id khác nhau)
        if p.get("code") == updated_data.code and p.get("id") != product_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Product code already exists"
            )

    # --- BƯỚC 4: GHI ĐÈ/CẬP NHẬT DỮ LIỆU MỚI KHI HỢP LỆ ---
    target_product["code"] = updated_data.code
    target_product["name"] = updated_data.name
    target_product["price"] = updated_data.price
    target_product["stock"] = updated_data.stock

    # Trả về kết quả sau cập nhật thành công (Mặc định mã 200 OK)
    return {
        "message": "Update product successfully",
        "data": target_product
    }