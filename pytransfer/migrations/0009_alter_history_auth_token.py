# Generated by Django 3.2.6 on 2021-08-06 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pytransfer', '0008_auto_20210806_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='auth_token',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
