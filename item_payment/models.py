from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.IntegerField(default=0, verbose_name='цена')
    stripe_product_id = models.CharField(max_length=100)
    stripe_price_id = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=1, verbose_name='количество')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='клиент')
    items = models.ManyToManyField(Item, verbose_name='товары')
