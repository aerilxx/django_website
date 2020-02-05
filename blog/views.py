from django.shortcuts import render
from django.views import generic
from .models import Blog

# Create your views here.
class BlogMain(generic.ListView):
	queryset = Blog.objects.filter(status=1)
	post_list = Blog.objects.raw('SELECT * FROM blog_blog')
	template_name = 'blogIndex.html'

class BlogDetail(generic.DetailView):
    model = Blog
    template_name = 'blogDetail.html'

