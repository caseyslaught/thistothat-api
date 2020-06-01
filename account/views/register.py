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

        if account.api_keys.count() > 0:
            subject = "Your New API Key"
            message = "Thanks for coming back! Your new API key will give you programmatic access to datasets like commodities and species. Your old keys are still valid."
        else:
            subject = "Your API Key"
            message = "Thanks for signing up for ThisToThat. You now have programmatic access to a bunch of different datasets like commodities and species!"

        api_key = ApiKey.objects.create(account=account, key=str(uuid.uuid4()).replace('-', ''))

        with open(os.path.join('account', 'resources', 'api_key.html'), 'r') as f:
            html = f.read()

        html = html.replace('--message--', message)
        html = html.replace('--api_key--', api_key.key)
        html = htmlmin.minify(html)

        text = f'Your ThisToThat API key is: {api_key.key}'
        ses.send_email(
            sender='ThisToThat <accounts@thistothat.io>',
            recipients=[email], 
            subject=subject,
            text=text,
            html=html
        )

        return Response(status=status.HTTP_200_OK)

