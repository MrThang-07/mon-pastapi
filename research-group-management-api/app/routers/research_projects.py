from fastapi import APIRouter, Depends, status , HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import List , Optional
# Import Models
from app.models.research_project import ResearchProject, ResearchMember
from app.models.user import User
from app.schemas.research_project import ResearchProjectUpdate
from app.schemas.research_project import ResearchMemberAdd, ResearchMemberResponse
from app.schemas.research_project import ResearchProjectCreate, ResearchProjectResponse

from app.dependencies.auth import get_current_user 
from app.utils.logger import log_activity
router = APIRouter(
    prefix="/research-projects",
    tags=["Research Projects"]
)
# Tạo đề tài nghiên cứu
@router.post("/", response_model=ResearchProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ResearchProjectCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    """
    API Tạo đề tài nghiên cứu:
    - Bắt buộc đăng nhập.
    - User tạo đề tài sẽ tự động trở thành OWNER.
    """
    
    # 1. Lưu thông tin đề tài vào DB
    new_project = ResearchProject(
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id  
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project) 

    # 2. Tự động cấp quyền OWNER trong bảng trung gian (ResearchMember)
    new_member = ResearchMember(
        project_id=new_project.id,
        user_id=current_user.id,
        role="OWNER" 
    )
    db.add(new_member)
    db.commit()

    # Ghi log hoạt động tạo đề tài
    log_activity(
        db=db,
        user_id=current_user.id,
        action="CREATE_PROJECT",
        description=f"Đã tạo đề tài nghiên cứu: '{new_project.name}' (ID: {new_project.id})"
    )

    return new_project

# API trả về đề tài nghiên cứu của owner / member
@router.get("/", response_model=List[ResearchProjectResponse], status_code=status.HTTP_200_OK)
def get_projects(
    search: Optional[str] = None, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    API Lấy danh sách đề tài:
    - Chỉ lấy những đề tài mà current_user có tham gia (là OWNER hoặc MEMBER).
    - Có hỗ trợ tìm kiếm theo tên đề tài.
    """
    
    # Bước 1: Tìm tất cả các Đề tài mà User này có mặt trong bảng trung gian (ResearchMember)
    query = db.query(ResearchProject).join(ResearchMember).filter(
        ResearchMember.user_id == current_user.id
    )

    # Bước 2: Xử lý chức năng Search (Nếu người dùng có nhập từ khóa tìm kiếm)
    if search:
        # ilike giúp tìm kiếm không phân biệt hoa thường (VD: gõ "AI" thì ra cả "ai", "Ai")
        query = query.filter(ResearchProject.name.ilike(f"%{search}%"))

    # Bước 3: Lấy toàn bộ kết quả sau khi đã lọc
    projects = query.all()

    return projects


# api xem chi tiết đề tài nghiên cứu chỉ thành viên mới xem dc 
@router.get("/{project_id}", response_model=ResearchProjectResponse, status_code=status.HTTP_200_OK)
def get_project_detail(
    project_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Bắt buộc đăng nhập
):
    """
    API Lấy chi tiết đề tài:
    - Tìm đề tài theo ID.
    - Chặn đứng nếu người dùng không phải là thành viên của đề tài này.
    """
    
    # Tìm đề tài trong kho (Database)
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Không tìm thấy đề tài nghiên cứu này!"
        )

    
    is_member = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Bạn không có quyền xem đề tài này vì không phải là thành viên!"
        )

    return project

# API  CẬP NHẬT ĐỀ TÀI (Chỉ OWNER được sửa)

@router.put("/{project_id}", response_model=ResearchProjectResponse)
def update_project(
    project_id: int,
    project_data: ResearchProjectUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Bước 1: Tìm đề tài xem có tồn tại không
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Không tìm thấy đề tài!")

    # Bước 2: Kiểm tra chức danh của user hiện tại trong đề tài này
    member_info = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == current_user.id
    ).first()

    # Nếu không tham gia nhóm, HOẶC tham gia nhưng không phải Trưởng nhóm (OWNER) -> Báo lỗi ngay
    if not member_info or member_info.role != "OWNER":
        raise HTTPException(
            status_code=403, 
            detail="Bạn không có quyền! Chỉ Trưởng nhóm (OWNER) mới được phép sửa."
        )

    # Bước 3: Cập nhật dữ liệu
    if project_data.name is not None:
        project.name = project_data.name
        
    if project_data.description is not None:
        project.description = project_data.description

    db.commit()
    db.refresh(project)
    
    # Ghi log hoạt động sửa đề tài
    log_activity(
        db=db,
        user_id=current_user.id,
        action="UPDATE_PROJECT",
        description=f"Đã cập nhật đề tài nghiên cứu ID: {project_id}"
    )
    
    return project


# API XÓA ĐỀ TÀI (Chỉ OWNER được xóa)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Bước 1: Tìm đề tài
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Không tìm thấy đề tài!")

    # Bước 2: Kiểm tra chức danh 
    member_info = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == current_user.id
    ).first()

    if not member_info or member_info.role != "OWNER":
        raise HTTPException(
            status_code=403, 
            detail="Bạn không có quyền! Chỉ Trưởng nhóm (OWNER) mới được phép xóa."
        )

    # Bước 3: Tiến hành xóa 

    # Xóa toàn bộ dòng trong bảng Member có chứa project_id này
    db.query(ResearchMember).filter(ResearchMember.project_id == project_id).delete()

    db.delete(project)
    db.commit()
    
    # Ghi log hoạt động xóa đề tài
    log_activity(
        db=db,
        user_id=current_user.id,
        action="DELETE_PROJECT",
        description=f"Đã xóa đề tài nghiên cứu ID: {project_id}"
    )
    
    return 

# ==========================================
# API THÊM THÀNH VIÊN VÀO NHÓM (Chỉ OWNER)
# ==========================================
@router.post("/{project_id}/members", status_code=status.HTTP_201_CREATED)
def add_member(
    project_id: int,
    member_data: ResearchMemberAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Bước 1: Kiểm tra xem người đang thao tác có phải là OWNER không
    is_owner = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == current_user.id,
        ResearchMember.role == "OWNER"
    ).first()

    if not is_owner:
        raise HTTPException(
            status_code=403, 
            detail="Bạn không có quyền! Chỉ Trưởng nhóm mới được thêm thành viên."
        )

    # Bước 2: Kiểm tra xem người được mời có tồn tại không
    user_to_add = db.query(User).filter(User.id == member_data.user_id).first()
    if not user_to_add:
        raise HTTPException(status_code=404, detail="Người dùng này không tồn tại trong hệ thống!")

    # Bước 3: Chống thêm trùng
    existing_member = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == member_data.user_id
    ).first()

    if existing_member:
        raise HTTPException(status_code=400, detail="Người này đã là thành viên của nhóm rồi!")

    # Bước 4: Thêm vào nhóm với vai trò MEMBER
    new_member = ResearchMember(
        project_id=project_id,
        user_id=member_data.user_id,
        role="MEMBER" 
    )
    db.add(new_member)
    db.commit()

    # Ghi log hoạt động thêm thành viên
    log_activity(
        db=db,
        user_id=current_user.id,
        action="ADD_MEMBER",
        description=f"Đã thêm user_id {member_data.user_id} vào đề tài ID: {project_id}"
    )

    return {"message": f"Đã thêm thành viên vào nhóm thành công!"}


# API XÓA THÀNH VIÊN KHỎI NHÓM (Chỉ OWNER)

@router.delete("/{project_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(
    project_id: int,
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Kiểm tra người bấm nút Xóa có phải là OWNER không?
    is_owner = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == current_user.id,
        ResearchMember.role == "OWNER"
    ).first()

    if not is_owner:
        raise HTTPException(
            status_code=403, 
            detail="Bạn không có quyền! Chỉ Trưởng nhóm mới được xóa thành viên."
        )

    # Tìm thẻ thành viên của người sắp bị xóa
    member_to_remove = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == user_id
    ).first()

    if not member_to_remove:
        raise HTTPException(status_code=404, detail="Người này không có trong nhóm!")

    # Không được xóa OWNER cuối cùng
    if member_to_remove.role == "OWNER":
        owner_count = db.query(ResearchMember).filter(
            ResearchMember.project_id == project_id,
            ResearchMember.role == "OWNER"
        ).count()
        
        if owner_count <= 1:
            raise HTTPException(
                status_code=400, 
                detail="Không thể xóa Trưởng nhóm cuối cùng của dự án!"
            )

    db.delete(member_to_remove)
    db.commit()
    
    # Ghi log hoạt động xóa thành viên
    log_activity(
        db=db,
        user_id=current_user.id,
        action="REMOVE_MEMBER",
        description=f"Đã xóa user_id {user_id} khỏi đề tài ID: {project_id}"
    )
    
    return


# API XEM DANH SÁCH THÀNH VIÊN
@router.get("/{project_id}/members", response_model=List[ResearchMemberResponse])
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    is_member = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Bạn không có quyền! Chỉ thành viên mới được xem danh sách này."
        )

    # Lấy toàn bộ danh sách thành viên trả về
    members = db.query(ResearchMember).filter(ResearchMember.project_id == project_id).all()
    return members