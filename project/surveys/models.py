from django.db import models
from django.db.models import Q, F


class AppUser(models.Model):
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=256, blank=True, null=True)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'app_user'


class Survey(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=4096, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        Answer.objects.filter(option__question__survey=self).delete()
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'survey'
        constraints = [
            models.CheckConstraint(
                check=(
                        Q(start_date__gte=models.functions.Now()) &
                        (Q(end_date__isnull=True) | Q(start_date__lt=F('end_date')))
                ),
                name='check_dates'
            )
        ]


class SurveyAdministrator(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    class Meta:
        db_table = 'survey_administrator'
        unique_together = ('user', 'survey')


class  Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    type = models.IntegerField()  # Можно заменить на choices для типов вопросов
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Question {self.id} in Survey {self.survey.id}"

    class Meta:
        db_table = 'question'


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'option'


class Answer(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.PROTECT)

    class Meta:
        db_table = 'answer'
        unique_together = ('user', 'option')
