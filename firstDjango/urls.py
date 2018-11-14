"""firstDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


from django.contrib import admin
from django.urls import path,include
from blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', views.blog_index),
    path('blog/input_front', views.blog_input),
    path('article/', include('article.urls', namespace='article')),
    # include将路径分发给下一步处理；
    # namespace可以保证反查到唯一的url，即使不同的app使用了相同的url（后面会用到）
]