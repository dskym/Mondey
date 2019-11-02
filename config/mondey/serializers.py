from rest_framework import serializers
from .models import User, CustomCategory, Expenditure, IncomeHistory, CategoryHistory

import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

    def validate(self, data):
        # pattern = r'^[.]+@[.]+\.[.]+$'
        pattern = r'^.+$'

        if re.match(pattern, data['email']) is None:
            raise serializers.ValidationError('Email type is not valid')

        return data


class CustomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomCategory
        fields = '__all__'

    def validate(self, data):
        return data

"""
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_category_id = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    limit_amount = models.IntegerField()
    period = models.CharField(max_length=10)
"""

class ExpenditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenditure
        fields = '__all__'

    def validate(self, data):
        return data


class IncomeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeHistory
        fields = '__all__'

    def validate(self, data):
        return data


class CategoryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryHistory
        fields = '__all__'

    def validate(self, data):
        return data
