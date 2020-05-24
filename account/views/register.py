from django.db import IntegrityError
from rest_framework import permissions, status, generics, views
from rest_framework.response import Response
import uuid

from account.models import Account, ApiKey
from account.serializers import register as serializers


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

        return Response({
            'api_key': api_key.key
        }, status=status.HTTP_200_OK)
