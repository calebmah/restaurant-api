# Generated by Django 2.2.5 on 2019-10-07 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20191004_2345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='option',
            new_name='item',
        ),
    ]