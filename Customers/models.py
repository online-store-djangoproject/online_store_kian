from django.core.validators import RegexValidator
from django.db import models
from cors.models import User


# Create your models here.



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    full_address = models.TextField()
    postalcode_regex = RegexValidator(r'^\d{10}$', message=' Enter a valid zipcode. ')
    postal_code = models.CharField(max_length=10, validators=[postalcode_regex])

    def __str__(self):
        return f"{self.city}, {self.state}"