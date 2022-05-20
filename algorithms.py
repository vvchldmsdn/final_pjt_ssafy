import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finalpjt.settings")

import django
django.setup()

from movies.models import Movie
from movies.serializers import MovieCosSerializer

from numpy import dot 
from numpy.linalg import norm 
import numpy as np 
from pprint import pprint
from itertools import combinations


movies = Movie.objects.all()
movie_serializer = MovieCosSerializer(movies, many=True)  # 이걸 입력변수로 받아서 미리 계산 끝낼꺼임
# pprint(type(movie_serializer.data))
# pprint(type(movie_serializer.data[0]['overview']))
movie_data = movie_serializer.data  # 리스트 형태

'''
계산 끝내놓고 어디다가 어떻게 쓸지 정해야함
아니 근데 이게 DB에 40개 있으면 40C2가지 결과를 저장하고 있어야 되는데
흠... A라는 영화 정보가 들어오면 A와의 코사인 유사도 결과를 들고 와야함
'''
# 조사 목록
pposi = {
    '은': 1, '께서': 1, '을': 1, '를': 1,
    '는': 1, '에': 1, '에게': 1, '께': 1,
    '이': 1, '한테': 1, '더러': 1, '으로': 1,
    '가': 1, '의': 1, '와': 1, '과': 1, '다': 1,
    '에서': 1, '하는': 1, '린': 1, '고': 1, '야': 1,
    '한다': 1
}


def sep(s):
    s_arr = s.split(' ')
    for i in range(len(s_arr)):
        for pos in pposi:
            if s_arr[i].endswith(pos):
                s_arr[i] = s_arr[i][:-len(pos)]
                break
    return s_arr


# 코사인 유사도를 구하는 함수 
def cos_sim(a, b): 
    return dot(a, b)/(norm(a)*norm(b)) 


# 기준이 되는 키워드와 벡터 키워드 리스트를 받아서 키워드별 빈도를 구하는 함수 
def make_matrix(feats, list_data): 
    freq_list = [] 
    for feat in feats: 
        freq = 0 
        for word in list_data: 
            if feat == word: 
                freq += 1 
        freq_list.append(freq) 
    return freq_list 


## 계산해야함

# 1. feats 만들기
sep_overviews = []
for info in movie_serializer.data:
    sep_overviews.append((info['id'], sep(info['overview'])))

feats = []
for id, overview in sep_overviews:
    feats += overview
feats = set(feats)


# 2. numpy array 만들기
np_arrs = []
for id, overview in sep_overviews:
    np_arrs.append((id, np.array(make_matrix(feats, overview))))


# 3. cosine similarity 계산하기
cosine_sim_dict = dict()  # 최종 저장된 딕셔너리
for info in movie_serializer.data:
    cosine_sim_dict[info['id']] = dict()


choices = list(combinations(np_arrs, 2))
for choice in choices:
    similarity = cos_sim(choice[0][1], choice[1][1])
    cosine_sim_dict[choice[0][0]][choice[1][0]] = similarity
    cosine_sim_dict[choice[1][0]][choice[0][0]] = similarity

# pprint(cosine_sim_dict)