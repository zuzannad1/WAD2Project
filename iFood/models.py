from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime
from django.template.defaultfilters import slugify

# Create your models here.
class Restaurant(models.Model):
	name    = models.CharField(max_length = 128)
	#address = models.CharField(max_length = 128)
	type    = models.CharField(max_length = 128)
	rating_choices = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
	rating = models.PositiveSmallIntegerField('Rating (stars)', blank=False, default=3, choices=rating_choices)
	slug    = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Restaurant, self).save(*args, **kwargs)
    

	def __str__(self):
		return self.name
	
# class Cuisine(models.Model):
# 	name = models.CharField(max_length = 128)
# 	class Meta:
# 		verbose_name_plural = 'cuisines'
# 		
# 	def __str__(self):
#                 return self.name
	
class UserProfile(models.Model):
        user = models.OneToOneField(User)
        address = models.CharField(max_length = 128, blank = True)
        facebook = models.URLField(default ='', blank = True)
        twitter = models.URLField(default = '', blank = True)

        def __str__(self):
                return self.user.username

class Dishes(models.Model):
        name = models.CharField(max_length = 128)
        restaurant  = models.ForeignKey(Restaurant, null=True, related_name='dishes')
        cuisine    = models.CharField(max_length = 20, default="None")
        description = models.TextField(max_length = 300)
        price       = models.DecimalField('Pounds amount', max_digits=8, decimal_places=2, blank=True, null=True)

        class Meta:
                verbose_name_plural = 'Dishes'
       
        def __str__(self):
                return self.name
        
class Feedback(models.Model):
	comment    = models.TextField(blank=True, null=True)
	user       = models.ForeignKey(User, default=1)
	created_at = models.DateField(default=datetime.date.today())
	restaurant = models.ForeignKey(Restaurant)
	rating_choices = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
	rating = models.PositiveSmallIntegerField('Rating (stars)', blank=False, default=3, choices=rating_choices)
	
	def __str__(self):
                return self.comment

	class Meta:
                verbose_name_plural = 'Feedback'

class Orders(models.Model):
	ordered_dishes = models.CharField(max_length = 150)
	restaurant     = models.CharField(max_length = 128)
	user       = models.ForeignKey(User, default=1)

	def __str__(self):
                return self.name

	class Meta:
                verbose_name_plural = 'Orders'

class Comments(models.Model):
        comment = models.TextField(blank=True, null=True)
        created_at = models.DateField(default=datetime.date.today())

        def __str__(self):
                return str(self.created_at)

        class Meta:
                verbose_name_plural = "Comments"
