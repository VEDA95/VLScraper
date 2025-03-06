from pydantic import BaseModel
from typing import Union

class CompanyNode(BaseModel):
    name: str
    industry: str

class QueueNode(BaseModel):
    company: CompanyNode
    data: Union[bytes, None]