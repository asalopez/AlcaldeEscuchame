# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-07 15:46
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quejas', '0003_auto_20171202_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valoracion',
            name='puntuacion',
            field=models.IntegerField(help_text='Requerido. Rango de 0 a 5 (inclusives).', validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]