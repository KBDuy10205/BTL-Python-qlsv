from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    # def create(self, validated_data):
    #     # dùng create_user để đảm bảo set_password
    #     return Account.objects.create_user(
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #     )



class AccountLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)