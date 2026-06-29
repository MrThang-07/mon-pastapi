from fastapi import FastAPI

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Lê Minh Thu",
        "category": "programming",
        "year": 2022,
        "is_available": True
    },
    {
        "id": 2,
        "title": "Web API Design",
        "author": "Phạm Lan Hồng",
        "category": "web",
        "year": 2021,
        "is_available": False
    },
    {
        "id": 3,
        "title": "Database System",
        "author": "Lê Minh Huyền",
        "category": "database",
        "year": 2020,
        "is_available": True
    },
    {
        "id": 4,
        "title": "Clean Code",
        "author": "Lê Ánh Linh",
        "category": "programming",
        "year": 2008,
        "is_available": False
    },
    {
        "id": 5,
        "title": "Computer Network",
        "author": "Vũ Hồng Vân",
        "category": "network",
        "year": 2019,
        "is_available": True
    }
]

@app.get("/books/statistics")
def get_books_statistics():
    total_books = len(books)
    available_books = 0
    borrowed_books = 0
    
    for book in books:
        if book["is_available"] == True:
            available_books = available_books + 1
        else:
            borrowed_books = borrowed_books + 1
            
    return {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books
    }

@app.get("/books/categories")
def get_books_categories():
    unique_categories = []
    
    for book in books:
        # Nếu thể loại này chưa có trong danh sách kết quả thì mới thêm vào
        if book["category"] not in unique_categories:
            unique_categories.append(book["category"])
            
    return {"categories": unique_categories}

@app.get("/books/latest")
def get_latest_book():
    if len(books) == 0:
        return {"message": "No books available"}
        
    # Giả định cuốn sách đầu tiên là cuốn mới nhất
    latest_book = books[0]
    
    for book in books:
        # Nếu tìm thấy cuốn nào có năm lớn hơn cuốn đang giữ, thì đổi ngôi
        if book["year"] > latest_book["year"]:
            latest_book = book
            
    return latest_book