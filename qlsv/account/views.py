from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import AccountSerializer, AccountLoginSerializer
from datetime import datetime, timedelta, timezone
from .models import Tokens
from rest_framework.permissions import IsAuthenticated

class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()

            return JsonResponse({
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({
                'error_message': 'This email has already exist!',
                'errors_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = AccountLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                # Hạn của access/refresh token
                access_expiry = datetime.now(timezone.utc) + timedelta(minutes=5)   # ví dụ 5 phút
                refresh_expiry = datetime.now(timezone.utc) + timedelta(days=1)     # ví dụ 1 ngày

                # Lưu DB
                Tokens.objects.create(
                    account=user,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    access_token_expiry=access_expiry,
                    refresh_token_expiry=refresh_expiry,
                )

                return Response({
                    'refresh_token': refresh_token,
                    'access_token': access_token,
                    'access_token_expiry': access_expiry,
                    'refresh_token_expiry': refresh_expiry
                }, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'Email or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)
    



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Lấy access token từ header
            auth_header = request.headers.get("Authorization", "")
            token_str = auth_header.split(" ")[1]
            token_obj = Tokens.objects.get(access_token=token_str, account=request.user)
            token_obj.is_revoked = True
            token_obj.save()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)