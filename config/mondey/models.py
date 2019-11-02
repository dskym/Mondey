from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import hashlib


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
    password = models.CharField(max_length=200, null=False)
    firebase_token = models.CharField(max_length=4096, null=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    """
    def set_password(self, raw_password):
        salt = b'mondey'
        iterations = 1000

        self.password = hashlib.pbkdf2_hmac('sha256', bytes(raw_password, 'utf-8'), salt, iterations).hex()
    """

    def __str__(self):
        return self.email


class UserSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income = models.IntegerField()
    alarm = models.TimeField(null=True)


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)


class CustomCategory(models.Model):
    class Meta:
        unique_together = (('user', 'custom_category_id'), )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_category_id = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    limit_amount = models.IntegerField()
    period = models.CharField(max_length=10)


class Expenditure(models.Model):
    class Meta:
        unique_together = (('user', 'expenditure_id'), )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expenditure_id = models.IntegerField()
    custom_category = models.ForeignKey(CustomCategory, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.IntegerField()
    detail = models.CharField(max_length=20)


class IncomeHistory(models.Model):
    class Meta:
        unique_together = (('user', 'income_history_id'), )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income_history_id = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    total_income = models.IntegerField()


class CategoryHistory(models.Model):
    class Meta:
        unique_together = (('user', 'category_history_id'), )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_history_id = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    total_limit = models.IntegerField()
