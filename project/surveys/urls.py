from django.urls import path
from .views import UserView, UserViewLogIn, SurveyView, UserAllView, SurveyAllView, QuestionView, QuestionAllView, \
    OptionView, OptionAllView

urlpatterns = [
    path('api/users/', UserView.as_view(), name='user_create'),  # POST - Создание пользователя
    path('api/users/<int:pk>/', UserView.as_view(), name='user_detail'),  # GET - Информация о пользователе, PUT - Обновление, DELETE - Удаление
    path('api/login/', UserViewLogIn.as_view(), name='user_login'),
    path('api/users/all/', UserAllView.as_view(), name='all_users'),  # GET - Получение всех пользователей
    path('api/users/survey/<int:pk>/', UserAllView.as_view(), name='survey_admins'), # GET - Получение администраторов опроса по ID

    path('api/surveys/', SurveyView.as_view(), name='survey_create'), #POST - Создание опроса
    path('api/surveys/<int:pk>/', SurveyView.as_view(), name='survey_detail'),  # PUT - Обновление опроса, DELETE - Удаление опроса, GET - один опрос
    path('api/surveys/all/', SurveyAllView.as_view(), name='survey_all'),  # GET - Все опросы
    path('api/surveys/user/<int:pk>/', SurveyAllView.as_view(), name='admins_survey'), # GET - Все опросы пользователя

    path('api/questions/', QuestionView.as_view(), name='question_create'),  # POST - Создание вопроса
    path('api/questions/<int:pk>/', QuestionView.as_view(), name='question_detail'),  # GET - Один вопрос, PUT - Изменение, DELETE - Удаление
    path('api/questions/survey/<int:pk>/', QuestionAllView.as_view(), name='questions_survey'),  # GET - Все вопросы опроса

    path('api/options/', OptionView.as_view(), name='option_create'),  # POST - создание,
    path('api/options/<int:pk>/', OptionView.as_view(), name='option_detail'),  # GET, PUT, DELETE
    path('api/options/question/<int:pk>/', OptionAllView.as_view(), name='options_question'),  #GET - все варианты (по question_id)

]

