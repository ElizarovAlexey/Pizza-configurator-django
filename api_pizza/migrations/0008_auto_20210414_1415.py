# Generated by Django 3.2 on 2021-04-14 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_pizza', '0007_auto_20210414_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='count',
        ),
        migrations.AddField(
            model_name='cart',
            name='count',
            field=models.SmallIntegerField(default=1),
        ),
    ]
