import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class AssetCreate(BaseModel):
    serial_number: str
    model: str
    stock_available: int
    status: str

class AssetUpdate(BaseModel):
    serial_number: str
    model: str
    stock_available: int
    status: str

class AllocationCreate(BaseModel):
    asset_id: int
    employee_email: str
    allocated_quantity: int
    start_date: str
    duration_months: int

assets = [
    {"id": 1, "serial_number": "SN-MAC-01", "model": "MacBook Pro M3", "stock_available": 5, "status": "READY"},
    {"id": 2, "serial_number": "SN-DELL-02", "model": "Dell UltraSharp 27", "stock_available": 10, "status": "READY"},
    {"id": 3, "serial_number": "SN-THINK-03", "model": "ThinkPad X1 Carbon", "stock_available": 0, "status": "REPAIRING"}
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12
    }
]

@app.post("/assets")
def create_asset(asset: AssetCreate):
    for a in assets:
        if a["serial_number"] == asset.serial_number:
            raise HTTPException(status_code=400, detail="Mã serial_number đã tồn tại")

    if len(asset.model) < 2 or len(asset.model) > 255:
        raise HTTPException(status_code=400, detail="Model phải từ 2 đến 255 ký tự")

    if asset.stock_available < 0:
        raise HTTPException(status_code=400, detail="Số lượng tồn kho phải lớn hơn hoặc bằng 0")

    danh_sach_status = ["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]
    if asset.status not in danh_sach_status:
        raise HTTPException(status_code=400, detail="Trạng thái không hợp lệ")

    id_moi = 1
    if len(assets) > 0:
        id_moi = assets[-1]["id"] + 1

    new_asset = {
        "id": id_moi,
        "serial_number": asset.serial_number,
        "model": asset.model,
        "stock_available": asset.stock_available,
        "status": asset.status
    }
    assets.append(new_asset)
    return new_asset

@app.get("/assets")
def get_assets(keyword: str = None, status: str = None, min_stock: int = None):
    ket_qua = []
    
    for a in assets:
        thoa_man = True
        
        if keyword != None:
            chuoi_tim_kiem = keyword.lower()
            if chuoi_tim_kiem not in a["serial_number"].lower() and chuoi_tim_kiem not in a["model"].lower():
                thoa_man = False
                
        if status != None:
            if a["status"] != status:
                thoa_man = False
                
        if min_stock != None:
            if a["stock_available"] < min_stock:
                thoa_man = False
                
        if thoa_man == True:
            ket_qua.append(a)
            
    return ket_qua

@app.get("/assets/{asset_id}")
def get_asset_by_id(asset_id: int):
    for a in assets:
        if a["id"] == asset_id:
            return a
    raise HTTPException(status_code=404, detail="Asset not found")

@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, asset_update: AssetUpdate):
    for index in range(len(assets)):
        if assets[index]["id"] == asset_id:
            for temp_a in assets:
                if temp_a["serial_number"] == asset_update.serial_number and temp_a["id"] != asset_id:
                    raise HTTPException(status_code=400, detail="Mã serial_number đã tồn tại ở thiết bị khác")

            if len(asset_update.model) < 2 or len(asset_update.model) > 255:
                raise HTTPException(status_code=400, detail="Model phải từ 2 đến 255 ký tự")

            if asset_update.stock_available < 0:
                raise HTTPException(status_code=400, detail="Số lượng tồn kho phải lớn hơn hoặc bằng 0")

            danh_sach_status = ["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]
            if asset_update.status not in danh_sach_status:
                raise HTTPException(status_code=400, detail="Trạng thái không hợp lệ")

            assets[index]["serial_number"] = asset_update.serial_number
            assets[index]["model"] = asset_update.model
            assets[index]["stock_available"] = asset_update.stock_available
            assets[index]["status"] = asset_update.status
            return assets[index]

    raise HTTPException(status_code=404, detail="Asset not found")

@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int):
    for index in range(len(assets)):
        if assets[index]["id"] == asset_id:
            assets.pop(index)
            return {"message": "Đã xóa tài sản thiết bị thành công!"}
    raise HTTPException(status_code=404, detail="Asset not found")

@app.post("/allocations")
def create_allocation(allocation: AllocationCreate):
    if allocation.allocated_quantity <= 0:
        raise HTTPException(status_code=400, detail="Số lượng cấp phát phải lớn hơn 0")

    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_pattern, allocation.employee_email):
        raise HTTPException(status_code=400, detail="Định dạng email không hợp lệ")

    if allocation.duration_months < 1 or allocation.duration_months > 12:
        raise HTTPException(status_code=400, detail="Thời gian mượn phải từ 1 đến 12 tháng")

    tai_san = None
    for a in assets:
        if a["id"] == allocation.asset_id:
            tai_san = a
            break

    if tai_san == None:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài sản thiết bị")

    if tai_san["status"] != "READY":
        raise HTTPException(status_code=400, detail="Thiết bị không ở trạng thái READY để cấp phát")

    if allocation.allocated_quantity > tai_san["stock_available"]:
        raise HTTPException(status_code=400, detail="Số lượng yêu cầu vượt quá số lượng tồn kho khả dụng")

    id_moi = 1
    if len(allocations) > 0:
        id_moi = allocations[-1]["id"] + 1

    new_allocation = {
        "id": id_moi,
        "asset_id": allocation.asset_id,
        "employee_email": allocation.employee_email,
        "allocated_quantity": allocation.allocated_quantity,
        "start_date": allocation.start_date,
        "duration_months": allocation.duration_months
    }
    
    # Giảm số lượng tồn kho của thiết bị sau khi cấp phát thành công
    tai_san["stock_available"] -= allocation.allocated_quantity
    
    allocations.append(new_allocation)
    return new_allocation

@app.get("/allocations")
def get_allocations():
    return allocations