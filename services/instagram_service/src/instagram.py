from instagrapi import Client
from datetime import datetime
class InstagramService:
    def __init__(self, username: str, password: str, proxy: str = None) -> None:
        self.client = Client(proxy=proxy)
        self.username=username
        self.password=password

    
    def login(self) -> None:
        try:
            self.client.login(self.username, self.password)
        except Exception as e:
            print(f"Error while setting up Instagram client: {e}")
        self.latest_message_timestamps = {}


    def send_direct_message(self, message: str, sender_username: str) -> None:
        sender_id = self.client.user_id_from_username(sender_username)
        sender_id = int(sender_id)
        recipients = [sender_id]
        thread_id = self.client.direct_thread(*recipients).id
        self.client.direct_send(message, thread_id)

    
    def read_direct_messages(self) -> list:
        messages = []
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
                    if message.text and message.user_id != self.client.user_id and message.thread_id == thread_id:
                        messages.append(message.text.strip())
                    self.latest_message_timestamps[thread_id] = message.timestamp
            if latest_timestamp is None:
                self.latest_message_timestamps[thread_id] = first_message_timestamp

        return messages

