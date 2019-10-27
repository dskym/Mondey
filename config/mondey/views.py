from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth import get_user_model, authenticate

from .utils import get_token, decode_token

import requests
import json

User = get_user_model()


class UserList(APIView):
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


class TokenList(APIView):
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


class TestList(APIView):
    """
    Auth Test API
    """
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request):
        headers = request.headers
        token = headers['Authorization'].split(' ')[1]
        data = decode_token(token)

        if data['type'] == 'access':
            email = data['email']

            return Response(status=status.HTTP_200_OK, data=email)

        return Response(status=status.HTTP_403_FORBIDDEN)


class PushList(APIView):
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
