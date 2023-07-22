from instagrapi import Client
from datetime import datetime
class InstagramService:
    def __init__(self, username: str, password: str, proxy: str = None) -> None:
        self.client = Client(proxy=proxy)
        try:
            self.client.login(username, password)
        except Exception as e:
            print(f"Error while setting up Instagram client: {e}")
        self.latest_message_timestamps = {}
    def send_direct_message(self, recipient_username: str, message: str) -> None:
        recipient_id = self.client.user_id_from_username(recipient_username)
        recipient_id = int(recipient_id)
        self.client.direct_send(message, [recipient_id])
    def read_direct_messages(self) -> None:
        threads = self.client.direct_threads()
        for thread in threads:
            thread_id = thread.id
            if thread_id in self.latest_message_timestamps:
                latest_timestamp = self.latest_message_timestamps[thread_id]
            else:
                latest_timestamp = None
            messages = thread.messages
            if messages:
                first_message_timestamp = messages[0].timestamp
            else:
                first_message_timestamp = datetime.utcnow()
            for message in messages:
                if latest_timestamp is None or message.timestamp > latest_timestamp:
                    if message.text:
                        print(message.text)
                    self.latest_message_timestamps[thread_id] = message.timestamp
            if latest_timestamp is None:
                self.latest_message_timestamps[thread_id] = first_message_timestamp
