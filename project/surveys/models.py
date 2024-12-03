from django.db import models
from django.db.models import Q, F


class AppUser(models.Model):
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=32)
    email = models.EmailField(max_length=256, blank=True, null=True)
    image_url = models.URLField(max_length=1024, blank=True, null=True)

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


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    type = models.IntegerField()  # Можно заменить на choices для типов вопросов
    text = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Question {self.id} in Survey {self.survey.id}"

    class Meta:
        db_table = 'question'


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    number = models.IntegerField()

    class Meta:
        db_table = 'option'
        unique_together = ('question', 'number')

    # def save(self, *args, **kwargs):
    #     if self.pk is None and self.number is None:
    #         existing_numbers = Option.objects.filter(question=self.question).values_list('number', flat=True)
    #         self.number = min(set(range(1, max(existing_numbers, default=0) + 2)) - set(existing_numbers))
    #     super().save(*args, **kwargs)


class Answer(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    class Meta:
        db_table = 'answer'
        unique_together = ('user', 'option')
