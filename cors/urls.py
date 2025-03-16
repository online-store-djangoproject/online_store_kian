from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
urlpatterns = [

    # TOKEN JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # register
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    # path("login/send_otp/", views.UserOTPLoginView.as_view(), name="send-otp"),
    # path("login/verify_otp/", views.UserOTPVerifyView.as_view(), name="verify-otp"),

]