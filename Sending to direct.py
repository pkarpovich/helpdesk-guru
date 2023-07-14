import instagrapi

class DirectSender:
    def __init__(self, username, password,proxy_address=None):
        self.username = username
        self.password=password
        self.proxy_address = proxy_address
        self.api = instagrapi.Client(proxies= {"http": self.proxy_address} if self.proxy_address else None)

    def login(self):
        self.api.login(self.username, self.password)

    def send_message(self, recipient_username, text):
        recipient_id = self.api.user_id_from_username(recipient_username)
        self.api.direct_send(recipient_id, text)

username = 'username'
password = 'user_password'
proxy_address = "//70o1oNEc-N80C94P:wifi;ca;;;toronto@proxy.soax.com:9137"
attempt = DirectSender(username, password,proxy_address)
attempt.login()
attempt.send_message('recipient_username', 'Hello world!')