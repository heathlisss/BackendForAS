from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import AppUser, Survey, SurveyAdministrator
from .serializers import AppUserSerializer, SurveySerializer


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



class SurveyView(APIView):

    def post(self, request):
        data = request.data
        serializer = SurveySerializer(data=data)
        if serializer.is_valid():
            survey = serializer.save()
            admin_user_ids = request.data.get('admins', [])
            errors = []
            for user_id in admin_user_ids:
                try:
                    admin = AppUser.objects.get(id=user_id)
                    SurveyAdministrator.objects.create(user=admin, survey=survey)
                except AppUser.DoesNotExist:
                    errors.append(f"User with id {user_id} does not exist.")

            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk)
        survey.delete()
        return Response({"message": "Survey deleted successfully"}, status=status.HTTP_200_OK)


    def get(self, request):
        user_id = request.query_params.get('user_id')  # Получаем id пользователя из параметров запроса
        if user_id:
            surveys = Survey.objects.filter(surveyadministrator__user__id=user_id)
        else:
            surveys = Survey.objects.all()

        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk)
        serializer = SurveySerializer(survey, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)