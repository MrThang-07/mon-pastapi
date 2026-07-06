from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Tuple
from datetime import datetime, timezone

app = FastAPI()

# ==========================================
# 1. DATABASE MÔ PHỎNG
# ==========================================
tasks_db = [
    {
        "id": 1, 
        "title": "Thiet ke database Shop AI", 
        "description": "Xay dung bang va toi uu index", 
        "assignee": "QuyDev", 
        "priority": 1, 
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z"
    },
    {
        "id": 2, 
        "title": "Code bo API Authen", 
        "description": "Trien khai filter verify JWT token", 
        "assignee": "FixerQ", 
        "priority": 2, 
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z"
    }
]

# ==========================================
# 2. CẤU TRÚC PHẢN HỒI & NGOẠI LỆ TÙY CHỈNH
# ==========================================
def unified_response(status_code: int, message: str, data: Any, error: Optional[str], path: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "message": message,
            "data": data,
            "error": error,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "path": path
        }
    )

class BusinessException(Exception):
    def __init__(self, status_code: int, message: str, error_code: str):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code

# ==========================================
# 3. GLOBAL EXCEPTION HANDLERS
# ==========================================
@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return unified_response(exc.status_code, exc.message, None, exc.error_code, request.url.path)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return unified_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "Lỗi: Dữ liệu đầu vào không hợp lệ hoặc sai định dạng quy định!",
        None,
        "ERR-VAL-422: Validation error at Request Body fields constraint layout.",
        request.url.path
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return unified_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Lỗi hệ thống nội bộ!",
        None,
        "ERR-SYS-500: Internal Server Error. Please contact admin.",
        request.url.path
    )

# ==========================================
# 4. PYDANTIC SCHEMAS (VALIDATION)
# ==========================================
class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=1)
    assignee: str = Field(..., min_length=1, json_schema_extra={"strip_whitespace": True})
    priority: int = Field(..., ge=1, le=5)

class TaskStatusUpdateSchema(BaseModel):
    status: str = Field(..., min_length=1)

# ==========================================
# 5. HÀM XỬ LÝ TOÁN HỌC ĐỘC LẬP (METRICS)
# ==========================================
def calculate_team_metrics() -> Tuple[int, int, float]:
    total_tasks = len(tasks_db)
    if total_tasks == 0:
        return (0, 0, 0.0)
    
    completed_tasks = sum(1 for task in tasks_db if task["status"] == "done")
    completion_rate_percentage = (completed_tasks / total_tasks) * 100
    
    return (total_tasks, completed_tasks, float(completion_rate_percentage))

# ==========================================
# 6. ENDPOINTS CHÍNH
# ==========================================

@app.get("/tasks")
async def get_all_tasks(request: Request, status_filter: Optional[str] = None):
    result = tasks_db
    if status_filter:
        result = [task for task in tasks_db if task["status"] == status_filter]
        
    return unified_response(
        status.HTTP_200_OK,
        "Lấy danh sách công việc thành công!",
        result,
        None,
        request.url.path
    )

@app.post("/tasks")
async def create_task(request: Request, task_in: TaskCreateSchema):
    # Kiểm tra trùng lặp tiêu đề
    for task in tasks_db:
        if task["title"] == task_in.title:
            raise BusinessException(
                status.HTTP_400_BAD_REQUEST,
                "Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!",
                "ERR-TASK-01: Task conflict: Title field duplicates an existing record."
            )
    
    new_id = max((task["id"] for task in tasks_db), default=0) + 1
    new_task = {
        "id": new_id,
        "title": task_in.title,
        "description": task_in.description,
        "assignee": task_in.assignee.strip(),
        "priority": task_in.priority,
        "status": "todo",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    tasks_db.append(new_task)
    
    return unified_response(
        status.HTTP_201_CREATED,
        "Khởi tạo công việc mới thành công!",
        new_task,
        None,
        request.url.path
    )

@app.put("/tasks/{task_id}")
async def update_task_status(request: Request, task_id: int, status_in: TaskStatusUpdateSchema):
    target_task = next((task for task in tasks_db if task["id"] == task_id), None)
    
    if not target_task:
        raise BusinessException(
            status.HTTP_404_NOT_FOUND,
            "Lỗi: Không tìm thấy công việc này trong hệ thống!",
            "ERR-TASK-03: Task not found."
        )
        
    if target_task["status"] == "done":
        raise BusinessException(
            status.HTTP_400_BAD_REQUEST,
            "Lỗi: Công việc đã hoàn thành, không thể cập nhật lùi trạng thái!",
            "ERR-TASK-04: Cannot update a completed task."
        )
        
    target_task["status"] = status_in.status
    
    return unified_response(
        status.HTTP_200_OK,
        "Cập nhật tiến độ công việc thành công!",
        target_task,
        None,
        request.url.path
    )

@app.get("/tasks/analytics/dashboard")
async def get_dashboard_analytics(request: Request):
    # Gọi hàm tính toán độc lập nhận Tuple
    total, completed, rate = calculate_team_metrics()
    
    data = {
        "total_tasks": total,
        "completed_tasks": completed,
        "completion_rate_percentage": rate
    }
    
    return unified_response(
        status.HTTP_200_OK,
        "Lấy số liệu thống kê hiệu suất nhóm thành công!",
        data,
        None,
        request.url.path
    )