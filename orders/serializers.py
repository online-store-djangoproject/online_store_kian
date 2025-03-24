from importlib.resources import read_binary
from itertools import product
from django.db import transaction
from rest_framework import serializers
from  orders.models import *