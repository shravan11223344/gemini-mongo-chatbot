import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from pymongo import DESCENDING
from pymongo.collection import Collection
from pymongo import ReturnDocument

from db.mongo import get_collection

# MongoDB collection
conversations: Collection = get_collection("conversations")

# Index for faster sorting
conversations.create_index([("last_interacted", DESCENDING)])


# ---- Helper ----
def new_utc() -> datetime:
    return datetime.now(timezone.utc)


def create_new_conversation_id() -> str:
    return str(uuid.uuid4())


# ---- Create Conversation ----
def create_new_conversation(
        title: Optional[str] = None,
        role: Optional[str] = None,
        content: Optional[str] = None,
) -> str:

    conv_id = create_new_conversation_id()
    ts = new_utc()

    doc: Dict[str, Any] = {
        "_id": conv_id,
        "title": title or "Untitled Conversation",
        "messages": [],
        "last_interacted": ts,
    }

    if role and content:
        doc["messages"].append({
            "role": role,
            "content": content,
            "ts": ts
        })

    conversations.insert_one(doc)

    return conv_id


# ---- Add Message ----
def add_message(conv_id: str, role: str, content: str) -> bool:

    ts = new_utc()

    result = conversations.update_one(
        {"_id": conv_id},
        {
            "$push": {
                "messages": {
                    "role": role,
                    "content": content,
                    "ts": ts
                }
            },
            "$set": {
                "last_interacted": ts
            }
        }
    )

    return result.matched_count == 1


# ---- Get Conversation ----
def get_conversation(conv_id: str) -> Optional[Dict[str, Any]]:

    ts = new_utc()

    doc = conversations.find_one_and_update(
        {"_id": conv_id},
        {"$set": {"last_interacted": ts}},
        return_document=ReturnDocument.AFTER
    )

    return doc


# ---- Get All Conversations ----
def get_all_conversations() -> Dict[str, str]:

    cursor = conversations.find(
        {},
        {"title": 1}
    ).sort("last_interacted", DESCENDING)

    return {
        doc["_id"]: doc.get("title", "Untitled")
        for doc in cursor
    }