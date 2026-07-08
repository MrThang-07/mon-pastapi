from pydantic import BaseModel
class UsersRequestDTO(BaseModel):
    name: str
    email:str