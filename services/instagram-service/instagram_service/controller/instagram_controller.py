import asyncio

from instagram_service.services import InstagramService, GptService


class InstagramController:
    def __init__(self, instagram_service: InstagramService, gpt_service: GptService) -> None:
        self.gpt_service = gpt_service
        self.instagram_service = instagram_service

    def login(self) -> None:
        return self.instagram_service.login()

    def read_direct_messages(self) -> list:
        return self.instagram_service.read_direct_messages()

    async def ask(self, query: str) -> str:
        return await self.gpt_service.ask(query)

    def send_direct_messages(self, message: str, sender_username: str) -> None:
        return self.instagram_service.send_direct_message(message, sender_username)

    async def start(self, interval_seconds=60) -> None:
        self.login()
        while True:
            direct_messages = self.read_direct_messages()
            if direct_messages is None:
                continue
            for message in direct_messages:
                sender_username = self.instagram_service.client.username_from_user_id(message.user_id)
                response = self.ask(message)
                self.send_direct_messages(message=response, sender_username=sender_username)
            await asyncio.sleep(interval_seconds)
