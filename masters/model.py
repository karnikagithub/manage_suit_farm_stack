from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class Group(BaseModel):
    group_name: str


class SuperCategory(BaseModel):
    super_category_name: str
    group_id: Optional[str]


class CategoryMaster(BaseModel):
    category_name: str
    super_category_id: Optional[str]


class DepartmentMaster(BaseModel):
    department_name: str


class LocationMaster(BaseModel):
    location_name: str


class ItemMaster(BaseModel):
    item_name: str
    item_code: str
    item_specification: str
    group_id: Optional[str]
    super_category_id: Optional[str]
