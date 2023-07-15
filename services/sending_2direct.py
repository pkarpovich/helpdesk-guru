import instagrapi

class DirectSender:
    def __init__(self, username: str, password: str, proxy_address: str = None) -> None:
        """
        Create an instance of DirectSender class.

        Arguments:
            username (str): Instagram username.
            password (str): Instagram password.
            proxy_address (str, optional): Proxy address. Defaults to None.
        """
        self.username = username
        self.password = password
        self.proxy_address = proxy_address
        self.api = instagrapi.Client(proxies={"http": self.proxy_address} if self.proxy_address else None)

    def login(self) -> None:
        """
        Login to Instagram account using instagrapi.
        """
        self.api.login(self.username, self.password)

    def send_message(self, recipient_username: str, message: str) -> None:
        """
        Send direct message to a recipient on Instagram using instagrapi.

        Arguments:
            recipient_username (str): Instagram username of the recipient.
            message (str): Message text to be sent.
        """
        recipient_id = self.api.user_id_from_username(recipient_username)
        self.api.direct_send(recipient_id, message)

username = 'username'
password = 'user_password'
proxy_address = "proxy_address"
attempt = DirectSender(username, password, proxy_address)
attempt.login()
attempt.send_message('recipient_username', 'your_message')
