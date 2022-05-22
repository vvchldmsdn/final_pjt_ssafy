from rest_framework import serializers
from ..models import Movie, Actor, Director


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


# ..algorithms.py에 json으로 데이터 주기 위한 serilaizer
class MovieCosSerializer(serializers.ModelSerializer):

    class ActorNameSerializer(serializers.ModelSerializer):

        class Meta:
            model = Actor
            fields = ('name',)
    

    class DirectorNameSerializer(serializers.ModelSerializer):

        class Meta:
            model = Director
            fields = ('name',)


    actor_ids = ActorNameSerializer(many=True, read_only=True)
    director_ids = DirectorNameSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'