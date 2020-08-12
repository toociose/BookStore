from django.contrib import admin
from .models import Users, Address, Book, Promotion, Carts, CartItem, CreditCard, Total
# Register your models here.

admin.site.register(Users)
admin.site.register(Address)
admin.site.register(Book)
admin.site.register(Promotion)
admin.site.register(CreditCard)
admin.site.register(CartItem)
admin.site.register(Carts)
admin.site.register(Total)