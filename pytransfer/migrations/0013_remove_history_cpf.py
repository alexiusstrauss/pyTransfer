# Generated by Django 3.2.6 on 2021-08-06 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pytransfer', '0012_history_cpf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='cpf',
        ),
    ]
