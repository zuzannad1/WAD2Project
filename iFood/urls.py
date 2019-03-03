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
    url(r'^account/$', views.account, name ='account'),
]
