# Generated by Django 3.2 on 2021-04-14 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_pizza', '0006_auto_20210410_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='additionalIngredients',
            field=models.ManyToManyField(null=True, related_name='addIngredients', to='api_pizza.Ingredient'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='dough',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_pizza.dough'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='ingredients',
            field=models.ManyToManyField(null=True, related_name='ingredients', to='api_pizza.Ingredient'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_pizza.size'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='sold',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='dessert',
            name='image',
            field=models.URLField(max_length=150, verbose_name='Изобрание'),
        ),
        migrations.AlterField(
            model_name='drink',
            name='image',
            field=models.URLField(max_length=150, verbose_name='Изобрание'),
        ),
    ]
