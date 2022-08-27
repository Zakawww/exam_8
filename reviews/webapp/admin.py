from django.contrib import admin
from .models import Product, Review


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    list_filter = ('category',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'description', 'rating')
    list_filter = ('author',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
