import datetime
import jwt


def generate_jwt_token(user_info: dict, life_span: datetime.timedelta, secret_key: str, algorithm='HS256'):
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
