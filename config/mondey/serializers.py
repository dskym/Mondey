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
    """
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_category_id = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    limit_amount = models.IntegerField()
    period = models.CharField(max_length=10)
    """
    class Meta:
        model = CustomCategory
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        response = dict()
        response['custom_category_id'] = data['custom_category_id']
        response['category'] = data['category']
        response['name'] = data['name']
        response['limit_amount'] = data['limit_amount']
        response['period'] = data['period']

        return response

    def validate(self, data):
        return data


class ExpenditureSerializer(serializers.ModelSerializer):
    """
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expenditure_id = models.IntegerField()
    custom_category = models.ForeignKey(CustomCategory, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.IntegerField()
    detail = models.CharField(max_length=20)
    """
    class Meta:
        model = Expenditure
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        response = dict()
        response['expenditure_id'] = data['expenditure_id']
        response['custom_category'] = data['custom_category']
        response['date'] = data['date']
        response['amount'] = data['amount']
        response['detail'] = data['detail']

        return response

    def validate(self, data):
        return data


class IncomeHistorySerializer(serializers.ModelSerializer):
    """
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income_history_id = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    total_income = models.IntegerField()
    """
    class Meta:
        model = IncomeHistory
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        response = dict()
        response['income_history_id'] = data['income_history_id']
        response['year'] = data['year']
        response['month'] = data['month']
        response['total_income'] = data['total_income']

        return response

    def validate(self, data):
        return data


class CategoryHistorySerializer(serializers.ModelSerializer):
    """
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_history_id = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    total_limit = models.IntegerField()
    """
    class Meta:
        model = CategoryHistory
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        response = dict()
        response['category_history_id'] = data['category_history_id']
        response['category'] = data['category']
        response['year'] = data['year']
        response['month'] = data['month']
        response['total_limit'] = data['total_limit']

        return response

    def validate(self, data):
        return data
