from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Restaurant(models.Model):
	name    = models.CharField(max_length = 128, unique=True)
	address = models.CharField(max_length = 128, unique=True)
	type    = models.CharField(max_length = 128)
	
	
class UserProfile(models.Model):
        user = models.OneToOneField(User, blank = False)
        fullname = models.CharField(max_length = 50, unique = True, blank = False)
        username = models.CharField(max_length = 30, unique = True, blank = False)
        password = models.CharField(max_length = 20, unique = True, blank = False)
        email = models.CharField(max_length = 128, unique = True)
        address = models.CharField(max_length = 128)
        facebook = models.URLField(blank = True)
        twitter = models.URLField(blank = True)
        def __str__(self):
                return self.user.username	
	
class Dishes(models.Model):
        name = models.CharField(max_length = 128, unique=True)
        restaurant  = models.ForeignKey(Restaurant, null=True, related_name='dishes')
        mealtype    = models.CharField(max_length = 20, default="None")
        description = models.CharField(max_length = 300)
        price       = models.DecimalField('Pounds amount', max_digits=8, decimal_places=2, blank=True, null=True)
        class Meta:
                verbose_name_plural = 'Dishes'
       
        def __str__(self):
                return self.name
        
class Feedback(models.Model):
	comment    = models.TextField(blank=True, null=True)
	user       = models.ForeignKey(User, default=1)
	created_at = models.DateField(default=date.today)
	restaurant = models.ForeignKey(Restaurant)
	def __str__(self):
                return self.name
	class Meta:
                verbose_name_plural = 'Feedback'

class Orders(models.Model):
	ordered_dishes = models.CharField(max_length = 150)
	restaurant     = models.CharField(max_length = 128)
	user_ID        = models.IntegerField(default = 0)
	def __str__(self):
                return self.name
	class Meta:
                verbose_name_plural = 'Orders'
        


