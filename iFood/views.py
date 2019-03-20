from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from iFood.forms import UserForm, UserProfileForm, UserProfileEditForm
from iFood.forms import UserDetailsForm, FeedbackForm, RestaurantFeedbackForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.shortcuts import get_object_or_404
from iFood.models import Restaurant, Product, OrderItem, Order
from cart.forms import CartAddProductForm
from cart.cart import Cart
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail 

#The index page view 
def index(request):
   context_dict = {'boldmessage' : "Eat whatever you want! "}
   response = render(request, 'iFood/index.html',context = context_dict)
   return response

#The about page view
def about(request):
   context_dict = {'boldmessage' : "Welcome "}
   response = render(request, 'iFood/about.html',context = context_dict)
   return response

#The signup page view, renders two forms corresponding to User
#and UserProfile models
#Automatic log-in after successful sign-up feature added
#To facilitate and "smoothen" the process
def signup(request):
   registered = False
   template_name = 'iFood/signup.html'
   if request.method == 'POST':
      user_form = UserForm(data=request.POST)
      profile_form = UserProfileForm(data=request.POST)
      if user_form.is_valid() and profile_form.is_valid():
         user = user_form.save()
         user.set_password(user.password)
         user.save()
         profile = profile_form.save(commit=False)
         profile.user = user
         profile.save()
         registered = True
         login(request,user)
      else:
         print(user_form.errors, profile_form.errors)

   else:
      user_form = UserForm()
      profile_form = UserProfileForm()
      
   return render(request, 'iFood/signup.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

#Edit profile view
#Decorator used so that only logged in users can open the page
#Renders two forms that handle editing details of
#current user's details and user's userprofile
@login_required
def edit_profile(request):
    user = request.user
    form = UserDetailsForm(request.POST or None, instance=user)
    prof = UserProfileEditForm(request.POST or None, instance=user.userprofile)
    if request.method == 'POST':
        if form.is_valid() and prof.is_valid():
            # Save the changes but password
            form.save()
            prof.save()
            # Change password
            new_password = form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)
            return HttpResponseRedirect(reverse('account'))
    context = {"form": form, "prof":prof}

    return render(request, "iFood/user-account.html", context)
   
#User log-in view
#Handles authentication of user using built-in
#Django authentication
#Logges user in or returns an error message
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account has been disabled!")
        else:
            messages.info(request,'Invalid login details supplied. Please try again or sign up.')
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'iFood/login.html', {})
      
#Log out view
#Handles log out using built in django method
#Decorator needed, because only logged in users should
#be able to log out
@login_required     
def user_logout(request):
   logout(request)
   return HttpResponseRedirect(reverse('index'))

#The view handling comments logged-in users can add
#about the website itself
@login_required  
def web_feedback(request):
   if request.method == 'POST':
       feedback_form = FeedbackForm(request.POST)
       if feedback_form.is_valid():
          feedback = feedback_form.save()
          feedback.save()
          return redirect('web-feedback')
   else:
       feedback_form = FeedbackForm()
   return render(request, 'iFood/web-feedback.html',{'feedback_form':feedback_form})

#The restaurant view that handles all restaurant's pages
#and their menus using the slug
#invokes product_detail method which handles the add-to-cart
#form. The add to cart feature only available to logged-in users
def show_restaurant(request, restaurant_name_slug):
   context_dict = {}
   restaurant = get_object_or_404(Restaurant,slug=restaurant_name_slug)
   try:
       dishes = Product.objects.filter(restaurant=restaurant)
       context_dict['restaurant'] = restaurant
       context_dict['dishes'] = dishes
       for dish in dishes:
          form = product_detail(request, id=dish.id, slug=dish.slug)
          context_dict['form'] = form
   except restaurant.DoesNotExist:
        context_dict['restaurant'] = None
        context_dict['dishes'] = None
   return render(request, 'iFood/restaurant.html', context_dict)

#A helper method to the restaurant site that invokes add-to-cart
#form (see cart.forms) in the menus
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form}
    return cart_product_form
   
def contact(request):
    return render(request, 'iFood/contact.html',{})

#The my order view that handles creating new Order objects
#After the user has confirmed the order and paid and clears the cart
#Displays the most current order  -> the order that was just created
#Sends user email with receipt and prints receipt to terminal
#If the request is not POST (so any case user goes to my-order)
#Not through the confirmation button
#The current order is selected by finding order with highest number
#(The most recent) from user's orders and displays its details
@login_required
def my_order(request):
   user = request.user
   context = {}
   cart = Cart(request)
   #The object is created HERE
   #if the method is post so if the button is clicked
   if request.method == 'POST':
      order = Order.objects.create(user=request.user)
      for item in cart:
         OrderItem.objects.create(order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])
      cart.clear()
      context['order'] = order
      my_orders = Order.objects.filter(user=request.user)
      l = []
      for o in my_orders:
         l.append(o.id)
      current = get_object_or_404(Order, id=max(l))
      order_items = OrderItem.objects.filter(order=current)
      context['my_orders']= my_orders
      context['order_items']=order_items
      context['current']=current
      #The terminal receipt
      print("--------------------------------------")
      print("This is your order's receipt\n\n")
      print("Order ID: ", current, "\nOrder date: ", current.created)
      print("--------------------------------------")
      total = 0
      for item in order_items:
         print(item.product.name, "---- £",item.product.price, " x ", item.quantity)
         total += (item.product.price * item.quantity)
      print("Total cost:", total)
      print("--------------------------------------")
      print("\n\nTHANK YOU FOR USING IFOOD. SEE YOU SOON!\n\n\n")
      print("iFood - Eat whatever you want! - www.pythonanywhere.com/iFood\n\n\n")  
      #The email receipt
      if user.email:
         mail_body = "Hi, this is your e-receipt for order: " + str(current) + "\nOrder date: "+ str(current.created) + "\nTotal cost: £" + str(total)
         send_mail('Your iFood receipt',mail_body,
                   '2312052D@student.gla.ac.uk',[user.email],)
   else:
         my_orders = Order.objects.filter(user=request.user)
         l = []
         for o in my_orders:
            l.append(o.id)
         if not len(l)==0:
            current = get_object_or_404(Order, id=max(l))
            order_items = OrderItem.objects.filter(order=current)
            context['my_orders']= my_orders
            context['order_items']=order_items
            context['current']=current
         else:
            pass
   return render(request, 'iFood/my-order.html', context)


