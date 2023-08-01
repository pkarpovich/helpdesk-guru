from src.client import client_grpc
from src.instagram import InstagramService
import asyncio


class instagram_Contoller:
    def __int__(self, instagram_service: InstagramService, client: client_grpc) -> None:
        self.client = client
        self.instagram_service = instagram_service

    def read_direct_messages(self) -> list:
        return self.instagram_service.read_direct_messages()

    def run(self, query: str) -> str:
        return self.client.run(query)

    def send_direct_messages(self, message: str, sender_username: str) -> None:
        return self.instagram_service.send_direct_message(message, sender_username)

    async def start(self, interval_seconds=60) -> None:
        while True:
            direct_messages = self.read_direct_messages()
            if direct_messages:
                for message in direct_messages:
                    sender_username = self.instagram_service.client.username_from_user_id(message.user_id)
                    response = self.run(message)
                    self.send_direct_messages(message=response, sender_username=sender_username)
            await asyncio.sleep(interval_seconds)