# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0002_auto_20171202_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='corpus',
            name='nombre',
            field=models.CharField(help_text='Requerido. 80 carácteres como máximo.', max_length=80, null=True),
        ),
    ]
