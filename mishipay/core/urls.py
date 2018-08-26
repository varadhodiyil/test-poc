from django.conf.urls import url
from mishipay.core import views


urlpatterns = [
    url(r'dashboard/$', views.Dashboard.as_view(),name='dashboard'),
    url(r'^cart/(?P<cart>\d+)/$',views.UpdateCart.as_view(),name='update_cart'),
    url(r'^cart/$', views.Cart.as_view(),name='cart'),
    url(r'^profile/$', views.Profile.as_view(),name='profile'),
    url(r'^orders/$', views.Orders.as_view(),name='orders'),
]