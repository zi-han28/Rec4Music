# db.py
import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
# TEMP DEBUG
print("=== ENV DEBUG ===")
print(f"MONGODB_URI present: {bool(os.getenv('MONGODB_URI'))}")
print(f"MONGODB_URI value (first 30): {str(os.getenv('MONGODB_URI'))[:30]}")
print(f"All env keys containing MONGO: {[k for k in os.environ if 'MONGO' in k.upper()]}")
print(f"RAILWAY env vars: {[k for k in os.environ if k.startswith('RAILWAY')]}")
print("=================")

MONGODB_URI = os.getenv("MONGODB_URI")

print(f"MONGODB_URI loaded: {bool(MONGODB_URI)}")
if MONGODB_URI:
    print(f"URI starts with: {MONGODB_URI[:20]}...")

client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
db = client["rec4music"]          # database name — pick anything, created automatically
users_collection = db["users"]    # equivalent of your old "users" table