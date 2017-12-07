# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 10:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
        ('quejas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now=True, verbose_name='Fecha de creación')),
                ('titulo', models.CharField(help_text='Requerido. 80 carácteres como máximo.', max_length=80)),
                ('cuerpo', models.TextField(help_text='Requerido. 500 carácteres como máximo.', max_length=500)),
                ('comentario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.Actor')),
                ('queja', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quejas.Queja')),
            ],
        ),
    ]