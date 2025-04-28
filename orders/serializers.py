from importlib.resources import read_binary
from itertools import product
from django.db import transaction
from rest_framework import serializers
from  orders.models import *
from products.serializers import SimpleProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")
    inventory = serializers.IntegerField(source='product.inventory', read_only=True)

    class Meta:
        model = Cartitems
        fields = ["id", "cart", "product", "quantity", "sub_total","inventory"]

    def total(self, cartitem: Cartitems):
        return cartitem.quantity * cartitem.product.price


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")
        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cartitem = Cartitems.objects.get(product_id=product_id, cart_id=cart_id)
            product = cartitem.product


            if cartitem.quantity + quantity > product.inventory:
                raise serializers.ValidationError("موجودی محصول کافی نیست")

            cartitem.quantity += quantity
            cartitem.save()

            self.instance = cartitem

        except Cartitems.DoesNotExist:

            product = Product.objects.get(pk=product_id)
            if quantity > product.inventory:
                raise serializers.ValidationError("موجودی محصول کافی نیست")

            self.instance = Cartitems.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = Cartitems
        fields = ["id", "product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # class Meta:
    #     model = Cartitems
    #     fields = ["quantity"]
    # class Meta:
    #     model = Cartitems
    #     fields = ["quantity"]
    #
    # def update(self, instance, validated_data):
    #     quantity = validated_data.get("quantity", instance.quantity)
    #     if quantity <= 0:
    #         instance.delete()
    #     else:
    #         instance.quantity = quantity
    #         instance.save()
    #     return instance
    class Meta:
        model = Cartitems
        fields = ["quantity"]

    def validate_quantity(self, value):
        cartitem = self.instance
        if value > cartitem.product.inventory:
            raise serializers.ValidationError("موجودی محصول کافی نیست")
        return value

    def update(self, instance, validated_data):
        if validated_data["quantity"] < 1:
            instance.delete()
            return None
        return super().update(instance, validated_data)




class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name='main_total')

    class Meta:
        model = Cart
        fields = ["id", "items", "grand_total"]

    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total


#  order


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', "placed_at", "pending_status", "owner", "items"]



# class CreateOrderSerializer(serializers.Serializer):
#     cart_id = serializers.UUIDField()
#
#     def validate_cart_id(self, cart_id):
#         if not Cart.objects.filter(pk=cart_id).exists():
#             raise serializers.ValidationError("This cart_id is invalid")
#
#         elif not Cartitems.objects.filter(cart_id=cart_id).exists():
#             raise serializers.ValidationError("Sorry your cart is empty")
#
#         return cart_id
#
#     def save(self, **kwargs):
#         with transaction.atomic():
#             cart_id = self.validated_data["cart_id"]
#             user_id = self.context["user_id"]
#             order = Order.objects.create(owner_id=user_id)
#             cartitems = Cartitems.objects.filter(cart_id=cart_id)
#             orderitems = [
#                 OrderItem(order=order,
#                           product=item.product,
#                           quantity=item.quantity
#                           )
#                 for item in cartitems
#             ]
#             OrderItem.objects.bulk_create(orderitems)
#             # Cart.objects.filter(id=cart_id).delete()
#             return order

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("This cart_id is invalid")

        elif not Cartitems.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError("Sorry your cart is empty")

        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]


            order = Order.objects.create(owner_id=user_id)
            cartitems = Cartitems.objects.filter(cart_id=cart_id)


            orderitems = [
                OrderItem(order=order,
                          product=item.product,
                          quantity=item.quantity
                          )
                for item in cartitems
            ]
            OrderItem.objects.bulk_create(orderitems)


            order.update_total_amount()


            cartitems.delete()

            return order




class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["pending_status"]