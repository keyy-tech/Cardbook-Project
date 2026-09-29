from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings

# Create your models here.


class UserBaseManager(BaseUserManager):

    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        return self.create_user(
            email=email,
            password=password
            **extra_fields
        )

class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserBaseManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE
    )
    code = models.CharField(max_length=8)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.code}"