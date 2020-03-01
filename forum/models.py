from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from user.models import Profile
from datetime import datetime


CATEGORIES = (
            ("Mood Disorder", "Mood Disorder"),
            ("Behavior Disorder", "Behavior Disorder"),
            ("Autism Spectrum Disorder", "Autism Spectrum Disorder"),
            ("Eating Disorder", "Eating Disorder"),
            ('Parenting','Parenting'),
            ('Other Children Behavior','Other Children Behavior'),
        )
class Category(models.Model):
    name = models.CharField(max_length=100, choices = CATEGORIES)
    descn = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

# sub category of disorder, such as depression in mood disorder blabla
class Forum(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(default='')
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    # 帖子
    num_posts = models.IntegerField(default=0)
    num_replies = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_on', 'updated_on')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Forum, self).save(*args, **kwargs)

    # def create(self):


# 发帖数
    def count_nums_post(self):
        return self.post_set.all().count()
# 回帖数
    def count_nums_replies(self):
        return Comment.objects.filter(post__forum=self).count()

# 有人回帖或者发帖自动更新
    def update_state_info(self, last_post=None, commit=True):
        self.num_posts = self.count_nums_post()
        self.num_replies = self.count_nums_replies()
        if not last_post:
            last_post = Comment.objects.filter(
                post__forum=self).order_by('-created_on').first()
        self.last_post = last_post
        if commit:
            self.save()

# 每个话题下的帖子
class Post(models.Model):
	# 话题被删除后帖子还在
    forum = models.ForeignKey(Forum, on_delete = models.SET_DEFAULT, default = None)
    category = models.ForeignKey(Category, on_delete = models.SET_DEFAULT, default = None)
    posted_by = models.ForeignKey(Profile, on_delete = models.CASCADE)
    poster_ip = models.GenericIPAddressField()

    # 帖子的名称
    subject = models.CharField(max_length=999)
    slug = models.SlugField(blank=True, unique=True)
    # 帖子的内容
    context = models.TextField(default='')

    num_views = models.IntegerField(default=0)
    num_replies = models.PositiveSmallIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    last_reply_on = models.DateTimeField(auto_now_add=True)

    closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('-last_reply_on',) 
        get_latest_by = ('created_on')

    def __str__(self):
        return self.subject

    def count_nums_replies(self):
        return Comment.objects.filter(post=self).count()

    def get_absolute_url(self):
        return ('forum_post', (), {'post_slug': self.slug})

# 是否有人回复
    def has_replied(self, user):
        if user.is_anonymous():
            return False
        return Comment.objects.filter(posted_by=user, post=self).count()

    def update_state_info(self, last_post=None, commit=True):
        self.num_replies = self.count_nums_replies()
        if not last_post:
            last_post = self.comments.order_by('-created_on').first()
        self.last_post = last_post
        if commit:
            self.save()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    posted_by = models.ForeignKey(Profile, on_delete = models.CASCADE)
    poster_ip = models.GenericIPAddressField()
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return self.message[:250]

    def subject(self):
        if self.post_comment:
            return _('Topic: %s') % self.post.subject
        return _('Re: %s') % self.post.subject


# 有人回帖或者发帖自动更新

def update_last_comment(sender, instance, created, **kwargs):
    comment = instance
    if created:
        post = instance.post
        forum = post.forum
        post.update_state_info(last_post=post)
        forum.update_state_info(last_post=post)

def update_last_post(sender, instance, created, **kwargs):
    post = instance
    if created:
        forum = post.forum
        forum.update_state_info(last_post=post)

post_save.connect(update_last_comment, sender=Comment)
post_save.connect(update_last_post, sender=Post)

