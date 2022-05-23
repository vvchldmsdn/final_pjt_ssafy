from .models import Movie, Genre, Comment
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .serializers.movie_serializers import MovieSerializer, MovieCosSerializer, MovieGenreSerializer, MovieLanguageSerializer
from .serializers.genre_serializers import GenreSerializer
from .serializers.comment_serializers import CommentSerializer
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from pprint import pprint
from algorithms import cos_algorithms, wr_algorithms


# Create your views here.
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    movies = get_list_or_404(Movie)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def genre_recom(request, genre_pk):
    result = []
    weighted_ratings = wr_algorithms.weighted_ratings
    while len(result) <= 20:
        for id, ratings in weighted_ratings:
            tmp_movie = get_object_or_404(Movie, pk=id)
            tmp_serializer = MovieGenreSerializer(tmp_movie)
            if genre_pk in tmp_serializer.data['genre_ids']:
                result.append(tmp_serializer.data)
    return Response(result)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def default_recom(request):
    result = []
    top_twenty = wr_algorithms.weighted_ratings[:20]  # 상위 20개 영화
    for id, rating in top_twenty:
        tmp_movie = get_object_or_404(Movie, pk=id)
        tmp_serializer = MovieSerializer(tmp_movie)
        result.append(tmp_serializer.data)
    return Response(result)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def user_interest(request, language_pk):
    result = []
    weighted_ratings = wr_algorithms.weighted_ratings
    for id, rating in weighted_ratings:
        tmp_movie = get_object_or_404(Movie, pk=id)
        tmp_serializer = MovieLanguageSerializer(tmp_movie)
        if language_pk in tmp_serializer.data['language_ids']:
            result.append(tmp_serializer.data)
    return Response(result)


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def create_comment(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=user)
        comments = movie.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_update_or_delete(request, movie_pk, comment_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    def update_comment():
        if request.user == comment.user:
            serializer = CommentSerializer(instance=comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                comments = movie.comments.all()
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data)

    def delete_comment():
        if request.user == comment.user:
            comment.delete()
            comments = movie.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
    
    if request.method == 'PUT':
        return update_comment()
    elif request.method == 'DELETE':
        return delete_comment()
