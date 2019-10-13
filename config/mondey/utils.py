import jwt
from datetime import datetime, timedelta

JWT_KEY = '4tqzms(6fb)6ba4$uy@sj4u=28ne08w7zx2c%2dj8aw)87s+$q'


def jwt_get_username_from_payload_handler(payload):
    """
    Override this function if username is formatted differently in payload
    """
    return payload.get('email')


def get_token(email):
    access_payload = {
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(hours=1),
        'email': email,
    }

    refresh_payload = {
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(days=14),
        'email': email,
    }

    access = jwt.encode(payload=access_payload, key=JWT_KEY, algorithm='HS256')
    refresh = jwt.encode(payload=refresh_payload, key=JWT_KEY, algorithm='HS256')

    token = {
        "access": access.decode('utf-8'),
        "refresh": refresh.decode('utf-8')
    }

    return token


def decode_token(token):
    data = jwt.decode(token, key=JWT_KEY, algorithms='HS256')

    return data

