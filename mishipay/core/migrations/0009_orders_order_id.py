# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-26 08:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180826_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='order_id',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
