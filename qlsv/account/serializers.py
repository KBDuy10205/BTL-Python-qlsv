from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class AccountLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)