from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.http import HttpResponse
from iFood.forms import UserForm, UserProfileForm

def index(request):
   context_dict = {'boldmessage' : "Eats whatever you want! "}
   response = render(request, 'iFood/index.html',context = context_dict)
   return response

def about(request):
   context_dict = {'boldmessage' : "Welcome "}
   response = render(request, 'iFood/about.html',context = context_dict)
   return response
   

def signup(request):
   registered = False
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

      else:

         print(user_form.errors, profile_form.errors)
   else:
      user_form = UserForm()
      profile_form = UserProfileForm()

   return render(request,'iFood/signup.html', {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

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
         print("Invalid login details: {0}, {1}".format(username, password))
         return HttpResponse("Invalid login details supplied.")

   else:
      return render(request, 'iFood/login.html', {})
      


