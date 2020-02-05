from django.db import models

# Create your models here.
from django.contrib.auth.models import User


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.CharField(max_length=100, unique=False)
    body = models.TextField()
    posted = models.DateField(db_index=True, auto_now_add=True)
    category = models.ForeignKey('blog.Category',on_delete=models.SET_DEFAULT, default="no category")
    status = models.IntegerField(choices=STATUS, default=0)

    def __unicode__(self):
        return '%s' % self.title

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __unicode__(self):
        return '%s' % self.title
