import yaml
import pydantic


class ConfLoadException(Exception):
    """Raises on configuration load related errors."""


class BotConf(pydantic.BaseModel):
    number_of_users: int
    max_posts_per_user: int
    max_likes_per_user: int


def load(conf_path: str):
    try:
        with open(conf_path) as f:
            raw_conf = yaml.safe_load(f)
            conf = BotConf(**raw_conf)
            return conf
    except FileNotFoundError as e:
        raise ConfLoadException(
            f'configuration file does not exist: {e}',
        )
    except yaml.YAMLError as e:
        raise ConfLoadException(
            f'can not load file with yaml format: {e}',
        )
    except pydantic.ValidationError as e:
        raise ConfLoadException(
            f'configuration file is invalid: {e}',
        )
