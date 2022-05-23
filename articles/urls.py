from django.urls import path
from . import views

urlpatterns = [
    # ArticleList.vue에서 요청 보냄 / 보낼 데이터 : 모든 게시글의 id, title
    path('', views.index),

    # CreateArticle.vue에서 POST 요청 보냄 /
    path('create/', views.article_list),

    # ArticleDetail.vue에서 요청 보냄 / 보낼 데이터 : id, title, content, created_at, updated_at
    # path('update/', views.update),
]
