# Generated by Django 2.1.15 on 2021-01-15 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date_attended',
            field=models.DateField(),
        ),
    ]
