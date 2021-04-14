from django.db import models


class Size(models.Model):
    """ Размеры """
    value = models.SmallIntegerField('Размер', default=25)
    cost = models.SmallIntegerField('Цена', default=0)

    def __str__(self):
        return str(self.value)


class Dough(models.Model):
    """ Тесто """
    type = models.CharField('Тесто', max_length=50)
    cost = models.SmallIntegerField('Цена', default=0)

    def __str__(self):
        return self.type


class Ingredient(models.Model):
    """ Ингредиенты """
    value = models.CharField('Ингредиент', max_length=50)
    cost = models.SmallIntegerField('Цена', default=0)

    def __str__(self):
        return self.value


class Pizza(models.Model):
    """ Пиццы """

    name = models.CharField('Название', max_length=50)
    description = models.TextField('Описание', max_length=250)
    image = models.URLField('Изображение', max_length=150)
    dough = models.ForeignKey(Dough, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    cost = models.PositiveIntegerField('Цена', default=0)
    forSale = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Drink(models.Model):
    """ Напитки """

    name = models.CharField('Название', max_length=50)
    image = models.URLField('Изобрание', max_length=150)
    description = models.TextField('Описание', max_length=250)
    cost = models.PositiveIntegerField('Цена', default=0)

    def __str__(self):
        return self.name


class Dessert(models.Model):
    """ Дессерты """

    name = models.CharField('Название', max_length=50)
    image = models.URLField('Изобрание', max_length=150)
    description = models.TextField('Описание', max_length=250)
    cost = models.PositiveIntegerField('Цена', default=0)

    def __str__(self):
        return self.name


class IntermediateCart(models.Model):
    """ Промежуточная корзина """

    name = models.CharField('Название', max_length=50)
    image = models.URLField('Изображение', max_length=150)
    dough = models.ForeignKey(Dough, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, related_name='intermediate_ingredients')
    additionalIngredients = models.ManyToManyField(Ingredient, related_name='intermediate_addIngredients')
    cost = models.PositiveIntegerField('Цена', default=0)
    sold = models.BooleanField(default=False)


class Cart(models.Model):
    """ Корзина """

    name = models.CharField('Название', max_length=50)
    image = models.URLField('Изображение', max_length=150)
    dough = models.ForeignKey(Dough, on_delete=models.CASCADE, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredients', null=True)
    additionalIngredients = models.ManyToManyField(Ingredient, related_name='addIngredients', null=True)
    cost = models.PositiveIntegerField('Цена', default=0)
    count = models.SmallIntegerField(default=1)
    sold = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cart'
