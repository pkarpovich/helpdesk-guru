from instagrapi import Client
class InstagramService:
    def __init__(self, username: str, password: str, proxy: str = None) -> None:
       self.client = Client(proxy=proxy)
        try:
            self.client.login(username, password)
        except Exception as e:
            print(f"Error while setting up Instagram client: {e}")
    def send_direct_message(self, recipient_username: str, message: str) -> None:
        recipient_id = self.client.user_id_from_username(recipient_username)
        recipient_id = int(recipient_id)
        self.client.direct_send(message, [recipient_id])
    def read_direct_messages(self) -> None:
        threads = self.client.direct_threads()
        for thread in threads:
            messages = thread.messages
            for message in messages:
                if message.text:
                    print(message.text)