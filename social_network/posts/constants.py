import enum


class PostOperation(str, enum.Enum):
    LIKE = 'like'
    UNLIKE = 'unlike'
