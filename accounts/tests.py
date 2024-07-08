from django.test import TestCase
from .models import UserProfile


print(UserProfile.objects.get(email='a@gmail.com').id)
