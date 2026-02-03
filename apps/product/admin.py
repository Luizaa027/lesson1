from django.contrib import admin
from apps.product.models import Product, Category, Models, ProductImage

admin.site.register(Product)
admin.site.register(Models)
admin.site.register(Category)
admin.site.register(ProductImage)