from django.urls import path
from .views import UserView, UserViewLogIn

urlpatterns = [
    path('api/users/', UserView.as_view(), name='user_create'),  # POST - Создание пользователя
    path('api/users/<int:pk>/', UserView.as_view(), name='user_detail'),  # GET - Информация о пользователе, PUT - Обновление, DELETE - Удаление
    path('api/login/', UserViewLogIn.as_view(), name='user_login')
]

