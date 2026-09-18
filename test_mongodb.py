# test_db_connection.py
import os
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "rec4music")

print(f"URI loaded: {bool(MONGODB_URI)}")

try:
    client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
    
    # This forces an actual round-trip to the server
    client.admin.command('ping')
    print("✅ Connected to MongoDB Atlas successfully!")
    
    db = client[MONGODB_DB_NAME]
    print(f"Using database: {db.name}")
    print(f"Existing collections: {db.list_collection_names()}")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")