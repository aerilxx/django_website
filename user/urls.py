from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views as user_views
from forum import views as forum_views

urlpatterns = [
    url(r'^$', user_views.home, name='user_home'),
    url(r'^login/$', user_views.login_view, name='login'),
    url(r'^logout/$', user_views.logout_view, name='logout'),
    url(r'^signup/$', user_views.signup, name='signup'),
    url(r'^terms/$', user_views.terms, name='signup agreement'),
    url(r'^edit/$', user_views.edit_profile_view, name='edit'),
    url(r'^account_activation_sent/$', user_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_views.activate, name='activate'),
    url(r'^panel/$', user_views.home, name = 'panel'),
    url(r'^forum/$',forum_views.manage_post_by_user, name ='manage_posts')
    # url(r'^profile/', user_views.userProfile.as_view(), name="user_single_profile"),
]
