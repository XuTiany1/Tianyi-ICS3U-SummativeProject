# Generated by Django 2.1.15 on 2021-01-15 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210115_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_student',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]
