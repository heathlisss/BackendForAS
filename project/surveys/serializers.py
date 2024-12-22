from rest_framework import serializers
from .models import AppUser, Survey


class AppUserSerializer(serializers.ModelSerializer):
    answered_surveys = serializers.SerializerMethodField()
    created_surveys = serializers.SerializerMethodField()

    class Meta:
        model = AppUser
        fields = ['id', 'username', 'password', 'email', 'admin', 'answered_surveys', 'created_surveys']

    def get_answered_surveys(self, obj):
        return list(Survey.objects.filter(question__option__answer__user=obj).distinct().values_list('id', flat=True))

    def get_created_surveys(self, obj):
        return list(Survey.objects.filter(surveyadministrator__user=obj).values_list('id', flat=True))

