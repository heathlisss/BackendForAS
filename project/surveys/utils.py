import jwt
import datetime
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

from .models import AppUser

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM

def create_token(user_id):
    payload = {
        "user_id": user_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=72)  # Срок действия
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        user = AppUser.objects.get(id=user_id)
        return payload  #
    except jwt.ExpiredSignatureError:
        print(1)
        raise AuthenticationFailed("Token has expired")  # Истек срок действия токена
    except jwt.InvalidTokenError:
        print(2)
        raise AuthenticationFailed("Invalid token")  # Неверный токен
    except AppUser.DoesNotExist:
        print(3)
        raise AuthenticationFailed("User not found")  # Пользователь не найден



class TokenAuthenticationMixin(APIView):
    def dispatch(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        if token:
            if token.startswith("Bearer "):
                token = token[7:]
            try:
                request.user_payload = verify_token(token)
            except AuthenticationFailed as e:
                print(str(e))
                return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:  # Обработка других исключений
                print(5)
                return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print(6)
            return Response({"error": "Authorization token is required"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().dispatch(request, *args, **kwargs)
