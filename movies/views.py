from .models import Movie, Genre
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .serializers.movie_serializers import MovieSerializer, MovieCosSerializer
from .serializers.genre_serializers import GenreSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pprint import pprint
from algorithms import cos_algorithms, wr_algorithms


# Create your views here.
@api_view(['GET'])
def index(request):
    movies = get_list_or_404(Movie)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recom(request, movie_pk):
    result = []
    cos_similarities = cos_algorithms.cosine_sim_dict[movie_pk]  # 딕셔너리
    for id in cos_similarities:
        if cos_similarities[id] >= 0.12:
            tmp_movie = get_object_or_404(Movie, pk=id)
            tmp_serializer = MovieSerializer(tmp_movie)
            tmp_serializer_dict = dict(tmp_serializer.data)
            tmp_serializer_dict['cos_sim'] = cos_similarities[id]
            result.append(tmp_serializer_dict)
    return Response(result)


@api_view(['GET'])
def genre_recom(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    serializer = GenreSerializer(genre)  # 장르 id, name, 연결 된 movie의 (id, poster, overview, ti)
    return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['GET'])
def default_recom(request):
    result = []
    top_twenty = wr_algorithms.weighted_ratings[:20]  # 상위 20개 영화
    for id, rating in top_twenty:
        tmp_movie = get_object_or_404(Movie, pk=id)
        tmp_serializer = MovieSerializer(tmp_movie)
        result.append(tmp_serializer.data)
    return Response(result)


@api_view(['GET'])
def user_interest(request, language_pk):
    result = []
    weighted_ratings = wr_algorithms.weighted_ratings
    for id, rating in weighted_ratings:
        tmp_movie = get_object_or_404(Movie, pk=id)
        tmp_serializer = MovieSerializer(tmp_movie)
        if language_pk in tmp_serializer['language_ids']:
            result.append(tmp_serializer.data)
    return Response(result)