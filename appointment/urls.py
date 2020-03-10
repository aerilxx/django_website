from django.conf.urls import url
from . import views as views


# appointment url
appointment_patterns=[
    url(r'^$',views.manage_appointment, name ='appointment_index'),
    url(r'^make/$',views.make_appointment, name ='make_management'),
    url(r'^delete/(?P<appointment_id>\w+)/$', views.delete_appointment, 
                                           name ='delete_appointment'),
    url(r'^update/(?P<appointment_id>\w+)/$', views.update_appointment, 
                                           name ='update_appointment'),
    url(r'^view/(?P<appointment_id>\w+)/$', views.view_appointment, 
                                           name ='view_appointment'),
]

