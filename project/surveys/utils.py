import jwt
import datetime
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM

def create_token(user_id):
    payload = {
        "user_id": user_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Срок действия
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Если токен валиден, возвращаем полезную нагрузку
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired")  # Истек срок действия токена
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token")  # Неверный токен
