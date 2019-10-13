from rest_framework import serializers
from .models import User

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
