from abc import abstractproperty
from django.db import models
from .rack_choices import  RACK_CHOICES


# Create your models here.

class Profile(models.Model):

    external_id = models.PositiveIntegerField(verbose_name='ID',)
    username = models.TextField(default='', verbose_name='никнейм',)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Message (models.Model):
    profile = models.ForeignKey(to='Profile', verbose_name='Профиль', on_delete=models.PROTECT)
    text = models.TextField(default='', verbose_name='текст',)
    created_at = models.DateField(verbose_name='created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'Сообщение {self.pk} от {self.profile}'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(default='', blank=True, verbose_name='Наименование')
    article = models.CharField(default='', blank=True, max_length=10, verbose_name='Артикул')
    picture = models.ImageField(upload_to='uploads/', blank=True,  default=None)
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = '1. Наименования'

    def __str__(self):
        return f'{self.name}'

class ItemProduct(models.Model):
    

    class Meta:
        abstract = True
    def __str__(self):
        return f'{self.product}'


class WarehouseItem(ItemProduct):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(null=True,verbose_name='кол-во')
    WAREHOUSE = 'Склад'
    WAIT = 'Ожидается'

    STATUS_CHOICES = [
        (WAREHOUSE, 'На Складе'),
        (WAIT, 'Ожидается'),
        ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=WAREHOUSE, verbose_name='Статус')   
    rack = models.CharField(max_length=10, choices=RACK_CHOICES, default='', verbose_name='Место') 
    receipt_date = models.DateField(default='', editable=True, null=True, blank=True, verbose_name='Дата прибытия')
    comments = models.TextField(default='', null=True, blank=True, verbose_name='Комментарий')
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = '2. Товары'

    def __str__(self):
        return '"{}" - {} шт | {}'.format(self.product.name, self.quantity, self.rack)
        