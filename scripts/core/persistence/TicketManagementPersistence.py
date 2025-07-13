from pymongo import MongoClient
from bson import ObjectId
from scripts.Common.AppConfigurations import APP_CONFIG
from scripts.Common.AppConstants import UserRole
from scripts.utils.logger import setup_logger

logger = setup_logger()

client = MongoClient(APP_CONFIG.MONGODB_URI)
db = client[APP_CONFIG.MONGO_DB_NAME]
collection = db.tickets

def insert_ticket(data):
    try:
        result = collection.insert_one(data)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Exception in insert_ticket {e}")
        raise

def modify_ticket(update_json):
    try:
        result = collection.update_one({"_id": ObjectId(update_json.get("ticket_id"))}, {"$set": {"status":  update_json.get("status"), "comments": update_json.get("comments"), "updated_by": update_json.get("updated_by", "static-user")}})
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Exception in modify_ticket {e}")
        raise

def fetch_ticket(ticket_id):
    try:
        ticket = collection.find_one({"_id": ObjectId(ticket_id)})
        if ticket:
            ticket["_id"] = str(ticket["_id"])
        return ticket
    except Exception as e:
        logger.error(f"Exception in fetch_ticket {e}")
        raise

def fetch_tickets_by_user(input_json):
    try:
        query = {"created_by": input_json.get("user_id") } if input_json and input_json.get("user_id", None) else {}
        return [
            {**doc, "_id": str(doc["_id"])} for doc in collection.find(query)
        ]
    except Exception as e:
        logger.error(f"Exception in fetch_tickets_by_role {e}")
        raise