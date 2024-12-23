# Generated by Django 5.1.3 on 2024-12-23 08:56

import django.db.models.functions.datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_alter_appuser_password'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='survey',
            name='check_dates',
        ),
        migrations.AddConstraint(
            model_name='survey',
            constraint=models.CheckConstraint(condition=models.Q(('start_date__gte', django.db.models.functions.datetime.TruncDate(django.db.models.functions.datetime.Now())), models.Q(('end_date__isnull', True), ('start_date__lte', models.F('end_date')), _connector='OR')), name='check_dates'),
        ),
    ]