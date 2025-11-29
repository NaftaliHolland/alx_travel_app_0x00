import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have email")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Default fields we get AbstractUser

        - id I need to overide this to use UUID
        - password
        - last_login
        - is_superuser
        - username (Special, Unique Constraint)
        - first_name
        - last_name
        - email
        - is_staff
        - is_active
        - date_joined
    """

    ROLE_CHOICES = [("guest", "Guest"), ("owner", "Owner")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = None
    email = models.EmailField(max_length=256, unique=True, verbose_name="email")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="guest")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}-{self.first_name} {self.last_name}"
