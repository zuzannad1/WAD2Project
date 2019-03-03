from django.contrib import admin
from iFood.models import UserProfile
from iFood.models import Restaurant
from iFood.models import Dishes
from iFood.models import Feedback
from iFood.models import Orders


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Restaurant)
admin.site.register(Dishes)
admin.site.register(Feedback)
admin.site.register(Orders)

