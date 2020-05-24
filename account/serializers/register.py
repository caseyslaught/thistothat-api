
from rest_framework import serializers


class RequestApiKeySerializer(serializers.Serializer):
    email = serializers.EmailField()