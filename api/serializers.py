from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import STUser, MusicBlock


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = STUser
        fields = ('url', 'username', 'email', 'groups', 'avatar', 'selfIntro', 'favoriteGenres', 'city', 'is_active')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class MusicBlockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MusicBlock
        fields = ('midiFile', 'createdAt', 'genre', 'tempo', 'blockConfigFile', 'engineConfigFile', 'collectedBy', 'composedBy')