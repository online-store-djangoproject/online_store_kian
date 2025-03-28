from django.core.validators import RegexValidator
from django.db import models
from cors.models import User
from django.utils.timezone import now, timedelta

# Create your models here.


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    full_address = models.TextField()
    postalcode_regex = RegexValidator(r'^\d{10}$', message=' Enter a valid zipcode. ')
    postal_code = models.CharField(max_length=10, validators=[postalcode_regex])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email},{self.city}, {self.state}"



# class DiscountCode(models.Model):
#     code = models.CharField(max_length=20, unique=True)  # کد تخفیف
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discount_codes")
#     percentage = models.IntegerField(default=15)  # درصد تخفیف
#     created_at = models.DateTimeField(auto_now_add=True)  # زمان ایجاد
#
#     def __str__(self):
#         return f"{self.code} - {self.user.email}"
#
#     @staticmethod
#     def user_can_get_discount(user):
#         """ بررسی کند که آیا کاربر می‌تواند کد جدید دریافت کند یا نه """
#         last_code = DiscountCode.objects.filter(user=user).order_by('-created_at').first()
#         if last_code and last_code.created_at.month == now().month:
#             return False  # اگر کاربر در این ماه کد گرفته، اجازه ندارد
#         return True