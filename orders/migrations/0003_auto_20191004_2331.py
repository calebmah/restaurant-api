# Generated by Django 2.2.5 on 2019-10-04 15:31

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20191004_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitems',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=32, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
