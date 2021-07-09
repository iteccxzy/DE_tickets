from django.contrib import admin


from .models import Orders, Offices, Customers, Business, Plans

# Register your models here.

admin.site.register(Orders)
admin.site.register(Offices)
admin.site.register(Customers)
admin.site.register(Business)
admin.site.register(Plans)