import os
import requests
from . import conf


_SERVER_URL = 'http://127.0.0.1:8000'


class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def retrieve_users(self, number_of_users: int):
        response = requests.get(
            f'{_SERVER_URL}/api/users/',
            params={
                'number_of_users': number_of_users,
            }
        )
        return response.json()


class Bot:
    def __init__(self, conf_path: str):
        self.config: conf.BotConf = conf.load(os.path.abspath(conf_path))
        self.client = Client()
        self.users = []

    def __enter__(self):
        self.users = self.client.retrieve_users(self.config.number_of_users)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
