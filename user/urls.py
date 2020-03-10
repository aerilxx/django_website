from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views as user_views
from forum import views as forum_views
from appointment.urls import appointment_patterns

# notebook url
notebook_patterns = [
    url(r'^$',user_views.notebook, name ='notebook_index'),
    url(r'^write/$',user_views.write_note, name ='write_note'),
    url(r'^manage/$',user_views.manage_note, name ='manage_note'),
    url(r'^(?P<note_id>\w+)/$',user_views.view_note, name ='view_note'),
    url(r'^delete/(?P<note_id>\w+)/$',user_views.delete_note, name ='delete_note'),
]

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
    url(r'^delete/$', user_views.delete_user, name='delete_account'),
    url(r'^panel/$', user_views.home, name = 'panel'),
    
    url(r'^forum/$',forum_views.manage_post_by_user, name ='manage_posts'),
    
    url(r'^notebook/', include(notebook_patterns)),
    url(r'^appointment/', include(appointment_patterns)),
    
]
