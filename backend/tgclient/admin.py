from django.contrib import admin
from django.utils.safestring import mark_safe
import import_export
from .models import ProfileTelegram, Message, Product, WarehouseItem
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
from django.utils.html import format_html
# Register your models here.

@admin.register(ProfileTelegram)
class ProfileTelegramAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'tg_username')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'text', 'created_at')

#@admin.register(Product)
#class ProductAdmin(admin.ModelAdmin):
#    list_display = ('name', 'article')
#
class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        exclude = ('id')
        skip_unchanged = True
        import_id_fields = ('name', 'article')
        

class WarehouseItemResource(resources.ModelResource):
    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'name')
        )
    class Meta:
        model = WarehouseItem
        exclude = ('id')
        skip_unchanged = True
        import_id_fields = ('product', 'quantity', 'status', 'rack', )
        


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    search_fields = ['name', 'article']
    list_display = ('name','info', 'article',)


@admin.register(WarehouseItem)
class WarehouseItemAdmin(ImportExportActionModelAdmin):
    resource_class = WarehouseItemResource
    autocomplete_fields = ['product']
    search_fields = ['product__name', 'rack']
    list_filter = ('product', 'receipt_date','rack')
    readonly_fields = ['get_image']
    list_display = ('product', 'quantity', 'status', 'rack', 'receipt_date', 'comments',)
        
    def get_image(self, obj):
            return format_html('<img src="{}" width="100" height="auto"/>'.format(obj.qr_code.url))

    get_image.short_description = 'Превью'
    get_image.allow_tags = True
    def image_data(self, obj):
        return format_html(
            '<img src="{}" width="100px"/>',
            obj.qr_code.path,
        )
    image_data.short_description = u'picture'
    
    