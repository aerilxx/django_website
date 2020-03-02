from django.conf.urls import url, include
from django.urls import path
from django.views.generic import TemplateView

from . import views


forum_patterns = [
    url(r'^(?P<forum_slug>[\w-]+)/$', views.forum, name='forum'),
    url(r'^(?P<forum_slug>[\w-]+)/new/$', views.new_post, name='post_in_topic'),
]

category_patterns = [
    url(r'^(?P<category_id>\w+)/$', views.category, name='category'),
    url(r'^(?P<category_id>\w+)/new/$', views.new_post_category, name='post_in_category'),
]
# change into topic in url 
post_patterns = [
    url(r'^(?P<post_id>\d+)/$', views.post, name='post'),
    url(r'^(?P<post_id>\d+)/edit/$', views.edit_post, name='post_edit'),
    url(r'^(?P<post_id>\d+)/delete/$', views.delete_post, name='post_delete'),
    url(r'^(?P<post_id>\d+)/close/$', views.close_post, name='post_close'),
]


urlpatterns = [
    url(r'^$', views.index.as_view(), name='forum_index'),
    url(r'^category/', include(category_patterns)),
    # same as forum
    url(r'^topic/', include(forum_patterns)),
    url(r'^post/', include(post_patterns)),
]
