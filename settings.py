import os
import dotenv
from pymongo import MongoClient
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, HTTPException, Depends


dotenv.load_dotenv()
MONGO_URL = os.getenv('MONGODB_URL')

# Security setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def mongo_client(db_name,db_collection):
    client = MongoClient(MONGO_URL)
    db = client[db_name]
    collection = db[db_collection]
    return collection



# Dependency to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    # In a real application, you would validate the token and retrieve the user from the database
    return {"username": "user123", "user_id": "123"}