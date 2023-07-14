from instagrapi import Client
import time
class DirectMessageReader:
    def __init__(self, username, password, proxy=None):
        if proxy:
            self.client = Client(proxy=proxy)
        else:
            self.client = Client()
        self.client.login(username, password)

    def read_direct_messages(self):
        threads = self.client.direct_threads()
        for thread in threads:
            messages = thread.messages
            for message in messages:
                print(message.text)

    def start_reading_messages(self, interval_seconds=60):
        while True:
            self.read_direct_messages()
            time.sleep(interval_seconds)


username = "username"
password = "password"
proxy_address = "http://70o1oNEc-N80C94P:wifi;ca;;;toronto@proxy.soax.com:9137"
reader = DirectMessageReader(username, password, proxy=proxy_address)
reader.start_reading_messages()