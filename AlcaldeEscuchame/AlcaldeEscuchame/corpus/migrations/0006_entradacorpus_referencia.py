# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-09 16:22
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0005_entradacorpus_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='entradacorpus',
            name='referencia',
            field=models.CharField(blank=True, default='', max_length=7, null=True, validators=[django.core.validators.RegexValidator(message='La referencia no cumple el patrón solicitado.', regex='^([a-zA-Z]{2})-([a-zA-Z0-9]{4})$')]),
        ),
    ]
