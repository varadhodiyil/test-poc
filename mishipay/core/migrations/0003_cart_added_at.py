# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-08-25 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20180825_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='added_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
