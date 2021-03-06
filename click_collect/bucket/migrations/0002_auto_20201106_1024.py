# Generated by Django 3.1.3 on 2020-11-06 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0012_auto_20201106_1020'),
        ('bucket', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bucket',
            name='quantity',
        ),
        migrations.CreateModel(
            name='BucketItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('bucket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bucket.bucket')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.product')),
            ],
        ),
    ]
