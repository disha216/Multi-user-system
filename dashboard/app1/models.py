from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Additional fields for the custom user
    usertype = models.CharField(max_length=50, choices=[('doctor', 'Doctor'), ('client', 'Client')], default='client')
    line1 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    pphoto = models.ImageField(upload_to="images", blank=True, null=True)

    def __str__(self):
        return self.username

