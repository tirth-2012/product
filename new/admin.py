from django.contrib import admin
from .models import Product,category,SubCategory

# Register your models here.

admin.site.register(Product)
admin.site.register(category)
admin.site.register(SubCategory)
