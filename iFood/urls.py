from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from iFood import views


#app_name = 'iFood'


urlpatterns = [ 
	url(r'^$', views.index, name='index'),
	url(r'about/$', views.about, name='about'),
	url(r'^signup/$',views.signup,name='signup'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^web-feedback/$', views.web_feedback, name='web-feedback'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^account/$', views.edit_profile, name ='account'),
	url(r'^my-order/$', views.my_order, name='my-order'),
	url(r'^restaurant-feedback/$', views.restaurant_feedback, name='restaurant-feedback'),
    url(r'^(?P<restaurant_name_slug>[\w\-]+)/$',
        views.show_restaurant, name='restaurant'),     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
