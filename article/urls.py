# 引入path
from django.urls import path
from . import views

# 正在部署的应用的名称
app_name = 'article'

urlpatterns = [
    # path函数将url映射到视图
    path('article-list/', views.article_list, name='article_list'),
    # 文章详情
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    # 写文章
    path('article-create/', views.article_create, name='article_create'),
    # 删除文章
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
# 更新文章
    path('article-update/<int:id>/', views.article_update, name='article_update'),
    path('article-detail/<int:id>/upload/jsons/group_data.json/', views.file_download, name='file_download'),
    path('article-detail/<int:id>/file_cluster', views.file_cluster, name='file_cluster'),
    path('article-detail/<int:id>/article/groups_result.json', views.show_result, name='show_result'),
    path('article-detail/<int:id>/sum', views.count, name='count'),
    path('article-data/', views.data_acquisition, name='data_acquisition'),

]