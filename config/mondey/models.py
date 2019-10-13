from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, firebase_token=None):
        if email is None:
            raise ValueError('Please enter your email.')

        if password is None:
            raise ValueError('Please enter your password.')

        user = self.model(
            email=self.normalize_email(email),
            password=password,
            firebase_token=firebase_token
        )

        user.set_password(raw_password=password)
        user.save()

        return user


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    firebase_token = models.CharField(max_length=4096, null=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email
