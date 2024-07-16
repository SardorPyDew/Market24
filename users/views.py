from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from shared.custom_pagination import CustomPagination

from shared.utils import send_code_to_email
from users.models import UserModel, ConfirmationModel, CODE_VERIFIED, VIA_EMAIL, VIA_PHONE
from users.serializers import CreateUserSerializer, UpdateUserSerializer, LoginSerializer, LogoutSerializer, \
    UserListViewSerializer, ForgetPasswordSerializer


class RegisterCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer
    model = UserModel.objects.all()


class UserVerifyCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = request.data.get('code')

        verification_code = ConfirmationModel.objects.filter(
            code=code, is_confirmed=False, user_id=user.id,
            expiration_time__gte=timezone.now()
        )
        if not verification_code.exists():
            response = {
                'success': False,
                'message': 'Your verification code is None.'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        ConfirmationModel.objects.update(is_confirmed=True)

        user.auth_status = CODE_VERIFIED
        user.save()

        response = {
            'success': True,
            'message': 'You are successfully logged in.',
            'auth_status': user.auth_status
        }

        return Response(response, status=status.HTTP_200_OK)


class ResendVerifyCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user

        verification_code = ConfirmationModel.objects.filter(is_confirmed=False, user_id=user.id,
                                                             expiration_time=timezone.now())

        if verification_code.exists():
            response = {
                'success': False,
                'message': 'You Have already verified'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        self.send_code()

        response = {
            'success': True,
            'message': 'New code is sent',
        }
        return Response(response,  status=status.HTTP_200_OK)

    def send_code(self):
        user = self.request.user
        new_code = user.create_verify_code(verify_type=user.auth_type)
        if user.auth_type == VIA_EMAIL:
            send_code_to_email(user.email, new_code)


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(UserUpdateAPIView, self).update(request, *args, **kwargs)
        response = {
            'success': True,
            'message': 'User updated successfully',
            'auth_status': self.request.user.auth_status
        }
        return Response(response, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        refresh = self.request.data['refresh_token']
        token = RefreshToken(token=refresh)
        token.blacklist()
        response = {
            'success': True,
            'message': 'User Logout successful'
        }
        return Response(response, status=status.HTTP_202_ACCEPTED)


class RefreshTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


class LoginListAPIView(generics.ListAPIView):
    model = UserModel.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = UserListViewSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return UserModel.objects.all()


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserListViewSerializer
    permission_classes = [IsAdminUser]


class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = ForgetPasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email_phone_number = serializer.validated_data.get('email')
            user = serializer.validated_data.get("user")

            if email_phone_number.endswith('@gmail.com'):
                new_code = user.create_verify_code(VIA_EMAIL)
                send_code_to_email(user.email, new_code)
            response = {
                "success": True,
                "message": "Code is sent to user",
                "access_token": user.token()['access_token']
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "success": False,
                "message": "Invalid data"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

