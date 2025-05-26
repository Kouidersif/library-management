from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from BookLibrariBackend.models import BaseModel




class UserManager(BaseUserManager):
    """
    Custom user manager for User model.
    """

    def create_user(self, email, first_name, last_name, password=None, password2=None):
        """
        Creates and saves a User with the given email, first_name, last_name and password.
        """
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, first_name, last_name and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_superuser = True
        user.is_verified = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(BaseModel, AbstractUser):

    email = models.EmailField(max_length=255, unique=True, help_text="Email address")
    username = None
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of the User object.
        """
        return self.email

    def get_full_name(self):
        """
        Returns the full name of the User.
        """
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """
        Returns the short name of the User.
        """
        return self.first_name

