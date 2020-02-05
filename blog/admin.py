from django.contrib import admin
from .models import Blog,Category
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_filter = ("status",)
    search_fields = ['title', 'content']

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
