# from __future__ import unicode_literals

# from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.text import slugify
from django.db.models import F
# from django.core.exceptions import FieldError
# from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import ugettext
# from django.core.urlresolvers import reverse
# from django.views.decorators.csrf import csrf_exempt
# from django.db.models import Q
# # from django.contrib import messages
from django.core.paginator import Paginator
from .forms import PostForm
from .models import Category, Forum, Post, Comment
from user.models import Profile


# forum index, no need to log in to view all topics post
class index(generic.ListView):
    queryset = Category.objects.order_by('id')
    post_list = Category.objects.raw('SELECT * FROM forum_category')
    template_name = 'forum/index_all_categories.html'



# get posts under each topics, just to view, cannot post
def get_category(request,category_id):
    cat_obj = Category.objects.get(id=category_id)
    forums = Forum.objects.filter(category_id = cat_obj.id).order_by('created_on')
    posts = Post.objects.filter(category_id = cat_obj.id).order_by('created_on')
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
   

# view single post
def post(request, post_id):
    post = Post.objects.get(id = int(post_id))
    comments = Comment.objects.filter(post_id=int(post_id))
    # increment num_views when load post
    Post.objects.filter(id = int(post_id)).update(num_views=F('num_views') + 1)
    post.num_views+=1
    ctx={'post':post, 'comments':comments }
    return render(request, 'forum/single_post.html', ctx)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def new_post(request,forum_slug=None, category_id=None):
    user = request.user
    profile = Profile.objects.get(user=user)
    forum = forum_obj = category =""
    
    if not user:
        print('use not authorized')
        return redirect('signup')

# post under sub cateogry
    if forum_slug:
        forum_obj = Forum.objects.get(slug = forum_slug)

        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                print('valid')
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
                print('form is invalid')
        else:
            print('not valid')
            form = PostForm()

