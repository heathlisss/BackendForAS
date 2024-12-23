from django.urls import path
from .views import UserView, UserViewLogIn, SurveyView, UserAllView, SurveyAllView

urlpatterns = [
    path('api/users/', UserView.as_view(), name='user_create'),  # POST - Создание пользователя
    path('api/users/<int:pk>/', UserView.as_view(), name='user_detail'),  # GET - Информация о пользователе, PUT - Обновление, DELETE - Удаление
    path('api/login/', UserViewLogIn.as_view(), name='user_login'),
    path('api/users/all/', UserAllView.as_view(), name='all_users'),  # GET - Получение всех пользователей
    path('api/users/survey/<int:pk>/', UserAllView.as_view(), name='survey_admins'), # GET - Получение администраторов опроса по ID

    path('api/surveys/', SurveyView.as_view(), name='survey_list_create'), #POST - Создание опроса
    path('api/surveys/<int:pk>/', SurveyView.as_view(), name='survey_detail'),  # PUT - Обновление опроса, DELETE - Удаление опроса, GET - один опрос
    path('api/surveys/all/', SurveyAllView.as_view(), name='survey_all'),  # GET - Все опросы
    path('api/surveys/user/<int:pk>/', SurveyAllView.as_view(), name='admins_survey'), # GET - Все опросы пользователя


]

