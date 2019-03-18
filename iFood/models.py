from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime
from django.template.defaultfilters import slugify
from django.urls import reverse
import random

# Create your models here.
class Restaurant(models.Model):
	name    = models.CharField(max_length = 128)
	rating_choices = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
	rating = models.PositiveSmallIntegerField('Rating (stars)', blank=False, default=3, choices=rating_choices)
	slug    = models.SlugField(unique=True)
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Restaurant, self).save(*args, **kwargs)
    
	def __str__(self):
		return self.name

class Product(models.Model):
        name = models.CharField(max_length = 128)
        restaurant  = models.ForeignKey(Restaurant, null=True, related_name='products')
        cuisine    = models.CharField(max_length = 20, default="None")
        description = models.TextField(max_length = 300)
        price       = models.DecimalField('Pounds amount',
                                          max_digits=8, decimal_places=2, blank=True,null=True)
        slug = models.SlugField(unique=True)

        def save(self, *args, **kwargs):
                self.slug = slugify(self.id)
                super(Product, self).save(*args, **kwargs)
		
        class Meta:
                index_together = (('id','slug'),)
                ordering = ('name',)
       
        def __str__(self):
                return self.name


class UserProfile(models.Model):
        user = models.OneToOneField(User)
        address = models.CharField(max_length = 128, blank = True)
        facebook = models.URLField(default ='', blank = True)
        twitter = models.URLField(default = '', blank = True)

        def __str__(self):
                return self.user.username
	      
        
class Feedback(models.Model):
	comment    = models.TextField(blank=True, null=True)
	user       = models.ForeignKey(User, default=1)
	created_at = models.DateField(default=datetime.date.today())
	restaurant = models.ForeignKey(Restaurant)
	rating_choices = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
	rating = models.PositiveSmallIntegerField('Rating (stars)',
                                                  blank=False,
                                                  default=3,
                                                  choices=rating_choices)
	
	def __str__(self):
                return self.comment

	class Meta:
                verbose_name_plural = 'Feedback'

class Comments(models.Model):
        comment = models.TextField(blank=True, null=True)
        created_at = models.DateField(default=datetime.date.today())

        def __str__(self):
                return str(self.created_at)

        class Meta:
                verbose_name_plural = "Comments"

class Order(models.Model):
        user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
        created = models.DateField(default=datetime.date.today())
        delivery = models.CharField(default=random.randrange(35,120), max_length=3)
        def __str__(self):
                return 'Order {}'.format(self.id)

        def get_total_cost(self):
                return sum(item.get_cost() for item in self.items.all())
        
class OrderItem(models.Model):
        order = models.ForeignKey(Order, default=1, related_name='items', on_delete=models.CASCADE)
        product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        quantity = models.PositiveIntegerField(default=1)
        def __str__(self):
                return '{}'.format(self.id)

        def get_cost(self):
                return self.price * self.quantity
        


