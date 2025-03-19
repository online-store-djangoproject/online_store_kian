from django.urls import path
from . import views

urlpatterns = [
    path('addresses/', views.AddressListCreateView.as_view(), name="address_list"),
    path('addresses/<int:pk>/', views.AddressUpdateDeleteView.as_view(), name="address_detail"),


]
