from django.contrib import admin

# Register your models here.


from .models import ConfeRoom, Order,check

# Register your models here.
admin.site.register(ConfeRoom)
admin.site.register(Order)
admin.site.register(check)