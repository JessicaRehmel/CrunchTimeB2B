# Generated by Django 3.0.3 on 2020-04-21 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('B2B', '0013_auto_20200410_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='wants_ab',
        ),
    ]
