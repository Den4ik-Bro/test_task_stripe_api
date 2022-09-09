from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.IntegerField(default=0, verbose_name='цена')
    stripe_product_id = models.CharField(max_length=100)
    stripe_price_id = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name