# Generated by Django 3.1.3 on 2020-11-05 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_auto_20201105_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='stock',
            field=models.ManyToManyField(to='stock.Stock'),
        ),
    ]
