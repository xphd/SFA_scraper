# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 15:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bingScraper', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='Profile',
        ),
    ]
