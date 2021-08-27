import json
import os
import requests
import random
import string
import conf


class ClientException(Exception):
    """Raises on client related exceptions."""


class Client:

    def __init__(self, server_url):
        self._server_url = server_url

    def _create_dummy_user(self):
        random_index = int(random.random() * 1000)
        return {
            'username': f'dummy_user_{random_index}',
            'password': f'DummyUser{random_index}',
            'email':  f'dummy.user{random_index}@gmail.com',
        }

    def _create_dummy_post_description(self):
        return ''.join(random.choice(string.ascii_letters) for _ in range(10))

    def create_users(self, number_of_users: int):
        users = []

        for _ in range(number_of_users):
            response = requests.post(
                f'{self._server_url}/api/users/authentication/signup/',
                json={
                    'user': self._create_dummy_user(),
                },
            )

            if response.status_code != 200:
                raise ClientException(
                    f'Could not create user: {response.content.decode("utf-8")}',
                )

            data = response.json()
            users.append(data['user'])

        return users

    def create_post(self, user: dict):
        response = requests.post(
            f'{self._server_url}/api/posts/create/',
            json={
                'post': {
                    'description': self._create_dummy_post_description()
                }
            },
            headers={
                'Authorization': f'simpletoken {user["token"]}',
            }
        )

        if response.status_code != 200:
            raise ClientException(
                f'Could not retrieve users from the server: {response.content.decode("utf-8")}',
            )

        return response.json()

    def _operation_on_post(self, user: dict, post: dict, operation: str):
        return requests.post(
            f'{self._server_url}/api/posts/operation/',
            json={
                'id': post['id'],
                'operation': operation,
            },
            headers={
                'Authorization': f'simpletoken {user["token"]}',
            }
        )

    def like_post(self, user: dict, post: dict):
        response = self._operation_on_post(
            user,
            post,
            'like'
        )

        if response.status_code != 204:
            raise ClientException(
                f'Could not like the post: {response.content.decode("utf-8")}',
            )

    def unlike_post(self, user: dict, post: dict):
        response = self._operation_on_post(
            user,
            post,
            'like'
        )

        if response.status_code != 204:
            raise ClientException(
                f'Could not unlike the post: {response.content.decode("utf-8")}',
            )


class Bot:
    def _setup(self):
        self.users = []
        self.posts = []
        self.liked_posts = []
        self.unliked_posts = []

    def __init__(self, conf_path: str):
        self.config: conf.Conf = conf.load(os.path.abspath(conf_path))
        self.client = Client(self.config.server.url)
        self._setup()

    def save_activity(self, activity_path):
        activity = {
            'created_users': self.users,
            'created_posts': self.posts,
            'liked_posts': self.liked_posts,
            'unliked_posts': self.unliked_posts,
        }

        with open(activity_path, 'w') as f:
            json.dump(activity, f)

    def signup_users(self):
        self.users = self.client.create_users(
            number_of_users=self.config.bot.number_of_users,
        )

    def create_random_posts(self):
        for user in self.users:
            for _ in range(self.config.bot.max_posts_per_user):
                post = self.client.create_post(user)
                self.posts.append(post)

    def create_random_likes_on_posts(self):
        for user in self.users:
            for _ in range(self.config.bot.max_likes_per_user):
                post_to_like = random.choice(self.posts)
                self.client.like_post(user, post_to_like)
                post_to_like['liked_by_now'] = user
                self.liked_posts.append(post_to_like)

    def create_random_unlikes_on_posts(self):
        for user in self.users:
            for _ in range(self.config.bot.max_likes_per_user):
                post_to_unlike = random.choice(self.posts)
                self.client.unlike_post(user, post_to_unlike)
                post_to_unlike['unliked_by_now'] = user
                self.unliked_posts.append(post_to_unlike)

    def __enter__(self):
        self.signup_users()
        self.create_random_posts()
        self.create_random_likes_on_posts()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._setup()


if __name__ == '__main__':
    bot = Bot(
        conf_path='bot/conf.yaml',
    )

    with bot as prepared_bot:
        prepared_bot.save_activity(os.path.abspath('bot_activity.json'))
