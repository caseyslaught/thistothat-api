
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions, status
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from account.models import Account, ApiKey


class LenientApiKeyAuthentication(BaseAuthentication):

    def authenticate(self, request):

        api_key_str = request.query_params.get('api_key')
        if not api_key_str:
            return None

        try:
            api_key = ApiKey.objects.get(key=api_key_str, is_active=True)
            return (api_key.account, api_key_str)
        except ApiKey.DoesNotExist:
            raise exceptions.AuthenticationFailed({
                "error": "invalid_api_key"
            }, status.HTTP_401_UNAUTHORIZED)