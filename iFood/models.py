from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime
from django.template.defaultfilters import slugify
from django.urls import reverse
import random

#The restaurant model
#Contains name of restaurant, rating
#and a slug created from restaurant's name
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
	
#The product model
#Model corresponding to all the dishes
#Each product (dish) has a FK - restaurant
#Cuisine, Description, Price and a slug created from dish name
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

#The userProfile model
#Each user profile has a foreign key - user
#That way each user instance of user model (the django built-in user model)
#Has a corresponding user profile
#These two are linked at signup
#User also has address and social handle fields
class UserProfile(models.Model):
        user = models.OneToOneField(User)
        address = models.CharField(max_length = 128, blank = True)
        facebook = models.URLField(default ='', blank = True)
        twitter = models.URLField(default = '', blank = True)
        picture = models.ImageField(upload_to='profile_images', blank=True)
        def __str__(self):
                return self.user.username
	      
#The feedback model - feedback about restaurant
#Each restaurant has a 1-5 star rating that users can add
#Restaurant and User models are foreign keys ->
#Each user can add feedback and each restaurant has feedback
class Feedback(models.Model):
	restaurant = models.ForeignKey(Restaurant)
	comment    = models.TextField(blank=True, null=True)
	user       = models.ForeignKey(User, default=1)
	created_at = models.DateField(default=datetime.date.today())
	rating_choices = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
	rating = models.PositiveSmallIntegerField('Rating (stars)',
                                                  blank=False,
                                                  default=3,
                                                  choices=rating_choices)
	
	def __str__(self):
                return self.restaurant

	class Meta:
                verbose_name_plural = 'Feedback'
#The comments model - feedback about the site itself
#The idea is for logged-in users to add anonymous comments and remarks
#About the site that only admins can see
class Comments(models.Model):
        comment = models.TextField(blank=True, null=True)
        created_at = models.DateField(default=datetime.date.today())

        def __str__(self):
                return str(self.created_at)

        class Meta:
                verbose_name_plural = "Comments"
                
#The order model
#A parent model containing all the orderItems
#From orderitem model
#User is a FK -> Each user has their orders
#Delivery is delivery time in minutes
#Random module used to pick the delivery time
#To avoid adding more complexity with each dish having preparation time
#As a field
class Order(models.Model):
        user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
        created = models.DateTimeField(auto_now_add=True)
        delivery = models.CharField(default=random.randrange(25,59,5), max_length=3)
        def __str__(self):
                return 'Order {}'.format(self.id)

        def get_total_cost(self):
                return sum(item.get_cost() for item in self.items.all())

#OrderItem model -> each instance of the model is the dish, its price
#And quantity
#Order is FK - each order has 1+ order items 
class OrderItem(models.Model):
        order = models.ForeignKey(Order, default=1, related_name='items', on_delete=models.CASCADE)
        product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        quantity = models.PositiveIntegerField(default=1)
        def __str__(self):
                return '{}'.format(self.id)

        def get_cost(self):
                return self.price * self.quantity
        


