from fastapi import FastAPI
from fastapi.routing import APIRouter
from settings import mongo_client
from .model import IndentDetails, ItemDetails
from fastapi import HTTPException
from typing import List
import os
from bson import ObjectId

indent_router = APIRouter()

db = os.getenv('MONGO_DB')


@indent_router.post("/indent_create/",response_model=IndentDetails)
async def create_indent_and_items(indent_data: IndentDetails):

    locat_collect = mongo_client(db,"location_master")
    depart_collect = mongo_client(db,"department_master")
    indent_collect = mongo_client(db, "indent_details")
    item_collect = mongo_client(db,"item_master")


    # Check if the indent_code already exists
    if indent_collect.find_one({"indent_code": indent_data.indent_code}):
        raise HTTPException(status_code=400, detail=f"Indent code '{indent_data.indent_code}' already exists")

    # Validate department and location
    if indent_data.department_id and not depart_collect.find_one({'_id': ObjectId(indent_data.department_id)}):
        raise HTTPException(status_code=400, detail="Department doesn't exist")
    
    if indent_data.location_id and not locat_collect.find_one({'_id': ObjectId(indent_data.location_id)}):
        raise HTTPException(status_code=400, detail="Location doesn't exist")
    
    # Validate each item
    for item_detail in indent_data.indentitems:
        if not item_collect.find_one({'_id': ObjectId(item_detail.item)}):
            raise HTTPException(status_code=400, detail=f"Item with id {item_detail.item} doesn't exist")
    
    # Insert indent details along with the items
    result_indent = indent_collect.insert_one(indent_data.dict())

    # Retrieve the created indent including items
    created_indent = indent_collect.find_one({"_id": result_indent.inserted_id})

    # Ensure successful retrieval
    if not created_indent:
        raise HTTPException(status_code=500, detail="Failed to create indent details")

    # Convert MongoDB document to a Pydantic model
    created_indent_model = IndentDetails(**created_indent)

    return created_indent_model


@indent_router.get("/all_indents/", response_model=List[IndentDetails])
async def get_all_indents():
    indent_collect = mongo_client(db, "indent_details")
    locat_collect = mongo_client(db, "location_master")
    depart_collect = mongo_client(db, "department_master")
    item_collect = mongo_client(db, "item_master")

    all_indents = list(indent_collect.find({}))

    # print(len(all_indents),'all_indents')

    indent_views = []
    for indent in all_indents:
        # print(indent['location_id'],'---------')
        # Fetch location and department names
        location_name = None
        if indent['location_id']:
            location = locat_collect.find_one({'_id': ObjectId(indent['location_id'])})
            # print(location,'location============location')
            location_name = location['location_name'] if location else None

        department_name = None
        if indent['department_id']:
            department = depart_collect.find_one({'_id': ObjectId(indent['department_id'])})
            department_name = department['department_name'] if department else None


        # Process indent items
        item_views = []
        for item_detail in indent.get('indentitems', []):
            item = item_collect.find_one({'_id': ObjectId(item_detail['item'])})
            item_name = item.get('item_name') if item else None
            item_views.append({
                "item_name"        :item_name,
                "quantity"         :item_detail['quantity'],
                "updated_quantity" :item_detail['updated_quantity'],
                "status"           :item_detail['status'],
            })

        indent_views.append({
            "indent_purpose": indent['indent_purpose'],
            "indent_remarks": indent['indent_remarks'],
            "indent_code"   : indent.get('indent_code'),
            "department_id" : department_name,
            "location_id"   : location_name,
            "indentitems"   : item_views,
            "status"        : indent['status'],
        })

    print(type(indent_views))

    # for view in indent_views:
    #     print(type(view))
    #     print(view)
    
    return indent_views


@indent_router.get("/user_indent", response_model=List[IndentDetails])
async def user_wise_indent():
    pass

