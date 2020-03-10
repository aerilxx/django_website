from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.text import slugify
from django.db.models import F
from django.contrib import messages 
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from django.core.paginator import Paginator
from .forms import PostForm, PostFormCategory, CommentForm
from .models import Category, Forum, Post, Comment
from user.models import Profile


# forum index, no need to log in to view all topics post
class index(generic.ListView):
    queryset = Category.objects.order_by('id')
    post_list = Category.objects.raw('SELECT * FROM forum_category')
    template_name = 'forum/index_all_categories.html'



# get posts under each topics, just to view, cannot post
def category(request,category_id):
    cat_obj = Category.objects.get(id=category_id)
    forums = Forum.objects.filter(category_id = category_id).order_by('created_on')
    posts = Post.objects.filter(category_id = category_id).order_by('created_on')
    paginator = Paginator(posts, 15)
    
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        posts_display = paginator.page(page)
    except:
        posts_display = paginator.page(paginator.num_pages)

    if len(posts)>=0:
        context_dict = {'category':cat_obj,
                        'forums':forums,
                        'posts': posts_display}
        return render(request, 'forum/each_category.html', context_dict)
    else:
        return render(request,'forum/topic_not_found.html')


# get posts under each sub topics, new post added to topic automatically display
def forum(request, forum_slug):
    
    forum_obj = Forum.objects.get(slug=forum_slug)
    posts = Post.objects.filter(forum_id = forum_obj.id).order_by('created_on')
    paginator = Paginator(posts, 20)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        posts_display = paginator.page(page)
    except:
        posts_display = paginator.page(paginator.num_pages)
    context_dict = {'forum':forum_obj,
                   'posts': posts_display}
    return render(request, 'forum/each_forum.html', context_dict)
   

# view single post, if log in, can reply
def post(request, post_id):
    post = Post.objects.get(id = int(post_id))
    comments = Comment.objects.filter(post_id=int(post_id))

    # increment num_views when load post
    Post.objects.filter(id = int(post_id)).update(num_views=F('num_views') + 1)
    post.num_views+=1

    # if user log in, they can reply
    user = request.user
    if not user.is_authenticated:
        ctx={'post':post, 'comments':comments }
        return render(request, 'forum/single_post.html', ctx)

    profile = Profile.objects.get(user=user)
    if not user:
        return redirect('/')

    if request.method == "POST":
        commentForm = CommentForm(request.POST)
        
        if commentForm.is_valid():
            instance = commentForm.save(commit=False)
            instance.posted_by = profile
            instance.post = post
            instance.poster_ip = get_client_ip(request)
            instance.message = commentForm.cleaned_data['message']
            instance.created_on = datetime.now()
            instance.save()

            return redirect('post', post_id= post_id)

        else:
            messages.add_message(request, messages.ERROR, commentForm.errors )
            
    else:
        commentForm = CommentForm()

    ctx={'post':post, 'comments':comments, 'comment_form':commentForm }
    return render(request, 'forum/single_post.html', ctx)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# post under sub cateogry
@login_required
def new_post(request,forum_slug):
    user = request.user
    profile = Profile.objects.get(user=user)
    forum = forum_obj = category =""
    print('new post called')
    
    if not user:
        return redirect('/')

    if forum_slug:
        forum_obj = Forum.objects.get(slug = forum_slug)

        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.forum = forum_obj
                instance.category = forum_obj.category
                instance.subject = form.cleaned_data['subject']
                instance.context = form.cleaned_data['context']
                instance.posted_by = profile
                instance.poster_ip =  get_client_ip(request)
                instance.created_on = datetime.now()
                instance.slug = slugify(form.cleaned_data['subject'])
                instance.save()
                return redirect('forum', forum_slug= forum_slug)

            else:
                messages.add_message(request, messages.ERROR, form.errors )
        else:
            form = PostForm()
    return render(request, 'forum/new_post.html', {'form': form})


# post under main category, no assigned sub category, create forum when post
@login_required
def new_post_category(request,category_id):
    user = request.user
    profile = Profile.objects.get(user=user)
    forum  = category =""

    if not user:
        return redirect('/')
 
    if category_id:
        category = Category.objects.get(id = category_id)

        if request.method == "POST":
            form = PostFormCategory(request.POST)
            
            if form.is_valid():
                instance = form.save(commit=False)
                forum_name = request.POST.get('forum')
                forum = Forum(name=forum_name, category = category)
                forum.save()
                instance.forum = forum
                instance.category = category
                instance.subject = form.cleaned_data['subject']
                instance.context = form.cleaned_data['context']
                instance.posted_by = profile
                instance.poster_ip =  get_client_ip(request)
                instance.created_on = datetime.now()
                instance.slug = slugify(form.cleaned_data['subject'])
                instance.save()

                return redirect('category', category_id= category_id)
            else:
                messages.add_message(request, messages.ERROR, form.errors )
        else:
            form = PostFormCategory()
      
    return render(request, 'forum/publish_post.html', {'form': form})


@login_required
def manage_post_by_user(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(posted_by=profile)
    return render(request, 'forum/manage_post_by_user.html',{'posts': posts})


@login_required
def edit_post(request, post_id):
    edit_post = get_object_or_404(Post, id=post_id)
    if not (request.user.is_active or request.user == edit_post.posted_by):
        return HttpResponse(ugettext('no right'))

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.update_post(edit_post)
            return redirect('manage_posts')
        else:
            messages.add_message(request, messages.ERROR, form.errors )
    else:
        form = PostForm()
    return render(request, 'forum/edit_post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    if not (request.user.is_active or request.user == edit_post.posted_by):
        return HttpResponse(ugettext('no right'))

    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('manage_posts')


@login_required
def close_post(request, post_id):
    if not (request.user.is_active or request.user == edit_post.posted_by):
        return HttpResponse(ugettext('no right'))

    Post.objects.filter(id=post_id).update(closed=True)
    return redirect('manage_posts')









