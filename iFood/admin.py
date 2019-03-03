from django.contrib import admin
from iFood.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Restaurant)
admin.site.register(Dishes)
admin.site.register(Feedback)
admin.site.register(Orders)

