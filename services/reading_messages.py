from instagrapi import Client
import time

class DirectMessageReader:
    def __init__(self, username: str, password: str, proxy: str = None) -> None:
        """
        Create an instance of DirectMessageReader class.

        Arguments:
            username (str): Instagram username.
            password (str): Instagram password.
            proxy (str, optional): Proxy address. Defaults to None.
        """
        if proxy:
            self.client = Client(proxy=proxy)
        else:
            self.client = Client()
        self.client.login(username, password)

    def read_direct_messages(self) -> None:
        """
        Read and print direct messages from Instagram using instagrapi.
        """
        threads = self.client.direct_threads()
        for thread in threads:
            messages = thread.messages
            for message in messages:
                print(message.text)

    def start_reading_messages(self, interval_seconds: int = 60) -> None:
        """
        Start reading direct messages from Instagram repeatedly in a specified time interval.

        Arguments:
            interval_seconds (int, optional): Time interval between each reading in seconds. Defaults to 60.
        """
        while True:
            self.read_direct_messages()
            time.sleep(interval_seconds)


username = "username"
password = "password"
proxy_address = "proxy_address"
reader = DirectMessageReader(username, password, proxy=proxy_address)
reader.start_reading_messages()
