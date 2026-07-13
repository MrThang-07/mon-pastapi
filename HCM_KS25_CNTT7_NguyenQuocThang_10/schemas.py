from typing import Optional
from pydantic import BaseModel
class table_employees(BaseModel):
    id : Optional[int] = None
    full_name : str
    department :str
    position :str
    salary : float