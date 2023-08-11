from typing import TYPE_CHECKING

from pymongo import MongoClient

if TYPE_CHECKING:
    from gpt_context.services import AppConfig


class ConversationStore:
    def __init__(self, config: 'AppConfig'):
        self._client = MongoClient(
            config.MONGODB_URI,
            username=config.MONGODB_USERNAME,
            password=config.MONGODB_PASSWORD
        )
        self._db = self._client["gpt_context"]
        self._collection = self._db["conversations"]

    def save_or_update(self, conversation_id: str, messages: list[dict]):
        existing = self.get_by_id(conversation_id)
        if existing is not None:
            self._collection.update_one({"conversation_id": conversation_id}, {"$set": {"messages": messages}})
            return

        self._collection.insert_one({
            "conversation_id": conversation_id,
            "messages": messages
        })

    def get_by_id(self, conversation_id: str) -> dict | None:
        return self._collection.find_one({"conversation_id": conversation_id})

    def delete_by_id(self, conversation_id: str) -> None:
        self._collection.delete_one({"conversation_id": conversation_id})
