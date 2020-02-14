from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views as user_views


urlpatterns = [
    url(r'^$', user_views.home, name='home'),
    url(r'^login/$', user_views.login_view, name='login'),
    url(r'^logout/$', user_views.logout_view, name='logout'),
    url(r'^signup/$', user_views.signup, name='signup'),
    url(r'^terms/$', user_views.terms, name='signup agreement'),
    url(r'^account_activation_sent/$', user_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_views.activate, name='activate'),
    url(r'^panel/$', user_views.home, name = 'panel'),
]
