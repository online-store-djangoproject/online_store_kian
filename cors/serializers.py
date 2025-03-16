from rest_framework import serializers
from cors.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken,Token
from django.conf import settings
import redis
import random
from rest_framework.exceptions import ValidationError
from .email import send_otp_email, send_password_email
# password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_bytes, force_str
from django.urls import reverse




class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'phone', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        del validated_data['password2']
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data



#  login method 1 ===

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    user_id = serializers.IntegerField(source='id', read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise AuthenticationFailed("Both email and password are required.")
        user = authenticate(username=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid email or password.")
        if not user.is_active:
            raise AuthenticationFailed("This account is inactive.")
        if not user.is_verified:
            raise AuthenticationFailed("This account is not verified.")

        tokens = user.tokens()
        return {
            "email": user.email,
            "access_token": str(tokens.get("access")),
            "refresh_token": str(tokens.get("refresh")),
            'user_id': user.id
        }


#  login method 2 ===

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=1, decode_responses=True)

class UserOTPLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get("email")

        user = User.objects.filter(email=email).first()
        if not user:
            raise ValidationError("User with this email does not exist.")

        otp = str(random.randint(100000, 999999))

        redis_client.setex(f"otp:{email}", 300, otp)

        send_otp_email(email, otp)
        return data


class UserOTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")
        stored_otp = redis_client.get(f"otp:{email}")

        if not stored_otp or stored_otp != otp:
            raise ValidationError("Invalid or expired OTP.")

        user = User.objects.filter(email=email).first()
        if not user:
            raise ValidationError("User does not exist.")

        redis_client.delete(f"otp:{email}")

        tokens = user.tokens()
        return {
            "email": user.email,
            "access_token": str(tokens.get("access")),
            "refresh_token": str(tokens.get("refresh")),
            'user_id': user.id
        }



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain = get_current_site(request).domain
            relative_link = reverse('passcon')  # به جای مسیر API از مسیر فرانت استفاده کنید
            abslink = f'http://{site_domain}{relative_link}?uidb64={uidb64}&token={token}'
            email_body = f'Hi use the link below to reset your password \n {abslink}'
            data = {
                'email_body': email_body,
                'email_subject': 'Reset your password',
                'to_email':user.email,
            }
            send_password_email(data)

        return super().validate(attrs)

#                 SetNewPasswordSerializer

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('reset link is invalid or has expired.')
            if password != confirm_password:
                raise AuthenticationFailed('password and confirm_password do not match.')
            user.set_password(password)
            user.save()
            return user

        except Exception as e:
            raise AuthenticationFailed('link is invalid or has expired.')

# ===logout===

class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {
        'bad_token':('Token is invalid or has expired.')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
