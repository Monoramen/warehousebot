from abc import abstractproperty
from re import T
from django.core.files import storage
from django.db import models
from .rack_choices import  RACK_CHOICES
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.core.files.storage import FileSystemStorage
# Create your models here.

media = FileSystemStorage(location='media')


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
    name = models.CharField(default='', blank=True, max_length=100, verbose_name='Наименование')
    info = models.TextField(default='', blank=True, verbose_name='Информация')
    article = models.CharField(default='', blank=True, max_length=10, verbose_name='Артикул')
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



#Товар на полке и его количество на складе
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
    qr_code = models.ImageField(storage=media,  upload_to='uploads/qr_codes/%d-%m-%Y', blank=True, null=True,)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = '2. Товары'

    def __str__(self):
        return '"{}" - {} шт | {}'.format(self.product.name, self.quantity, self.rack)

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=8,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=1,
        )
        qr.add_data(self.product.name)
        qr.make(fit = True)
        qrcode_img = qr.make_image(fill_color = "black", back_color = '#d4f4f5')
        print(qrcode_img.size)
        
        canvas = Image.new('RGB', (qrcode_img.size), 'white')
        canvas.paste(qrcode_img)
        canvas.convert('RGBA')
        fname = f'qr_code-{self.id}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
