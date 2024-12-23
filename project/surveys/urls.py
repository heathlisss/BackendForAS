from django.urls import path
from .views import UserView, UserViewLogIn, SurveyView

urlpatterns = [
    path('api/users/', UserView.as_view(), name='user_create'),  # POST - Создание пользователя
    path('api/users/<int:pk>/', UserView.as_view(), name='user_detail'),  # GET - Информация о пользователе, PUT - Обновление, DELETE - Удаление
    path('api/login/', UserViewLogIn.as_view(), name='user_login'),
    path('api/surveys/', SurveyView.as_view(), name='survey_list_create'), #POST - Создание опроса
    path('api/surveys/<int:pk>/', SurveyView.as_view(), name='survey_detail'),  # PUT - Обновление опроса, DELETE - Удаление опроса, GET - один опрос
]

