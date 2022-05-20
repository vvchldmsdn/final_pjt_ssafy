from .models import Movie
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .serializers import MovieSerializer, MovieCosSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pprint import pprint
import algorithms

from movies import serializers
# Create your views here.
@api_view(['GET'])
def index(request):
    movies = get_list_or_404(Movie)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recom(request, movie_pk):
    result = []
    cos_similarities = algorithms.cosine_sim_dict[movie_pk]  # 딕셔너리
    for id in cos_similarities:
        if cos_similarities[id] >= 0.1:
            tmp_movie = get_object_or_404(Movie, pk=id)
            tmp_serializer = MovieSerializer(tmp_movie)
            tmp_serializer_dict = dict(tmp_serializer.data)
            tmp_serializer_dict['cos_sim'] = cos_similarities[id]
            result.append(tmp_serializer_dict)
    return Response(result)