from django.db import IntegrityError
import htmlmin
import os
from rest_framework import permissions, status, generics, views
from rest_framework.response import Response
import uuid

from account.models import Account, ApiKey
from account.serializers import register as serializers
from thistothat.common.aws import ses


class RequestApiKeyView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RequestApiKeySerializer


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']

        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            account = Account.objects.create(email=email)

        # TODO: set some sort of limit for multiple keys per account...

        api_key = ApiKey.objects.create(account=account, key=str(uuid.uuid4()).replace('-', ''))

        with open(os.path.join('account', 'resources', 'api_key.html'), 'r') as f:
            html = f.read()

        html = html.replace('--api_key--', api_key.key)
        html = htmlmin.minify(html)

        text = f'Your API key is: {api_key.key}'
        ses.send_email(
            'ThisToThat <accounts@thistothat.io>', 
            [email], 
            'Your API Key', 
            text=text, 
            html=html
        )
        
        return Response(status=status.HTTP_200_OK)


# TODO: test this!
def send_api_key_email(api_key, email):
    
    with open(os.path.join('account', 'resources', 'api_key.html'), 'r') as f:
        html = f.read()
        html = html.replace('--api_key--', api_key.key)

    text = f'Your API key is: {api_key.key}'
    ses.send_email('casey@thistothat.io', [email], 'Your API Key', text=text, html=html)
    