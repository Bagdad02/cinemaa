from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import RegisterSerializer, LoginSerializer

User = get_user_model()


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = 'вы успешно зарегистреривоныб вам отправлено письмо'
            return Response(message, status=201)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            # user.is_activation_code = ''///
            user.save()
            return Response('был успешно активировон акаунт', status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response('активатционный код не действует', status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    # permission_classes = [AllowAny]
    def post(self, request):
        try:
            user = request.user
            Token.objects.filter(user=user).delete()
            return Response('вы успешно разлогинолись')
        except:
            return Response(status=status.HTTP_403_FORBIDDEN )

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_user_password
        return Response('пароль успешно зарегистрриревано')
