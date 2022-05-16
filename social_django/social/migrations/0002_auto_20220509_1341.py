# Generated by Django 3.1.2 on 2022-05-09 18:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuarios',
            options={},
        ),
        migrations.RemoveField(
            model_name='usuarios',
            name='usuario',
        ),
        migrations.AddField(
            model_name='usuarios',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='usuarios',
            name='password',
            field=models.CharField(default=django.utils.timezone.now, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuarios',
            name='username',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, unique=True, verbose_name='Nombre usuario'),
            preserve_default=False,
        ),
    ]
