from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import STUser, MusicBlock, Billboard, MusicPiece, fxStatus, instStatus
from rest_framework.validators import UniqueValidator

class fxStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = fxStatus
        fields = ('file',)

class instStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = instStatus
        fields = ('file',)

class MusicBlockSerializer(serializers.HyperlinkedModelSerializer):
    fxStatus = fxStatusSerializer(many=True, read_only=True)
    instStatus = instStatusSerializer(many=True, read_only=True)

    class Meta:
        model = MusicBlock
        fields = ('url', 'title', 'midiFile', 'jsonFile', 'fxStatus', 'instStatus', 'onboard', 'collectedBy',
                  'composedBy', 'createdAt')

class MusicPieceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MusicPiece
        fields = ('url', 'musicBlock', 'audioFile')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=STUser.objects.all())])
    composedBlocks = MusicBlockSerializer(many=True, read_only=True)
    collectedBlocks = MusicBlockSerializer(many=True, read_only=True)
    composedMusic = MusicPieceSerializer(many=True, read_only=True)
    collectedMusic = MusicBlockSerializer(many=True, read_only=True)
    class Meta:
        model = STUser
        fields = ('url', 'id', 'username', 'displayName', 'email', 'groups', 'avatar', 'selfIntro', 'favoriteGenres',
                  'country', 'city', 'is_active', 'collectedBlocks', 'composedBlocks', 'composedMusic', 'collectedMusic')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')



class BillboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Billboard
        fields = ('url','latitude','longitude','location','name','address1','address2', 'info', 'setupAt')

