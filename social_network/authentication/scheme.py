from rest_framework import authentication, exceptions
from . import services
from . import models


class JWTAuthentication(authentication.BaseAuthentication):
    _authentication_header_prefix = 'simpletoken'

    def is_valid_header_prefix(self, header_prefix: str):
        return self._authentication_header_prefix == header_prefix.lower()

    def authenticate(self, request):
        request.user = None

        try:
            header_prefix, token = authentication.get_authorization_header(request).split()
        except ValueError:
            return None

        header_prefix = header_prefix.decode('utf-8')
        token = token.decode('utf-8')

        if not self.is_valid_header_prefix(header_prefix):
            return None

        try:
            payload = services.token.decode_jwt_token(token)
            user = models.User.objects.get(pk=payload['id'])
        except services.token.TokenOperationException as e:
            raise exceptions.AuthenticationFailed(
                'Could not decode a given token',
            ) from e
        except models.User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'Encoded token contains invalid information',
            )

        return user, token
