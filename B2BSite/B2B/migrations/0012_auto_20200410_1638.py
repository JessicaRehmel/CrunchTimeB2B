# Generated by Django 3.0.4 on 2020-04-10 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('B2B', '0011_auto_20200410_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='wants_ab',
            field=models.BooleanField(verbose_name='can search Audiobooks.com'),
        ),
        migrations.AlterField(
            model_name='company',
            name='wants_gb',
            field=models.BooleanField(verbose_name='can search Google Books'),
        ),
        migrations.AlterField(
            model_name='company',
            name='wants_kb',
            field=models.BooleanField(verbose_name='can search Kobo'),
        ),
        migrations.AlterField(
            model_name='company',
            name='wants_lc',
            field=models.BooleanField(verbose_name='can search Livraria Cultura'),
        ),
        migrations.AlterField(
            model_name='company',
            name='wants_sd',
            field=models.BooleanField(verbose_name='can search Scribd'),
        ),
        migrations.AlterField(
            model_name='company',
            name='wants_tb',
            field=models.BooleanField(verbose_name='can search Test Bookstore (for TESTING purposes ONLY)'),
        ),
    ]
