"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url, include
from . import views
from contact import views as contact_views
from forum import views as forum_views
from contact.views import Questions

from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='index'),
    path('about/',views.about , name="about"),
    path('service/', views.service, name ="service"),
    path('resource/', include('blog.urls'), name="resource"),
    path('contact/', include('contact.urls'), name="contact"),
    path('privacy/', views.privacy, name ="privacy"),
    path('user/', include('user.urls'), name="users"),
    path('questions/', contact_views.Questions.as_view(), name="qestions"),
    path('forum/', include('forum.urls'), name ="forum"),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
