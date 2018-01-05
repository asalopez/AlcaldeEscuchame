# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-28 19:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0012_auto_20171216_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administrador',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='ciudadano',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='funcionario',
            name='usuario',
        ),
        migrations.AddField(
            model_name='actor',
            name='usuario',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
