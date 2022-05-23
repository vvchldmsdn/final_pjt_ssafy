from django.urls import path
from . import views

urlpatterns = [
    # HomeView.vue에서 요청 보냄 -> 보낼 데이터 = weighted rating 상위 15개 영화들의 poster_path, id, title
    path('', views.index),

    # RelatedRecommend.vue에서 요청 보냄 -> 보낼 데이터 = 코사인 유사도 0.12이상인 영화들의 poster_path, id, title
    path('<int:movie_pk>/recom/', views.recom),
    
    # GenreRecommend.vue에서 요청 보냄 -> 보낼 데이터 = 해당 장르에 대응되는 영화들 weighted rating 상위 15개 영화들의 poster_path, id, title
    path('genre/<int:genre_pk>/', views.genre_recom),

    # MovieInfo.vue에서 요청 보냄 -> 보낼 데이터 = 해당 영화의 poster_path, id, title, overview, actor_ids, director_ids
    path('<int:movie_pk>/', views.movie_detail),

    # DefaultRecom.vue에서 요청 보냄 -> 보낼 데이터 전체 영화중 weighted rating 상위 20개 영화들의 poster_path, id, title
    path('default/', views.default_recom),

    # UserInterest.vue에서 POST 요청 보냄 
    # 받는 데이터 : spoken_language의 id값
    # 보낼 데이터 : 해당 spoken_language에 대응되는 영화들 weighted rating 해서 상위 20개 영화들의 poster_path, id, title
    path('interest/<int:language_pk>/', views.user_interests),
]
