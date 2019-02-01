from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Menu)

admin.site.register(Token)
admin.site.register(TokenItem)

admin.site.register(OrderList)
admin.site.register(OrderedItem)

admin.site.register(History)

admin.site.register(WeightBuffer)