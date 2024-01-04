from django.db import models
from django.core.validators import MinValueValidator


# Товар для нашей витрины 
class Product(models.Model):
    # поле категории будет ссылаться на модель категории
    # все продукты в категории будут доступны через поле products
    category = models.ForeignKey(to='Category', blank=True, null=True, on_delete=models.SET_NULL, related_name='products', verbose_name='Категория')
    
    name = models.CharField(max_length=50, unique=True, verbose_name='Название') # названия товаров не должны повторяться
    description = models.TextField(verbose_name='Описание')
    quantity = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Количество')
    price = models.FloatField(validators=[MinValueValidator(0.0)], verbose_name='Цена')

    def __str__(self):
        return f'{self.name} : {self.description[:20]}. Цена: {str(self.price)}'
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товар'
        ordering = ['-price']


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, null=True, unique=True, verbose_name='Название') 

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']