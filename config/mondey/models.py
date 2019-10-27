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
    password = models.CharField(max_length=200)
    firebase_token = models.CharField(max_length=4096, null=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email


class UserSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income = models.IntegerField()
    alarm = models.TimeField()


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.EmailField(max_length=20, unique=True)


class CustomCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    limit_amount = models.IntegerField()
    period = models.CharField(max_length=10)


class Expenditure(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.IntegerField()
    detail = models.CharField(max_length=20)


class IncomeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    total_income = models.IntegerField()


class CategoryHistory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    total_limit = models.IntegerField()
