# Generated by Django 3.0.4 on 2020-04-05 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('B2B', '0005_auto_20200405_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='wants_tb',
            field=models.BooleanField(verbose_name='Needs search results from Test Bookstore? (for TESTING purposes ONLY)'),
        ),
    ]
