from pydantic import BaseModel
from typing import Optional

class table_team(BaseModel):
    id : Optional[int] = None
    country_name :str
    coach_name : str
    group_name : str

    class Config:
        from_attributes = True