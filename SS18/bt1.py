from fastapi import status

@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED  # Trả về HTTP 201 khi thành công
)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db)
):
    # 1. Tìm phòng ban
    department = (
        db.query(Department)
        .filter(Department.id == data.department_id)
        .first()
    )

    # Chặn lỗi 500: Trả 404 nếu không tìm thấy
    if department is None:
        raise HTTPException(status_code=404, detail="Phòng ban không tồn tại")

    # 2. Kiểm tra phòng ban có đang INACTIVE không
    if department.status == "INACTIVE":
        raise HTTPException(status_code=400, detail="Phòng ban đã ngừng hoạt động")

    # 3. Đếm số nhân viên hiện tại
    current_count = (
        db.query(Employee)
        .filter(Employee.department_id == data.department_id)
        .count()
    )
    
    # Chặn thêm mới nếu đã đủ hoặc vượt quota (dùng >= thay vì >)
    if current_count >= department.max_employees:
        raise HTTPException(status_code=400, detail="Phòng ban đã đủ nhân viên")

    # 4. Kiểm tra mã nhân viên bị trùng (kiểm tra trên toàn hệ thống)
    duplicate_employee = (
        db.query(Employee)
        .filter(Employee.employee_code == data.employee_code) 
        .first()
    )
    
    if duplicate_employee:
        raise HTTPException(status_code=400, detail="Mã nhân viên đã tồn tại")

    # 5. Lưu nhân viên mới
    employee = Employee(
        employee_code=data.employee_code,
        full_name=data.full_name,
        department_id=data.department_id
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)
    
    return employee