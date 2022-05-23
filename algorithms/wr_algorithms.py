import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finalpjt.settings")

import django
django.setup()

from movies.models import Movie, Genre

from movies.serializers.genre_serializers import GenreSerializer
from movies.serializers.movie_serializers import MovieSerializer

from pprint import pprint


## 1. 우선 weighted rating 계산하는 함수 짜야 함
'''
투표 수 상위 20프로 이상 만
(v / (v + m)) * R + (m / (v + m)) * C
v = 개별 영화 투표 수
m = minimum votes required to be listed (상위 20퍼의 영화의 vote_count 가져오기)
    최소 투표수
R = 개별 영화 평점
C = 전체 영화에 대한 평균 평점
'''

# 1.1. 전체 영화에 대해서
movies = Movie.objects.all()
movies_serializer = MovieSerializer(movies, many=True)
movies_data = movies_serializer.data  # 리스트

num_movies = len(movies_data)  # 전체 영화 개수
total_sum_rating = 0  # 모든 영화 평점 합칠 변수
vote_count_arr = []  # 모든 영화의 vote count가 담길 리스트  (id, vote_count)

for info in movies_data:
    vote_average = info['vote_average']
    vote_count = info['vote_count']
    movie_id = info['id']

    total_sum_rating += vote_average
    vote_count_arr.append((movie_id, vote_count))

vote_count_arr.sort(key=lambda x: x[1], reverse=True)
m = vote_count_arr[(num_movies * 2) // 10][1]

c = total_sum_rating / num_movies
c = round(c, 2)  # 나중에 장르 별 계산 할 때도 계속 쓸꺼임

# vote_count_arr에서 (num_movies * 2) // 10인덱스 밑 부분만 볼꺼임
weighted_ratings = []
target_movies = vote_count_arr[:(num_movies * 2) // 10 + 1]

for info in movies_data:
    movie_id = info['id']
    vote_count = info['vote_count']
    if (movie_id, vote_count) in target_movies:
        weighted_rating = (vote_count / (vote_count + m)) * info['vote_average'] + (m / (vote_count + m)) * c
        weighted_ratings.append((movie_id, weighted_rating))

weighted_ratings.sort(key=lambda x: x[1], reverse=True)  # weighted rating이 큰 순서대로 id값과 weighted rating값 저장
# pprint(weighted_ratings)