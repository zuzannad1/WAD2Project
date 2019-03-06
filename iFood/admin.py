from django.contrib import admin
from iFood.models import UserProfile
from iFood.models import Restaurant
from iFood.models import Dishes
from iFood.models import Feedback
from iFood.models import Orders
from iFood.models import Comments


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Dishes)
admin.site.register(Feedback)
admin.site.register(Orders)
admin.site.register(Comments)

class RestaurantAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Restaurant, RestaurantAdmin)

