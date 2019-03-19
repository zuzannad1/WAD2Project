from django.contrib import admin
from iFood.models import UserProfile
from iFood.models import Restaurant
from iFood.models import Product
from iFood.models import Feedback
from iFood.models import Comments
from iFood.models import OrderItem, Order



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
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Product, ProductAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','created']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)



