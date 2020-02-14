from django.shortcuts import render
from django.views import generic
from .models import Blog

# Create your views here.
class BlogMain(generic.ListView):
	queryset = Blog.objects.filter(status=1)
	post_list = Blog.objects.raw('SELECT * FROM blog_blog')
	# all_category = ["Depression","ADHD","Children Behavior" ,"Autism", "Anxiety", 
	#                "Bipolar", "Eating Disorder", 'Anorexia','Parenting',"Others"]

	template_name = 'blog.html'


class BlogDetail(generic.DetailView):
    model = Blog
    template_name = 'Blog_detail.html'

