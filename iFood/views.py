from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.http import HttpResponse
from iFood.forms import UserProfiles, UpdateProfile
from django.contrib import messages
from django.shortcuts import render

from django.shortcuts import render_to_response

def index(request):
   context_dict = {'boldmessage' : "Eats whatever you want! "}
   response = render(request, 'iFood/index.html',context = context_dict)
   return response

def about(request):
   context_dict = {'boldmessage' : "Welcome "}
   response = render(request, 'iFood/about.html',context = context_dict)
   return response


def signup(request):
    if request.method == 'POST':
        form = UserProfiles(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            fullname = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            form.save()
            if request.user.is_authenticated():
               instance.user.add(request.user)
            # change it to redirect to login
            # and authenticate when login template
            # is ready
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserProfiles()

    context = {'form': form}

    return render(request, 'iFood/signup.html', context)

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

@login_required     
def user_logout(request):
   logout(request)
   return HttpResponseRedirect(reverse('index'))

@login_required
def account(request):
    if request.method == "POST":
       form = UpdateProfile(data=request.POST, instance=request.user)
       if form.is_valid():
           form.save()
    else:
       form = UpdateProfile()

    return render(request, "iFood/user-account.html", {'form':form})


@login_required
def delete_user(request, username):
    context = {}
    try:
        user = User.object.get(username=username)
        user.is_active = False
        user.save()
        context['msg'] = 'Profile successfully disabled.'
    except Exception as e:
        context['msg'] = e.message

    return render(request, 'iFood/user-account.html',context=context)

@login_required
def web_feedback(request):
   pass

def contact(request):
   pass


