from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CarrierCreate(BaseModel):
    code: str
    name: str
    max_weight_capacity: int
    status: str

class CarrierUpdate(BaseModel):
    code: str
    name: str
    max_weight_capacity: int
    status: str

class ShipmentCreate(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int
    dispatch_date: str
    shift: str

carriers = [
    {"id": 1, "code": "GHN", "name": "Giao Hang Nhanh", "max_weight_capacity": 5000, "status": "ACTIVE"},
    {"id": 2, "code": "GHTK", "name": "Giao Hang Tiet Kiem", "max_weight_capacity": 3000, "status": "ACTIVE"},
    {"id": 3, "code": "VTP", "name": "Viettel Post", "max_weight_capacity": 10000, "status": "SUSPENDED"}
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": "2026-07-01",
        "shift": "MORNING"
    }
]

@app.post("/carriers")
def create_carrier(carrier: CarrierCreate):
    if len(carrier.name) < 3:
        raise HTTPException(status_code=400, detail="Tên phải có ít nhất 3 ký tự")
        
    if carrier.max_weight_capacity <= 0:
        raise HTTPException(status_code=400, detail="Tải trọng phải lớn hơn 0")
        
    danh_sach_status = ["ACTIVE", "INACTIVE", "SUSPENDED"]
    if carrier.status not in danh_sach_status:
        raise HTTPException(status_code=400, detail="Status không hợp lệ")

    for c in carriers:
        if c["code"] == carrier.code:
            raise HTTPException(status_code=400, detail="Mã đối tác đã tồn tại")
    
    id_moi = 1
    if len(carriers) > 0:
        id_moi = carriers[-1]["id"] + 1
        
    new_carrier = {
        "id": id_moi,
        "code": carrier.code,
        "name": carrier.name,
        "max_weight_capacity": carrier.max_weight_capacity,
        "status": carrier.status
    }
    carriers.append(new_carrier)
    return new_carrier

@app.get("/carriers")
def get_carriers(keyword: str = None, status: str = None, min_weight: int = None):
    ket_qua = []
    
    for c in carriers:
        thoa_man = True
        
        if keyword != None:
            chuoi_tim_kiem = keyword.lower()
            if chuoi_tim_kiem not in c["code"].lower() and chuoi_tim_kiem not in c["name"].lower():
                thoa_man = False
                
        if status != None:
            if c["status"] != status:
                thoa_man = False
                
        if min_weight != None:
            if c["max_weight_capacity"] < min_weight:
                thoa_man = False
                
        if thoa_man == True:
            ket_qua.append(c)
            
    return ket_qua

@app.get("/carriers/{carrier_id}")
def get_carrier_by_id(carrier_id: int):
    for c in carriers:
        if c["id"] == carrier_id:
            return c
    raise HTTPException(status_code=404, detail="Carrier not found")

@app.put("/carriers/{carrier_id}")
def update_carrier(carrier_id: int, carrier_update: CarrierUpdate):
    for index in range(len(carriers)):
        if carriers[index]["id"] == carrier_id:
            carriers[index]["code"] = carrier_update.code
            carriers[index]["name"] = carrier_update.name
            carriers[index]["max_weight_capacity"] = carrier_update.max_weight_capacity
            carriers[index]["status"] = carrier_update.status
            return carriers[index]
            
    raise HTTPException(status_code=404, detail="Carrier not found")

@app.delete("/carriers/{carrier_id}")
def delete_carrier(carrier_id: int):
    for index in range(len(carriers)):
        if carriers[index]["id"] == carrier_id:
            carriers.pop(index)
            return {"message": "Đã xóa đối tác thành công!"}
    raise HTTPException(status_code=404, detail="Carrier not found")

@app.post("/shipments")
def create_shipment(shipment: ShipmentCreate):
    if shipment.total_weight <= 0:
        raise HTTPException(status_code=400, detail="Khối lượng phải lớn hơn 0")
        
    danh_sach_ca = ["MORNING", "AFTERNOON", "NIGHT"]
    if shipment.shift not in danh_sach_ca:
        raise HTTPException(status_code=400, detail="Ca làm việc không hợp lệ")

    doi_tac = None
    for c in carriers:
        if c["id"] == shipment.carrier_id:
            doi_tac = c
            break
            
    if doi_tac == None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đối tác vận chuyển.")
        
    if doi_tac["status"] != "ACTIVE":
        raise HTTPException(status_code=400, detail="Đối tác không ở trạng thái ACTIVE.")
        
    if shipment.total_weight > doi_tac["max_weight_capacity"]:
        raise HTTPException(status_code=400, detail="Khối lượng vượt quá tải trọng tối đa.")
        
    for s in shipments:
        if (s["carrier_id"] == shipment.carrier_id and 
            s["dispatch_date"] == shipment.dispatch_date and 
            s["shift"] == shipment.shift):
            raise HTTPException(status_code=400, detail="Đối tác đã có chuyến hàng vào ca và ngày này.")
            
    id_moi = 1
    if len(shipments) > 0:
        id_moi = shipments[-1]["id"] + 1
        
    new_shipment = {
        "id": id_moi,
        "carrier_id": shipment.carrier_id,
        "order_reference": shipment.order_reference,
        "total_weight": shipment.total_weight,
        "dispatch_date": shipment.dispatch_date,
        "shift": shipment.shift
    }
    shipments.append(new_shipment)
    return new_shipment

@app.get("/shipments")
def get_shipments():
    return shipments