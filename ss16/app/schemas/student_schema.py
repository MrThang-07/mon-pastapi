from pydantic import BaseModel
class StudentCreateDTO(BaseModel):
    name : str
    age : int