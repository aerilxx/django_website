from . import views
from django.urls import path

urlpatterns = [
    path('', views.BlogMain.as_view(), name='home'),
    path('<slug:slug>/', views.BlogDetail.as_view(), name='post_detail'),
]