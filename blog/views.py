from django.shortcuts import render
from blog.models import BlogsPost
from blog.models import JsonPost

# Create your views here.


def blog_index(request):
    blog_list = BlogsPost.objects.all()  # 获取所有数据
    return render(request, 'blog/index.html', {'blog_list': blog_list})
# 返回index.html页面


def blog_input(request):
    json_list = JsonPost.objects.all()
    return render(request, 'blog/input_front.html', {'json_list': json_list})