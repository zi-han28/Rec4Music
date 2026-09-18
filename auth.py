# auth.py (MongoDB version)
import bcrypt
from db import users_collection

def init_db():
    """Ensure username is unique (equivalent of PRIMARY KEY)."""
    try:
        users_collection.create_index("username", unique=True)
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        raise 

def create_user(username, password):
    """Register a new user securely."""
    if not username or not password:
        return False, "Username and password cannot be empty."

    if users_collection.find_one({"username": username}):
        return False, "Username already exists."

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        users_collection.insert_one({
            "username": username,
            "password": hashed_pw,
            "favourites": []
        })
        return True, "Account created successfully! Please login."
    except Exception as e:
        return False, f"Error creating account: {e}"

def authenticate_user(username, password):
    """Verify login credentials."""
    user = users_collection.find_one({"username": username})
    if user:
        stored_hash = user["password"]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return True
    return False

def get_user_favourites(username):
    """Get favourites for a user."""
    user = users_collection.find_one({"username": username})
    if user:
        return user.get("favourites", [])
    return []

def add_to_favourites(username, track_data):
    """Add a track to user's favourites."""
    favourites = get_user_favourites(username)

    for track in favourites:
        if track['track_id'] == track_data['track_id']:
            return False, "Song already in favourites"

    try:
        users_collection.update_one(
            {"username": username},
            {"$push": {"favourites": track_data}}
        )
        return True, "Added to favourites!"
    except Exception as e:
        return False, f"Error adding to favourites: {e}"

def remove_from_favourites(username, track_id):
    """Remove a track from user's favourites."""
    try:
        users_collection.update_one(
            {"username": username},
            {"$pull": {"favourites": {"track_id": track_id}}}
        )
        return True, "Removed from favourites!"
    except Exception as e:
        return False, f"Error removing from favourites: {e}"

def is_favourite(username, track_id):
    """Check if a track is in user's favourites."""
    favourites = get_user_favourites(username)
    return any(track['track_id'] == track_id for track in favourites)