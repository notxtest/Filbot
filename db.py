from pymongo import MongoClient
from config import MONGO_URL, DB_NAME
import logging
from bson.objectid import ObjectId
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s'
)

try:
    mongo_client = MongoClient(MONGO_URL)
    db = mongo_client[DB_NAME]
    
    # Collections
    filters_collection = db["filters"]
    users_collection = db["users"] 
    groups_collection = db["groups"]
    dm_filters_collection = db["dm_filters"]
    dm_settings_collection = db["dm_settings"]
    
    logging.info("✅ MongoDB connected successfully!")
except Exception as e:
    logging.error(f"❌ Failed to connect to MongoDB: {e}")

# ==========================================================
# 🟢 NORMAL FILTERS FUNCTIONS
# ==========================================================

def save_filter(keyword: str, filter_data: dict):
    upsert_doc = {"keyword": keyword, **filter_data}
    filters_collection.update_one(
        {"keyword": {"$regex": f"^{re.escape(keyword)}$", "$options": "i"}},
        {"$set": upsert_doc},
        upsert=True
    )

def delete_filter(keyword: str):
    result = filters_collection.delete_one({"keyword": {"$regex": f"^{re.escape(keyword)}$", "$options": "i"}})
    return result.deleted_count > 0

def get_filter(keyword: str):
    return filters_collection.find_one({"keyword": {"$regex": f"^{re.escape(keyword)}$", "$options": "i"}})

def get_filter_by_id(id_str: str):
    try:
        return filters_collection.find_one({"_id": ObjectId(id_str)})
    except:
        return None

def get_all_filters():
    return list(filters_collection.find({}).sort("keyword", 1))

# ==========================================================
# 🟢 DM FILTERS FUNCTIONS
# ==========================================================

def save_dm_filter(keyword: str, filter_data: dict):
    upsert_doc = {"keyword": keyword, **filter_data}
    dm_filters_collection.update_one(
        {"keyword": {"$regex": f"^{re.escape(keyword)}$", "$options": "i"}},
        {"$set": upsert_doc},
        upsert=True
    )

def delete_dm_filter(keyword: str):
    result = dm_filters_collection.delete_one({"keyword": {"$regex": f"^{re.escape(keyword)}$", "$options": "i"}})
    return result.deleted_count > 0

def get_dm_filter(keyword: str):
    return dm_filters_collection.find_one({"keyword": {"$regex": f"^{re.escape(keyword)}$", "$options": "i"}})

def get_dm_filter_by_id(id_str: str):
    try:
        return dm_filters_collection.find_one({"_id": ObjectId(id_str)})
    except:
        return None

def get_all_dm_filters():
    return list(dm_filters_collection.find({}).sort("keyword", 1))

# ==========================================================
# 🟢 DM SETTINGS MANAGEMENT
# ==========================================================

def get_dm_settings():
    settings = dm_settings_collection.find_one({"_id": "global_settings"})
    if not settings:
        settings = {
            "_id": "global_settings",
            "dm_filters_enabled": False,
            "creation_mode": False,
            "global_groups_enabled": False,
            "enabled_groups": [],
            "disabled_groups": []
        }
        dm_settings_collection.insert_one(settings)
    return settings

def update_dm_settings(update_data: dict):
    dm_settings_collection.update_one(
        {"_id": "global_settings"},
        {"$set": update_data},
        upsert=True
    )

def is_dm_filter_enabled_for_group(chat_id: int) -> bool:
    settings = get_dm_settings()
    if not settings["global_groups_enabled"]:
        return chat_id in settings["enabled_groups"]
    return chat_id not in settings["disabled_groups"]

# ==========================================================
# 🟢 USER & GROUP MANAGEMENT
# ==========================================================

def update_user_data(user_id: int, chat_id: int, bot_token: str):
    if chat_id == user_id:
        users_collection.update_one(
            {"user_id": user_id, "bot_token": bot_token},
            {"$set": {"user_id": user_id, "bot_token": bot_token}},
            upsert=True
        )
    
    if chat_id != user_id:
        groups_collection.update_one(
            {"chat_id": chat_id, "bot_token": bot_token},
            {"$set": {"chat_id": chat_id, "bot_token": bot_token}},
            upsert=True
        )

def get_user_count(bot_token: str) -> int:
    return users_collection.count_documents({"bot_token": bot_token})

def get_group_count(bot_token: str) -> int:
    return groups_collection.count_documents({"bot_token": bot_token})

# ==========================================================
# 🟢 HELPER FUNCTIONS
# ==========================================================

def short_display(text: str, limit: int = 50) -> str:
    if not text:
        return ""
    if len(text) <= limit:
        return text
    return text[:limit-3] + "..."
