from django.contrib import admin
import import_export
from .models import Profile, Message, Product, WarehouseItem
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'username')

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
    list_display = ('name', 'article')


@admin.register(WarehouseItem)
class WarehouseItemAdmin(ImportExportActionModelAdmin):
    resource_class = WarehouseItemResource
    autocomplete_fields = ['product']
    search_fields = ['product__name', 'rack']
    list_filter = ('product', 'receipt_date','rack')
    list_display = ('product', 'quantity', 'status', 'rack', 'receipt_date', 'comments')
