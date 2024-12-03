from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi import HTTPException
from .model import *
from pymongo import MongoClient
from settings import mongo_client
import os
from bson import ObjectId

masters_router = APIRouter()

db = os.getenv('MONGO_DB')



@masters_router.post("/create_group/",response_model=Group)
async def create_group(group_data:Group):
    group_collect = mongo_client(db,"group_master")

    if group_collect.find_one({"group_name":group_data.group_name}):
        raise HTTPException(status_code=400,detail="Group already exists")
    
    # result = group_collect.insert_one({"_id":result.inserted_id})
    result = group_collect.insert_one(group_data.dict())
    created_group = group_collect.find_one({"_id": result.inserted_id})


    return created_group



# Endpoint to create a new super category
@masters_router.post("/create_super_category/", response_model=SuperCategory)
async def create_super_category(super_category_data: SuperCategory):
    sup_cat_collect = mongo_client(db, "super_category_master")
    group_collect = mongo_client(db, "group_master")

    # Checking if the Super Category already exists
    if sup_cat_collect.find_one({"super_category_name": super_category_data.super_category_name}):
        raise HTTPException(status_code=400, detail="Super Category already exists")

    # If a group_id is provided, check if the referenced Group exists
    if super_category_data.group_id and not group_collect.find_one({"_id": ObjectId(super_category_data.group_id)}):
        raise HTTPException(status_code=400, detail="Invalid group_id, Group does not exist")

    # Inserting the new Super Category
    result = sup_cat_collect.insert_one(super_category_data.dict())
    created_sup_cat = sup_cat_collect.find_one({"_id": result.inserted_id})

    return created_sup_cat


@masters_router.post("/create_category/",response_model=CategoryMaster)
async def create_category(category_data:CategoryMaster):

    category_collect = mongo_client(db,"category_master")
    sup_cat_collect = mongo_client(db,"super_category_master")

    if category_collect.find_one({"category_name":category_data.category_name}):
        raise HTTPException(status_code=400, detail="Category already exists")
    

    if category_data.super_category_id and not sup_cat_collect.find_one({"_id":ObjectId(category_data.super_category_id)}):
        raise HTTPException(status_code=400,detail="Invalid Super Category Id")
    

    result = category_collect.insert_one(category_data.dict())
    created_category = category_collect.find_one({"_id":result.inserted_id})

    return created_category


@masters_router.post("/create_department/",response_model=DepartmentMaster)
async def create_department(department_data:DepartmentMaster):

    depart_collect = mongo_client(db,"department_master")
    
    if depart_collect.find_one({"department_name":department_data.department_name}):
        raise HTTPException(status_code=400,detail="Department already exists")
    
    result = depart_collect.insert_one(department_data.dict())

    created_depart = depart_collect.find_one({"_id":result.inserted_id})

    return created_depart


@masters_router.post("/create_location/", response_model=LocationMaster)
async def create_location(location_data:LocationMaster):

    locat_collect = mongo_client(db,"location_master")

    if locat_collect.find_one({"location_name":location_data.location_name}):
        raise HTTPException(status_code=400,detail="Location already exists")
    
    result = locat_collect.insert_one(location_data.dict())
    created_locat = locat_collect.find_one({"_id":result.inserted_id})

    return created_locat


@masters_router.post("/create_item/",response_model=ItemMaster)
async def create_item(item_data:ItemMaster):

    item_collect = mongo_client(db,"item_master")

    if item_collect.find_one({"item_name":item_data.item_name,"item_code":item_data.item_code,"item_specification":item_data.item_specification}):
        raise HTTPException(status_code=400,detail="Item with Item Code & Specification already exists")
    
    result = item_collect.insert_one(item_data.dict())
    created_item = item_collect.find_one({"_id":result.inserted_id})

    return created_item