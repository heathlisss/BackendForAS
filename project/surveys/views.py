from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import AppUser, Survey, SurveyAdministrator, Question, Option
from .serializers import AppUserSerializer, SurveySerializer, QuestionSerializer, OptionSerializer


class UserView(APIView):

    def post(self, request):
        data = request.data
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = AppUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            response_data.pop('password', None)
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = AppUser.objects.get(pk=pk)
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
        except AppUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, pk):
        try:
            user = AppUser.objects.get(pk=pk)
        except AppUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = AppUserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            response_data.pop('password', None)
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk):
        user = get_object_or_404(AppUser, pk=pk)
        serializer = AppUserSerializer(user)
        response_data = serializer.data
        response_data.pop('password', None)
        return Response(response_data, status=status.HTTP_200_OK)


class UserViewLogIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = AppUser.objects.get(username=username)
        except AppUser.DoesNotExist:
            return Response({"error": "Invalid username"}, status=status.HTTP_404_NOT_FOUND)

        if check_password(password, user.password):
            response_data = AppUserSerializer(user).data
            response_data.pop('password', None)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)


class UserAllView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            survey_admins = SurveyAdministrator.objects.filter(survey_id=pk).select_related('user')
            if not survey_admins.exists():
                return Response({"message": "No administrators found for this survey."}, status=status.HTTP_404_NOT_FOUND)
            admins_data = AppUserSerializer([admin.user for admin in survey_admins], many=True).data
            for admin in admins_data:
                admin.pop('password', None)
            return Response(admins_data, status=status.HTTP_200_OK)
        else:
            users = AppUser.objects.all()
            users_data = AppUserSerializer(users, many=True).data
            for user in users_data:
                user.pop('password', None)
            return Response(users_data, status=status.HTTP_200_OK)


class SurveyView(APIView):

    def post(self, request):
        data = request.data
        serializer = SurveySerializer(data=data)
        if serializer.is_valid():
            survey = serializer.save()
            admin_user_ids = request.data.get('admins', [])
            successful_admins = []
            for user_id in admin_user_ids:
                try:
                    admin = AppUser.objects.get(id=user_id)
                    SurveyAdministrator.objects.create(user=admin, survey=survey)
                    successful_admins.append(user_id)
                except AppUser.DoesNotExist:
                    continue  # Игнорируем несуществующих администраторов
            response_data = serializer.data
            response_data["admins"] = successful_admins
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk)
        survey.delete()
        return Response({"message": "Survey deleted successfully"}, status=status.HTTP_200_OK)

    def get(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk)
        serializer = SurveySerializer(survey)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk)
        serializer = SurveySerializer(survey, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SurveyAllView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            admin_surveys = SurveyAdministrator.objects.filter(user_id=pk).select_related('survey')
            surveys = [admin.survey for admin in admin_surveys]
            if not surveys:
                return Response({"message": "No surveys found for this user."}, status=status.HTTP_404_NOT_FOUND)
            surveys_data = SurveySerializer(surveys, many=True).data
            return Response(surveys_data, status=status.HTTP_200_OK)
        else:
            surveys = Survey.objects.all()
            surveys_data = SurveySerializer(surveys, many=True).data
            return Response(surveys_data, status=status.HTTP_200_OK)


class QuestionView(APIView):

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = serializer.errors
            if 'survey' in errors and isinstance(errors['survey'], list):
                if 'Invalid pk' in errors['survey'][0]:
                    return Response({"error": "Survey with the provided ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        question.delete()
        return Response({"message": "Question deleted successfully"}, status=status.HTTP_200_OK)


    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = serializer.errors
            if 'survey' in errors and isinstance(errors['survey'], list):
                for error in errors['survey']:
                    if "Invalid pk" in error:
                        return Response({"error": "Survey with the provided ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionAllView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            try:
                survey = Survey.objects.get(pk=pk)
            except Survey.DoesNotExist:
                return Response({"error": "Survey not found."}, status=status.HTTP_404_NOT_FOUND)
            questions = Question.objects.filter(survey=survey)
            questions_data = QuestionSerializer(questions, many=True).data
            return Response(questions_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Survey ID is required."}, status=status.HTTP_400_BAD_REQUEST)


class OptionView(APIView):

    def post(self, request):
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = serializer.errors
            if 'question' in errors and isinstance(errors['question'], list):
                if 'Invalid pk' in errors['question'][0]:
                    return Response({"error": "Question with the provided ID does not exist."},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            option = Option.objects.get(pk=pk)
            option.delete()
            return Response({"message": "Option deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Option.DoesNotExist:
            return Response({"error": "Option not found."}, status=status.HTTP_404_NOT_FOUND)


    def get(self, request, pk):
        try:
            option = Option.objects.get(pk=pk)
            serializer = OptionSerializer(option)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Option.DoesNotExist:
            return Response({"error": "Option not found."}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, pk):
        try:
            option = Option.objects.get(pk=pk)
        except Option.DoesNotExist:
            return Response({"error": "Option not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = OptionSerializer(option, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = serializer.errors
            if 'question' in errors and isinstance(errors['question'], list):
                for error in errors['question']:
                    if "Invalid pk" in error:
                        return Response({"error": "Question with the provided ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class OptionAllView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            try:
                question = Question.objects.get(pk=pk)
            except Question.DoesNotExist:
                return Response({"error": "Question not found."}, status=status.HTTP_404_NOT_FOUND)
            options = Option.objects.filter(question=question)
            options_data = OptionSerializer(options, many=True).data
            return Response(options_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Question ID is required."}, status=status.HTTP_400_BAD_REQUEST)
