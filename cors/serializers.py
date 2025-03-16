# from rest_framework import serializers
# from cors.models import User
# from django.contrib.auth import authenticate
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework_simplejwt.exceptions import TokenError
# from rest_framework_simplejwt.tokens import RefreshToken,Token
#
#
# class UserRegisterSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ['first_name','last_name', 'email', 'phone', 'password', 'password2']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         del validated_data['password2']
#         user = User.objects.create_user(**validated_data)
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
#
#
#     def validate(self, data):
#         if data['password'] != data['password2']:
#             raise serializers.ValidationError('Passwords must match.')
#         return data
#
#
#
# #  login method 1 ===
#
# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#     access_token = serializers.CharField(max_length=255, read_only=True)
#     refresh_token = serializers.CharField(max_length=255, read_only=True)
#     user_id = serializers.IntegerField(source='id', read_only=True)
#
#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')
#
#         if not email or not password:
#             raise AuthenticationFailed("Both email and password are required.")
#
#
#         user = authenticate(username=email, password=password)
#
#         if not user:
#             raise AuthenticationFailed("Invalid email or password.")
#         if not user.is_active:
#             raise AuthenticationFailed("This account is inactive.")
#         if not user.is_verified:
#             raise AuthenticationFailed("This account is not verified.")
#
#
#         tokens = user.tokens()
#
#         return {
#             "email": user.email,
#             "access_token": str(tokens.get("access")),
#             "refresh_token": str(tokens.get("refresh")),
#             'user_id': user.id
#         }
#
#
# #  login method 2 ===