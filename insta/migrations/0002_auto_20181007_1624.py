# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-07 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Name',
            field=models.TextField(default='Mike'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='I love instagram!'),
        ),
    ]
