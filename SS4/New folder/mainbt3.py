# ==========================================
# PHẦN 1: BÁO CÁO PHÂN TÍCH
# ==========================================
# 1. Input của bài toán:
#    - keyword (kiểu str): Từ khóa tìm tên sản phẩm (không bắt buộc).
#    - max_price (kiểu float): Mức giá tối đa để lọc (không bắt buộc).
#    - Dữ liệu gốc: Danh sách `products` chứa các sản phẩm.
#
# 2. Output mong muốn:
#    - Một danh sách chứa các sản phẩm thỏa mãn điều kiện lọc.
#    - Nếu max_price < 0: Trả về thông báo lỗi {"detail": "max_price không được âm"}.
#
# 3. Đề xuất giải pháp & Các bước xử lý (Cực kỳ cơ bản):
#    - Bước 1: Kiểm tra lỗi âm trước. Nếu `max_price < 0` thì trả về lỗi luôn.
#    - Bước 2: Tạo một danh sách rỗng tên là `filtered_products` để chứa kết quả.
#    - Bước 3: Dùng vòng lặp `for` duyệt qua từng sản phẩm trong danh sách gốc.
#    - Bước 4: Kiểm tra điều kiện bằng `if`:
#              + Nếu có truyền keyword -> Tên sản phẩm phải chứa keyword (dùng chữ thường .lower()).
#              + Nếu có truyền max_price -> Giá sản phẩm phải nhỏ hơn hoặc bằng max_price.
#    - Bước 5: Nếu thỏa mãn thì `append` (thêm) sản phẩm đó vào danh sách kết quả và trả về.
# ==========================================

from fastapi import FastAPI

app = FastAPI()

# Dữ liệu danh sách sản phẩm mẫu
products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000}
]

# PHẦN 2: TRIỂN KHAI CODE (BẢN ĐƠN GIẢN)
@app.get("/products")
def get_products(keyword: str = None, max_price: float = None):
    # 1. Bẫy dữ liệu: Nếu người dùng truyền giá âm, báo lỗi ngay lập tức
    if max_price is not None and max_price < 0:
        return {"detail": "max_price không được âm"}

    # 2. Tạo một list rỗng để gom các sản phẩm thỏa mãn điều kiện
    filtered_products = []
    
    # 3. Duyệt qua từng sản phẩm trong danh sách gốc
    for product in products:
        
        # Tình huống 1: Người dùng truyền CẢ keyword VÀ max_price
        if keyword is not None and max_price is not None:
            if keyword.lower() in product["name"].lower() and product["price"] <= max_price:
                filtered_products.append(product)
                
        # Tình huống 2: Người dùng CHỈ truyền mỗi keyword
        elif keyword is not None:
            if keyword.lower() in product["name"].lower():
                filtered_products.append(product)
                
        # Tình huống 3: Người dùng CHỈ truyền mỗi max_price
        elif max_price is not None:
            if product["price"] <= max_price:
                filtered_products.append(product)
                
        # Tình huống 4: Không truyền gì cả -> Lấy hết sản phẩm
        else:
            filtered_products.append(product)
            
    # 4. Trả về kết quả sau khi lọc
    return filtered_products