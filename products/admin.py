# products/admin.py
from django.contrib import admin
from .models import Product, ProductImage , Collection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date')
    prepopulated_fields = {'slug': ('title',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('filename', 'alt_text', 'order', 'image_type')
    ordering = ('order',)
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'categories', 'gender', 'price','id' ,  'collection', 'stock', 'review' )
    list_filter = ('categories', 'gender', 'collection')
    search_fields = ('title', 'description_text')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]
    ordering = ('-title',)
    list_per_page = 20


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'filename', 'image_type', 'order')
    list_filter = ('image_type',)
    search_fields = ('filename', 'alt_text', 'product__title')
    ordering = ('product', 'order')