# post under main category, no assigned sub category, create forum when post 
    if category_id:
        category_obj = Category.objects.get(id = category_id)

        if request.method == "POST":
            form = PostFormCategory(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                forum_name = form.cleaned_data['forum']
                forum_obj = Forum.objects.create(category_id = category_id,
                             name = forum_name, created_on = datetime.now())
                
                print('valid')
                post = Post.objects.create(forum = forum_obj, subject = form.cleaned_data['subject'],
                             context = form.cleaned_data['context'], category = category_id, 
                             posted_by=profile, poster_ip = get_client_ip(request), created_on = datetime.now())
                instance.save()

            else:
                print('form is invalid')
        else:
            print('not valid')
            form = PostFormCategory()
      
    return render(request, 'forum/new_post.html', {'form': form})



# @login_required
# def new_post(request):
#     categories =  ( "Mood Disorder",
#             "Behavior Disorder",
#             "Autism Spectrum Disorder",
#             "Eating Disorder",
#             'Parenting',
#             'Other Children Behavior',
#         )
#     user = request.user
#     if not user:
#         return redirect('signup')

#     if request.method == "POST":
#         print('post')
#         form = PostForm()
#         if form.is_valid() and request.POST.get('submit'):
            
#             post = form.save(commit=False)
#             post.posted_by = request.user
#             post.created_on = timezone.now()
#             post.poster_ip = get_client_ip(request)

#             print(post.poster_ip)
          
#             return render(request,'successful_post.html')
#     else:
#         print('post not saved')
#         form = PostForm()

#     return render(request,'forum/publish_post.html', {'categories':categories})


# def topic(request, topic_id, template_name="lbforum/topic.html"):
#     user = request.user
#     topic = get_object_or_404(Topic, pk=topic_id)
#     if topic.hidden and not topic.forum.is_admin(user):
#         return HttpResponse(ugettext('no right'))
#     topic.num_views += 1
#     topic.save()
#     posts = get_all_posts(user)
#     posts = posts.filter(topic=topic)
#     posts = posts.filter(topic_post=False)
#     posts = posts.order_by('created_on')
#     ext_ctx = {
#         'request': request,
#         'topic': topic,
#         'posts': posts,
#         'has_replied': topic.has_replied(request.user),
#         'can_admin': topic.forum.is_admin(user)
#     }
#     return render(request, template_name, ext_ctx)


# def post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     return HttpResponseRedirect(post.get_absolute_url_ext())


# @csrf_exempt
# def markitup_preview(request, template_name="lbforum/markitup_preview.html"):
#     return render(request, template_name, {'message': request.POST['data']})


# @login_required
# def new_post(
#         request, forum_id=None, topic_id=None, form_class=NewPostForm,
#         template_name='lbforum/post.html'):
#     user = request.user
#     if not user.lbforum_profile.nickname:
#         return redirect('lbforum_change_profile')
#     qpost = topic = forum = first_post = preview = None
#     post_type = _('topic')
#     topic_post = True
#     initial = {}
#     if forum_id:
#         forum = get_object_or_404(Forum, pk=forum_id)
#     if topic_id:
#         post_type = _('reply')
#         topic_post = False
#         topic = get_object_or_404(Topic, pk=topic_id)
#         if not topic_can_post(topic, user):
#             return HttpResponse(_("you can't reply, this topic closed."))
#         forum = topic.forum
#         first_post = topic.posts.order_by('created_on').first()
#     initial['forum'] = forum
#     if request.method == "POST":
#         form = form_class(
#             request.POST, user=user, forum=forum,
#             initial=initial,
#             topic=topic, ip=get_client_ip(request))
#         preview = request.POST.get('preview', '')
#         if form.is_valid() and request.POST.get('submit', ''):
#             post = form.save()
#             forum = post.topic.forum
#             if topic:
#                 return HttpResponseRedirect(post.get_absolute_url_ext())
#             else:
#                 return HttpResponseRedirect(reverse("lbforum_forum",
#                                                     args=[forum.slug]))
#     else:
#         qid = request.GET.get('qid', '')
#         if qid:
#             qpost = get_object_or_404(Post, id=qid)
#             initial['message'] = "[quote=%s]%s[/quote]" % (
#                 qpost.posted_by.lbforum_profile, qpost.message)
#         form = form_class(initial=initial, forum=forum)
#     ext_ctx = {
#         'forum': forum,
#         'show_forum_field': topic_post,
#         'form': form,
#         'topic': topic,
#         'first_post': first_post,
#         'post_type': post_type,
#         'preview': preview
#     }
#     ext_ctx['attachments'] = user.lbattachment_set.filter(
#         pk__in=request.POST.getlist('attachments'))
#     ext_ctx['is_new_post'] = True
#     ext_ctx['topic_post'] = topic_post
#     return render(request, template_name, ext_ctx)


# @login_required
# def edit_post(request, post_id, form_class=EditPostForm,
#               template_name="lbforum/post.html"):
#     preview = None
#     post_type = _('reply')
#     edit_post = get_object_or_404(Post, id=post_id)
#     if not (request.user.is_staff or request.user == edit_post.posted_by):
#         return HttpResponse(ugettext('no right'))
#     if edit_post.topic_post:
#         post_type = _('topic')
#     if request.method == "POST":
#         form = form_class(instance=edit_post, user=request.user,
#                           data=request.POST)
#         preview = request.POST.get('preview', '')
#         if form.is_valid() and request.POST.get('submit', ''):
#             edit_post = form.save()
#             return HttpResponseRedirect('../')
#     else:
#         form = form_class(instance=edit_post)
#     ext_ctx = {
#         'form': form,
#         'post': edit_post,
#         'topic': edit_post.topic,
#         'forum': edit_post.topic.forum,
#         'post_type': post_type,
#         'preview': preview,
#         'attachments': edit_post.attachments.all()
#     }
#     # ext_ctx['unpublished_attachments'] = request.user.lbattachment_set.filter(activated=False)
#     ext_ctx['topic_post'] = edit_post.topic_post
#     return render(request, template_name, ext_ctx)


# @login_required
# def delete_topic(request, topic_id):
#     if not request.user.is_staff:
#         # messages.error(_('no right'))
#         return HttpResponse(ugettext('no right'))
#     topic = get_object_or_404(Topic, id=topic_id)
#     forum = topic.forum
#     topic.delete()
#     forum.update_state_info()
#     return HttpResponseRedirect(reverse("lbforum_forum", args=[forum.slug]))


# @login_required
# def delete_post(request, post_id):
#     if not request.user.is_staff:
#         return HttpResponse(ugettext('no right'))
#     post = get_object_or_404(Post, id=post_id)
#     topic = post.topic
#     post.delete()
#     topic.update_state_info()
#     topic.forum.update_state_info()
#     # return HttpResponseRedirect(request.path)
#     return HttpResponseRedirect(reverse("lbforum_topic", args=[topic.id]))


# @login_required
# def toggle_topic_attr(request, topic_id, attr):
#     topic = get_object_or_404(Topic, id=topic_id)
#     forum = topic.forum
#     if not forum.is_admin(request.user):
#         return HttpResponse(ugettext('no right'))
#     if attr == 'sticky':
#         topic.sticky = not topic.sticky
#     elif attr == 'close':
#         topic.closed = not topic.closed
#     elif attr == 'hide':
#         topic.hidden = not topic.hidden
#     elif attr == 'distillate':
#         topic.level = 30 if topic.level >= 60 else 60
#     topic.save()
#     return HttpResponseRedirect(reverse("lbforum_topic", args=[topic.id]))
