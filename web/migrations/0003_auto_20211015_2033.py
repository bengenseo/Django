# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-10-15 12:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20211015_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archives',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
    ]
