# Generated by Django 5.1.3 on 2024-12-22 12:48

import django.db.models.deletion
import django.db.models.functions.datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('email', models.EmailField(blank=True, max_length=256, null=True)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'app_user',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField()),
                ('text', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.question')),
            ],
            options={
                'db_table': 'option',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, max_length=4096, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'survey',
                'constraints': [models.CheckConstraint(condition=models.Q(('start_date__gte', django.db.models.functions.datetime.Now()), models.Q(('end_date__isnull', True), ('start_date__lt', models.F('end_date')), _connector='OR')), name='check_dates')],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.survey'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.appuser')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='surveys.option')),
            ],
            options={
                'db_table': 'answer',
                'unique_together': {('user', 'option')},
            },
        ),
        migrations.CreateModel(
            name='SurveyAdministrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.survey')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.appuser')),
            ],
            options={
                'db_table': 'survey_administrator',
                'unique_together': {('user', 'survey')},
            },
        ),
    ]
