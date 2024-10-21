from django.contrib import admin
from LittleLemonAPI .models import Category, MenuItem, Cart, Order, OrderItem

# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Cart)   
admin.site.register(Order)
admin.site.register(OrderItem)   