from instagrapi import Client
import time


# define the InstagramService class
class InstagramService:
    # set up the client by logging in with the provided credentials
    def __init__(self, username, password, proxy=None):
        if proxy:
            self.client = Client(proxy=proxy)
        else:
            self.client = Client()
        self.client.login(username, password)

    # send a direct message to a specified recipient
    def send_direct_message(self, recipient_username, message):
        recipient_id = self.client.user_id_from_username(recipient_username)
        recipient_id = int(recipient_id)
        self.client.direct_send(message, [recipient_id])

    # read all direct messages for the logged in user
    def read_direct_messages(self):
        threads = self.client.direct_threads()
        for thread in threads:
            messages = thread.messages
            for message in messages:
                if message.text:
                    # print the text of the message to the console
                    print(message.text)

    # continuously read direct messages at a specified interval of time
    def start_reading_messages(self, interval_seconds=60):
        while True:
            # call the read_direct_messages method to read messages
            self.read_direct_messages()
            time.sleep(interval_seconds)


# define the necessary variables
username = "username"
password = "password"
proxy_address = "proxy_address"

# create an instance of InstagramService with the specified credentials and proxy
instagram_service = InstagramService(username, password, proxy=proxy_address)

# read direct messages once
instagram_service.read_direct_messages()

# start reading direct messages repeatedly
instagram_service.start_reading_messages()

# send a direct message to specified recipient
instagram_service.send_direct_message("recipient_username", "message_text")
