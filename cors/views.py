from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from django.views import View
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,UserLoginSerializer

# Create your views here.


# class UserRegisterView(GenericAPIView):
#     serializer_class = UserRegisterSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             try:
#                 serializer.save()
#                 user = serializer.instance  # دریافت شیء User ذخیره‌شده
#                 print(user)
#                 return Response({
#                     'data': UserRegisterSerializer(user).data,  # سریالایز مجدد برای حذف فیلدهای اضافی
#                     'message': f'Hi {user.get_full_name()}! Thanks for signing up.'
#                 }, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# # login method 1
#
# class UserLoginView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             return Response({
#                 "data": serializer.validated_data,
#                 "message": "Login successful."
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)