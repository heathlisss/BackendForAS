from django.utils.timezone import now as django_now
from rest_framework import serializers

from .models import AppUser, Survey, Question, SurveyAdministrator, Option, Answer


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


class SurveySerializer(serializers.ModelSerializer):
    #questions = serializers.SerializerMethodField()
    admins = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'admins', 'number_of_respondents']

    # def get_questions(self, obj):
    #     return list(Question.objects.filter(survey=obj).distinct().values_list('id', flat=True))

    def get_admins(self, obj):
        return list(SurveyAdministrator.objects.filter(survey=obj).values_list('user_id', flat=True))

    def get_number_of_respondents(self, obj):
        return obj.answer_user_set.count()

    def validate(self, data):
        instance = self.instance
        current_start_date = instance.start_date if instance else None
        current_end_date = instance.end_date if instance else None

        start_date = data.get('start_date', current_start_date)
        end_date = data.get('end_date', current_end_date)
        if start_date and start_date < django_now().date():
            raise serializers.ValidationError({"error_start_date": "The start date cannot be in the past."})
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError({"error_end_date": "The end date must be later than the start date."})
        return data


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'survey', 'text']

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.survey = validated_data.get('survey', instance.survey)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class OptionSerializer(serializers.ModelSerializer):
    selected_count = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ['id', 'question', 'text', 'selected_count']

    def get_selected_count(self, obj):
        return obj.answer_set.count()  # Подсчёт количества раз, когда вариант был выбран
