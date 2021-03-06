# Generated by Django 3.0.4 on 2020-04-10 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('B2B', '0010_auto_20200410_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='wants_ab',
            field=models.BooleanField(verbose_name='search Audiobooks.com'),
        ),
        migrations.AlterField(
            model_name='company',
            name='wants_gb',
            field=models.BooleanField(verbose_name='search Google Books'),
        ),
        migrations.AlterField(
            model_name='company',
            name='wants_kb',
            field=models.BooleanField(verbose_name='search Kobo'),
        ),
        migrations.AlterField(
            model_name='company',
            name='wants_lc',
            field=models.BooleanField(verbose_name='search Livraria Cultura'),
        ),
        migrations.AlterField(
            model_name='company',
            name='wants_sd',
            field=models.BooleanField(verbose_name='search Scribd'),
        ),
        migrations.AlterField(
            model_name='company',
            name='wants_tb',
            field=models.BooleanField(verbose_name='search Test Bookstore (for TESTING purposes ONLY)'),
        ),
    ]
