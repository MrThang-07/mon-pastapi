raw_product = [
    {"sku": "SP001", "name": "Áo thun livestream", "price": 250000, "stock": 50, "status": "active"}, 
    {"sku": " sp002 ", "name": "Quần jean", "price": 450000, "stock": 30, "status": "active"}, 
    {"sku": "SP003", "name": "Giày thể thao", "price": 1200000, "stock": 20, "status": "inactive"}, 
    {"sku": "SP004", "name": "Váy công sở", "price": 680000, "stock": 15, "status": "sold_out"}, 
    {"sku": "SP005", "name": "Kính mát", "price": 350000, "stock": 45, "status": "active"} 
]

def clean_and_validate_products():
    for i in raw_product:
        i["sku"] = i["sku"].strip().upper()
        print(i)
    
def sort_products_by_stock_asc(products):
    sort = products.copy()
    n = len(sort)
    for i in range(n -1):
        for j in range(n - i - 1):
            if sort[j]["stock"] > sort[j + 1]["stock"]:
                sort[j],sort[j + 1] = sort[j + 1],sort[j]
    print(sort)

                

clean_and_validate_products()
print("------------------------------------------------------------------------")
sort_products_by_stock_asc(raw_product)