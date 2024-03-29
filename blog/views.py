from django.shortcuts import render
from django.views import generic
from .models import Blog

# Create your views here.
class BlogMain(generic.ListView):
	queryset = Blog.objects.filter(status=1)
	post_list = Blog.objects.raw('SELECT * FROM blog_blog')
	paginate_by = 8
	# all_category = ["Depression","ADHD","Children Behavior" ,"Autism", "Anxiety", 
	#                "Bipolar", "Eating Disorder", 'Anorexia','Parenting',"Others"]

	template_name = 'blog/blog.html'


class BlogDetail(generic.DetailView):
    model = Blog
    template_name = 'blog/Blog_detail.html'

