from pydantic import BaseModel
# model base dung chung , muon dung cho nhung khac tinh nang khac thi phai ke thua roi viet lai
class StudentBase(BaseModel):
    name : str
    age : int
    department_id : int
class StudentCreateDTO(StudentBase):
    pass
class StudentPutDTO(StudentBase):
    pass

class StudentResponse(StudentBase):
    id : int

    class Config:
        from_attributes = True

