from django.db import models
from api.file_crypto import generateKey
from django.contrib.auth.models import User
import uuid


class Trustee(models.Model):
    username = models.CharField(default="",max_length=200)
    email = models.CharField(default="",max_length=200)
    
    def __str__(self):
        return self.username

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    cryptoKey = models.CharField(default=generateKey, max_length=200)
    trustee = models.OneToOneField(Trustee,null=True ,on_delete=models.SET_NULL)
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.username
