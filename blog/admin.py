from django.contrib import admin
from blog.models import BlogsPost
from blog.models import JsonPost
# Register your models here.


class BlogsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'timestamp']


class JsonPostAdmin(admin.ModelAdmin):
    list_display = ['classid', 'jsonfile']


admin.site.register(BlogsPost, BlogsPostAdmin)
admin.site.register(JsonPost, JsonPostAdmin)

