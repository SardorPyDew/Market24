"""from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from shared.utils import send_code_to_email
from users.models import UserModel, VIA_EMAIL, VIA_PHONE, DONE


class RegisterSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(RegisterSerializer, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)

    uuid = serializers.IntegerField(read_only=True)
    auth_type = serializers.CharField(read_only=True, required=False)
    auth_status = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = UserModel
        fields = ['uuid', 'auth_type', 'auth_status']

    def validate(self, attrs):
        return self.auth_validate(attrs)

    def create(self, validated_data):
        user = super(RegisterSerializer, self).create(validated_data)
        code = user.create_verify_code(user.auth_type)

        if user.auth_type == VIA_EMAIL:
            send_code_to_email(user.email, code)
        user.save()
        return user

    def auth_validate(self, data):
        user_input = str(data['email']).lower()
        if user_input.endswith('@gmail.com'):
            data = {
                'email': user_input,
                'auth_type': VIA_EMAIL
            }
        elif user_input.startswith("+"):
            data = {
                'phone_number': user_input,
                'auth_type': VIA_PHONE
            }
        else:
            data = {
                'success': False,
                'message': "Please enter a valid phone number or email"
            }
            raise serializers.ValidationError(data)
        return data

    def to_representation(self, instance):
        data = super(RegisterSerializer, self).to_representation(instance)
        data['access_token'] = instance.token()['access_token']
        return data


class UpdateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            response = {
                'success': False,
                'message': "Passwords don't match"
            }
            raise serializers.ValidationError(response)

        return attrs

    def validate_username(self, username):
        if UserModel.objects.filter(username=username).exists():
            response = {
                'success': False,
                'message': "Username already exists"
            }

            raise serializers.ValidationError(response)

        return username

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)

        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
            instance.auth_status = DONE
            instance.save()

        return instance


class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['userinput'] = serializers.CharField(max_length=128, required=False)
        self.fields['username'] = serializers.CharField(max_length=128, required=False)

    def validate(self, attrs):
        userinput = attrs.get('userinput')
        if userinput.endswith('@gmail.com'):
            user = UserModel.objects.filter(email=userinput).first()

        elif userinput.startswith('+'):
            user = UserModel.objects.filter(phone_number=userinput).first()

        else:
            user = UserModel.objects.filter(username=userinput).first()

        if user is None:
            response = {
                'success': False,
                'message': "Invalid username or password"
            }

            raise serializers.ValidationError(response)

        auth_user = authenticate(username=user.username, password=attrs['password'])
        if auth_user is None:
            response = {
                'success': False,
                'message': "Username or password incorrect"
            }

            raise serializers.ValidationError(response)

        response = {
            'status': True,
            'access_token': auth_user.token()['access_token'],
            'refresh_token': auth_user.token()['refresh_token']
        }

        return response


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
"""


from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response

from shared.utils import send_code_to_email
from users.models import UserModel, VIA_EMAIL, VIA_PHONE, DONE, ConfirmationModel, CODE_VERIFIED
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class CreateUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords must match."})

        if UserModel.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = UserModel.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data.get('username'),
        )

        refresh = RefreshToken.for_user(user)
        verify_code = user.create_verify_code(VIA_EMAIL)

        send_code_to_email(user.email, verify_code)

        return {
            'user': user.pk,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def to_representation(self, instance):
        return {
            'user': instance['user'],
            'refresh': instance['refresh'],
            'access': instance['access'],
        }

    def send_code_to_email(email, code):
        send_mail(
            'Verification Code',
            f'Your verification code is {code}',
            'emailizi yozas@gmail.com',
            [email],
            fail_silently=False,
        )


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        if not ConfirmationModel.objects.filter(code=value, is_confirmed=False).exists():
            raise serializers.ValidationError("Invalid or expired code.")
        return value

    def to_representation(self, instance):
        return {
            'user': instance['user'],
            'refresh': instance['refresh'],
            'access': instance['access'],
        }

    def save(self, **kwargs):
        code = self.validated_data['code']
        confirmation = ConfirmationModel.objects.get(code=code)
        confirmation.is_confirmed = True
        confirmation.save()
        confirmation.user.auth_status = CODE_VERIFIED
        confirmation.user.save()
        return confirmation.user


class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['username'] = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        userinput = attrs.get('username')
        password = attrs.get('password')

        if userinput.endswith('@gmail.com'):
            user = UserModel.objects.filter(email=userinput).first()
        else:
            user = UserModel.objects.filter(username=userinput).first()

        if user is None:
            raise serializers.ValidationError("Username is invalid")

        auth_user = authenticate(username=user.username, password=password)
        if auth_user is None:
            raise serializers.ValidationError("Username or Password is invalid")

        refresh = RefreshToken.for_user(auth_user)
        response = {
            "status": True,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        return response


class UpdateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, write_only=True, required=True)
    last_name = serializers.CharField(max_length=255, write_only=True, required=True)
    username = serializers.CharField(max_length=255, write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'email']

    def validate_username(self, username):
        if UserModel.objects.filter(username=username).exists():
            response = {
                "success": False,
                "message": "Username is already gotten"
            }
            raise serializers.ValidationError(response)
        return username

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        return instance


"""class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['userinput'] = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        userinput = attrs.get('userinput')
        password = attrs.get('password')

        if userinput.endswith('@gmail.com'):
            user = UserModel.objects.filter(email=userinput).first()
        else:
            user = UserModel.objects.filter(username=userinput).first()

        if user is None:
            raise serializers.ValidationError("Username is invalid")

        auth_user = authenticate(username=user.username, password=password)
        if auth_user is None:
            raise serializers.ValidationError("Username or Password is invalid")

        refresh = RefreshToken.for_user(auth_user)
        response = {
            "status": True,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        return response"""


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email_phone_number = attrs.get('email')
        response = {"success": False}
        if not email_phone_number:
            response = {"message": "Email or phone number is required"}
            raise serializers.ValidationError(response)

        user = UserModel.objects.filter(Q(email=email_phone_number) | Q(phone_number=email_phone_number))
        if not user.exists():
            response["message"] = "User not found"
            raise serializers.ValidationError(response)

        attrs["user"] = user.first()
        return attrs


