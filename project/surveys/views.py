from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import AppUser, Survey
from .serializers import AppUserSerializer

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


