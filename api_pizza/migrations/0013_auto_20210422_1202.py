# Generated by Django 3.2 on 2021-04-22 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_pizza', '0012_auto_20210422_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='dessert',
            name='discount',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='drink',
            name='discount',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pizza',
            name='discount',
            field=models.BooleanField(default=False),
        ),
    ]
