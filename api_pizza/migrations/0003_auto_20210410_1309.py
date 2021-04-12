# Generated by Django 3.2 on 2021-04-10 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_pizza', '0002_cart_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='forSale',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='image',
            field=models.URLField(max_length=150, verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='ingredients',
            field=models.ManyToManyField(null=True, to='api_pizza.Ingredient'),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='image',
            field=models.URLField(max_length=150, verbose_name='Изображение'),
        ),
    ]
