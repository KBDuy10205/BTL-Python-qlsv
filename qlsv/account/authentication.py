from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from .models import Tokens

class MyJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        # Kiểm tra token có tồn tại trong DB và chưa bị revoke
        try:
            token_obj = Tokens.objects.get(access_token=str(validated_token), account=user)
        except Tokens.DoesNotExist:
            raise AuthenticationFailed('Token is invalid or revoked')
        
        if token_obj.is_revoked:
            raise AuthenticationFailed('Token has been revoked')
        
        return user
