from django.contrib import admin
from iFood.models import UserProfile
from iFood.models import Restaurant
from iFood.models import Product
from iFood.models import Feedback
from iFood.models import Comments



# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Feedback)
admin.site.register(Comments)


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name','slug','rating']
    list_editable = ['rating']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Restaurant, RestaurantAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','restaurant','cuisine','description','price']
    list_editable = ['price']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Product, ProductAdmin)

