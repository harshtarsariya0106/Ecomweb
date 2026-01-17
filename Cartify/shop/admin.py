from django.contrib import admin
from . models import Category, product, Contact,Orders

# Register your models here.
admin.site.register(product),
admin.site.register(Contact),
admin.site.register(Orders),
admin.site.register(Category)