from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import MIDIFiles, MIDIInfo, Artist


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class MIDIFilesSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = MIDIFiles
        read_only_fields = ('created', 'owner', 'parsed')
        required_fields = 'datafile'

class MIDIInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MIDIInfo


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
