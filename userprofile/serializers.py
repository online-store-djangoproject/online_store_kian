from rest_framework import serializers
from .models import Address




class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','user','city','state','full_address','postal_code']
        extra_kwargs = {"user": {"read_only": True}}