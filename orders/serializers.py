from importlib.resources import read_binary
from itertools import product
from django.db import transaction
from rest_framework import serializers
from  orders.models import *
from products.serializers import SimpleProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = Cartitems
        fields = ["id", "cart", "product", "quantity", "sub_total"]

    def total(self, cartitem: Cartitems):
        return cartitem.quantity * cartitem.product.price
