from django.urls import path, include
from . import views
from .views import activation_sent_view, activate

urlpatterns = [
    path('signup/', views.register, name='register'),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    # auth.urls automatically rewinding to http://127.0.0.1:8000/users/login/
    path('', include("django.contrib.auth.urls")),
]