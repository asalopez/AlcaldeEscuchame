# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-21 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quejas', '0005_auto_20180107_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queja',
            name='fecha',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de publicación/actualización'),
        ),
    ]