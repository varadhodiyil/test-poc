from django.conf.urls import url
from mishipay.auth import views
urlpatterns = [
    url(r'^login/$', views.UserLogin.as_view(),name='login'),
    url(r'^register/$', views.UserRegistration.as_view(),name='register'),
    url(r'^logout/$', views.Logout.as_view(),name='logout'),

]