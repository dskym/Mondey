from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth import get_user_model, authenticate

from .utils import get_token, decode_token

from .models import CustomCategory, Expenditure, IncomeHistory, CategoryHistory
from .serializers import CustomCategorySerializer, ExpenditureSerializer, \
    IncomeHistorySerializer, CategoryHistorySerializer

import requests
import json

User = get_user_model()


class UserAPI(APIView):
    """
    User API
    """
    authentication_classes = ()

    # Sign In
    def get(self, request):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(email=email, password=password)

        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        token = get_token(user.email)

        return Response(status=status.HTTP_200_OK, data=token)

    # Sign Up
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        firebase_token = None

        if 'firebase_token' in request.data.keys():
            firebase_token = request.data['firebase_token']

        user = User.objects.create_user(email=email, password=password, firebase_token=firebase_token)

        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    # Update firebase token
    def put(self, request):
        email = request.data['email']
        password = request.data['password']
        firebase_token = request.data['firebase_token']

        user = authenticate(email=email, password=password)

        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.firebase_token = firebase_token
        user.save()

        return Response(status=status.HTTP_200_OK)

    # Delete user
    def delete(self, request):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(email=email, password=password)

        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()

        return Response(status=status.HTTP_200_OK)


class TokenAPI(APIView):
    """
    Refresh Token API
    """

    authentication_classes = ()

    def get(self, request):
        refresh_token = decode_token(request.data['refresh_token'])

        if refresh_token['type'] == 'refresh':
            data = get_token(refresh_token['email'])

            return Response(status=status.HTTP_200_OK, data=data)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class PushMessageAPI(APIView):
    """
    FCM Push Message Test API
    """
    authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request):
        headers = request.headers
        data = request.data

        token = headers['Authorization'].split(' ')[1]
        email = decode_token(token)['email']

        SERVER_KEY = "AAAAtUjeBg4:APA91bH7Hdvr3XgV58j5D-J_ayDnhZseRDKgcdJ7qS8QtGFjfB0J8cnXu4kX61" \
                     "YQS_zfBytarnJseKM7IxTpXdKU2jXCxNsBqUccScLIVNa6DUuIZZZpLGY5QqFVRBs6mTqy4X7Hjnog"
        firebase_token = User.objects.get(email=email).firebase_token

        url = 'https://fcm.googleapis.com/fcm/send'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + SERVER_KEY,
        }

        message = {
            "to": firebase_token,
            "data": {
                "title": data['title'],
                "body": data['body'],
            }
        }

        response = requests.post(url=url, data=json.dumps(message), headers=headers)
        response_data = None

        if response:
            response_data = json.loads(response.text)

        return Response(status=status.HTTP_200_OK, data=response_data)


class CustomCategoryView(APIView):
    """
    Custom Category API

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_category_id = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    limit_amount = models.IntegerField()
    period = models.CharField(max_length=10)
    """
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            user_id = User.objects.get(email=email).id

            custom_category = CustomCategory.objects.filter(user=user_id)
            serializer = CustomCategorySerializer(custom_category, many=True)

            return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            user_id = User.objects.get(email=email).id

            custom_category_data = {
                'user': user_id,
                'custom_category_id': request.data['custom_category_id'],
                'category': request.data['category'],
                'name': request.data['name'],
                'limit_amount': request.data['limit_amount'],
                'period': request.data['period'],
            }

            serializer = CustomCategorySerializer(data=custom_category_data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            user_id = User.objects.get(email=email).id
            custom_category_id = request.data['custom_category_id']

            custom_category = CustomCategory.objects.filter(user_id=user_id, custom_category_id=custom_category_id)[0]

            custom_category_data = {
                'id': custom_category.id,
                'user': user_id,
                'custom_category_id': custom_category_id,
                'category': request.data['category'],
                'name': request.data['name'],
                'limit_amount': request.data['limit_amount'],
                'period': request.data['period'],
            }

            serializer = CustomCategorySerializer(custom_category, data=custom_category_data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            user_id = User.objects.get(email=email).id
            custom_category_id = request.data['custom_category_id']

            custom_category = CustomCategory.objects.filter(user_id=user_id, custom_category_id=custom_category_id)[0]

            custom_category.delete()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_403_FORBIDDEN)


class ExpenditureView(APIView):
    """
    Expenditure API

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expenditure_id = models.IntegerField()
    custom_category = models.ForeignKey(CustomCategory, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.IntegerField()
    detail = models.CharField(max_length=20)
    """
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            user_id = User.objects.get(email=email).id

            expenditure = Expenditure.objects.filter(user=user_id)
            serializer = ExpenditureSerializer(expenditure, many=True)

            return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            user_id = User.objects.get(email=email).id

            expenditure_data = {
                'user': user_id,
                'expenditure_id': request.data['expenditure_id'],
                'custom_category': request.data['custom_category'],
                'date': request.data['date'],
                'amount': request.data['amount'],
                'detail': request.data['detail'],
            }

            serializer = ExpenditureSerializer(data=expenditure_data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            user_id = User.objects.get(email=email).id
            expenditure_id = request.data['expenditure_id']

            expenditure = Expenditure.objects.filter(user_id=user_id, expenditure_id=expenditure_id)[0]

            expenditure_data = {
                'id': expenditure.id,
                'user': user_id,
                'expenditure_id': expenditure_id,
                'custom_category': request.data['custom_category'],
                'date': request.data['date'],
                'amount': request.data['amount'],
                'detail': request.data['detail'],
            }

            serializer = ExpenditureSerializer(expenditure, data=expenditure_data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            user_id = User.objects.get(email=email).id
            expenditure_id = request.data['expenditure_id']

            expenditure = Expenditure.objects.filter(user_id=user_id, expenditure_id=expenditure_id)[0]

            expenditure.delete()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_403_FORBIDDEN)


class IncomeHistoryView(APIView):
    """
    Income History API

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income_history_id = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    total_income = models.IntegerField()
    """
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            user_id = User.objects.get(email=email).id

            income_history = IncomeHistory.objects.filter(user=user_id)
            serializer = IncomeHistorySerializer(income_history, many=True)

            return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            user_id = User.objects.get(email=email).id

            income_history_data = {
                'user': user_id,
                'income_history_id': request.data['income_history_id'],
                'year': request.data['year'],
                'month': request.data['month'],
                'total_income': request.data['total_income'],
            }

            serializer = IncomeHistorySerializer(data=income_history_data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN)


class CategoryHistoryView(APIView):
    """
    Immutable

    Category History API

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_history_id = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    total_limit = models.IntegerField()
    """
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            user_id = User.objects.get(email=email).id

            category_history = CategoryHistory.objects.filter(user=user_id)
            serializer = CategoryHistorySerializer(category_history, many=True)

            return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            user_id = User.objects.get(email=email).id

            category_history_data = {
                'user': user_id,
                'category_history_id': request.data['category_history_id'],
                'category': request.data['category'],
                'year': request.data['year'],
                'month': request.data['month'],
                'total_limit': request.data['total_limit'],
            }

            serializer = CategoryHistorySerializer(data=category_history_data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN)
