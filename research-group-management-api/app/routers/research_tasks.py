from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.models.research_task import ResearchTask
from app.models.research_project import ResearchProject, ResearchMember
from app.models.user import User
from app.schemas.research_task import (
    ResearchTaskCreate, 
    ResearchTaskResponse, 
    ResearchTaskUpdate,
    TaskStatus,
    TaskPriority
)
from app.dependencies.auth import get_current_user

router = APIRouter(
    tags=["Research Tasks"]
)

# ==========================================
# 1. API TẠO NHIỆM VỤ NGHIÊN CỨU
# ==========================================
@router.post("/research-projects/{project_id}/research-tasks", response_model=ResearchTaskResponse, status_code=status.HTTP_201_CREATED)
def create_research_task(
    project_id: int,
    task_data: ResearchTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Tạo nhiệm vụ mới trong một đề tài:
    - Bắt buộc phải là thành viên của đề tài mới được tạo.
    """
    # Bước 1: Kiểm tra đề tài có tồn tại không
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Không tìm thấy đề tài nghiên cứu!")

    # Bước 2: Kiểm tra current_user có phải là thành viên của đề tài không?
    is_member = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=403, 
            detail="Bạn không có quyền! Chỉ thành viên nhóm mới được tạo nhiệm vụ."
        )

    # Bước 3: Tạo task mới
    new_task = ResearchTask(
        project_id=project_id,
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        priority=task_data.priority,  
        status=task_data.status      
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# ==========================================
# 2. API LẤY DANH SÁCH NHIỆM VỤ (Đã nâng cấp Search, Filter, Sort, Pagination)
# ==========================================
@router.get("/research-projects/{project_id}/research-tasks", response_model=List[ResearchTaskResponse])
def get_research_tasks(
    project_id: int,
    # --- CÁC THAM SỐ TÌM KIẾM & LỌC ---
    search: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee_id: Optional[int] = None,
    # --- CÁC THAM SỐ SẮP XẾP ---
    sort_by: str = Query("created_at", description="Nhập 'created_at' hoặc 'due_date'"),
    order: str = Query("desc", description="Nhập 'desc' (mới nhất) hoặc 'asc' (cũ nhất)"),
    # --- CÁC THAM SỐ PHÂN TRANG ---
    page: int = Query(1, ge=1, description="Số trang (bắt đầu từ 1)"),
    size: int = Query(10, ge=1, le=100, description="Số lượng task trên 1 trang"),
    # --- CÁC DEPENDENCIES ---
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy danh sách nhiệm vụ của 1 đề tài:
    - Hỗ trợ Filter (status, priority, assignee_id), Search (title).
    - Hỗ trợ Sort (created_at, due_date) và Phân trang (page, size).
    """
    # 1. Check quyền truy cập (Phải là thành viên mới cho xem)
    is_member = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=403, 
            detail="Bạn không có quyền xem danh sách nhiệm vụ của đề tài này!"
        )

    # 2. Khởi tạo câu truy vấn cơ bản (Lấy task của project hiện tại)
    query = db.query(ResearchTask).filter(ResearchTask.project_id == project_id)

    # 3. XỬ LÝ SEARCH & FILTER (Nếu người dùng có truyền lên)
    if search:
        query = query.filter(ResearchTask.title.ilike(f"%{search}%"))
    if status:
        query = query.filter(ResearchTask.status == status.value)
    if priority:
        query = query.filter(ResearchTask.priority == priority.value)
    if assignee_id:
        query = query.filter(ResearchTask.assignee_id == assignee_id)

    # 4. XỬ LÝ SORT (Sắp xếp)
    if sort_by == "due_date":
        if order == "asc":
            query = query.order_by(ResearchTask.due_date.asc())
        else:
            query = query.order_by(ResearchTask.due_date.desc())
    else: # Mặc định là sắp xếp theo created_at
        if order == "asc":
            query = query.order_by(ResearchTask.created_at.asc())
        else:
            query = query.order_by(ResearchTask.created_at.desc())

    # 5. XỬ LÝ PAGINATION (Phân trang)
    offset = (page - 1) * size
    tasks = query.offset(offset).limit(size).all()
    
    return tasks


# ==========================================
# 3. API XEM CHI TIẾT NHIỆM VỤ (GET)
# ==========================================
@router.get("/research-tasks/{task_id}", response_model=ResearchTaskResponse)
def get_task_detail(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Xem chi tiết 1 nhiệm vụ:
    - Bắt buộc user đang xem phải là thành viên của đề tài chứa task này.
    """
    # 1. Tìm task
    task = db.query(ResearchTask).filter(ResearchTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhiệm vụ!")

    # 2. Kiểm tra quyền (phải là thành viên của project chứa task)
    is_member = db.query(ResearchMember).filter(
        ResearchMember.project_id == task.project_id,
        ResearchMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xem nhiệm vụ của nhóm khác!")

    return task


# ==========================================
# 4. API CẬP NHẬT & GIAO VIỆC (PATCH)
# ==========================================
@router.patch("/research-tasks/{task_id}", response_model=ResearchTaskResponse)
def update_task(
    task_id: int,
    task_data: ResearchTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cập nhật nhiệm vụ (Có thể dùng để Giao việc - Assign):
    - Chỉ cập nhật những trường gửi lên.
    - Nếu có giao việc (assignee_id), bắt buộc người đó phải trong nhóm.
    """
    # 1. Tìm task
    task = db.query(ResearchTask).filter(ResearchTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhiệm vụ!")

    # 2. Kiểm tra quyền của người đang thao tác
    is_member = db.query(ResearchMember).filter(
        ResearchMember.project_id == task.project_id,
        ResearchMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(status_code=403, detail="Bạn không có quyền sửa nhiệm vụ này!")

    # 3. LOGIC GIAO VIỆC: Nếu có gửi lên assignee_id thì phải kiểm tra
    if task_data.assignee_id is not None:
        is_assignee_in_group = db.query(ResearchMember).filter(
            ResearchMember.project_id == task.project_id,
            ResearchMember.user_id == task_data.assignee_id
        ).first()
        
        if not is_assignee_in_group:
            raise HTTPException(
                status_code=400, 
                detail="Lỗi giao việc: Người được giao không phải là thành viên của đề tài này!"
            )

    # 4. Cập nhật dữ liệu 
    if task_data.title is not None:
        task.title = task_data.title
        
    if task_data.description is not None:
        task.description = task_data.description
        
    if task_data.assignee_id is not None:
        task.assignee_id = task_data.assignee_id
        
    if task_data.due_date is not None:
        task.due_date = task_data.due_date

    if task_data.status is not None:
        task.status = task_data.status.value
        
    if task_data.priority is not None:
        task.priority = task_data.priority.value

    db.commit()
    db.refresh(task)
    return task


# ==========================================
# 5. API XÓA NHIỆM VỤ (DELETE)
# ==========================================
@router.delete("/research-tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Xóa nhiệm vụ:
    - Áp dụng Permission: Chỉ Trưởng nhóm (OWNER) mới được phép xóa task.
    """
    task = db.query(ResearchTask).filter(ResearchTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhiệm vụ!")


    is_owner = db.query(ResearchMember).filter(
        ResearchMember.project_id == task.project_id,
        ResearchMember.user_id == current_user.id,
        ResearchMember.role == "OWNER"
    ).first()

    if not is_owner:
        raise HTTPException(status_code=403, detail="Bạn không có quyền! Chỉ Trưởng nhóm mới được xóa nhiệm vụ.")

    # 3. Tiến hành xóa
    db.delete(task)
    db.commit()
    return