# Generated by Django 3.1.3 on 2020-11-06 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bucket', '0002_auto_20201106_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucket',
            name='confirmed',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
