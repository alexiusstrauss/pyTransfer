# Generated by Django 3.2.6 on 2021-08-06 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pytransfer', '0006_auto_20210806_0503'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=5, default=0, max_digits=12, null=True)),
                ('cancelado', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pytransfer.pessoa')),
            ],
        ),
    ]
