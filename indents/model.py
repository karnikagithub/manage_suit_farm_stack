from pydantic import BaseModel
from typing import Optional, List


class ItemDetails(BaseModel):
    item_name: str
    quantity: int
    updated_quantity: int
    status: int

class IndentDetails(BaseModel):
    indent_purpose: str
    indent_remarks: str
    indent_code: Optional[str]
    department_id: Optional[str]
    location_id: Optional[str]
    indentitems: List[ItemDetails]
    status: int

    
# class IndentDetailsView(BaseModel):
#     indent_details = List[IndentDetails]
