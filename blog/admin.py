from django.contrib import admin
from .models import Blog
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_filter = ("status",'category')
    search_fields = ['title', 'content','category']

admin.site.register(Blog, BlogAdmin)
