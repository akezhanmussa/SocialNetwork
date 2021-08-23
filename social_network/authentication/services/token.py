import datetime
import jwt
from social_network import settings


class TokenOperationException(Exception):
    """Raises on token operation related errors."""


def generate_jwt_token(user_info: dict, life_span: datetime.timedelta, secret_key : str = settings.SECRET_KEY, algorithm:str='HS256'):
    exp_date = datetime.datetime.now() + life_span
    exp_date_in_sec = int(exp_date.strftime('%s'))

    token = jwt.encode(
        {
            **user_info,
            'exp': exp_date_in_sec,
        },
        secret_key,
        algorithm=algorithm,
    )

    return token


def decode_jwt_token(token: str, secret_key: str = settings.SECRET_KEY, algorithms : tuple = ('HS256')):
    print(secret_key)
    try:
        return jwt.decode(token, secret_key, algorithms=algorithms)
    except jwt.DecodeError as e:
        print(e)
        raise TokenOperationException(
            f'Could not decode token {token}'
        ) from e
