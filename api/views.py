from django.contrib.auth.models import User, Group
from rest_framework import permissions, viewsets, parsers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer, MusicBlockSerializer
from django.http import JsonResponse
from .models import STUser, MusicBlock
from SoundTrack.settings import MEDIA_ROOT
from . import musicInfo
import simplejson as json
# Create your views here.

@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def create_auth(request):
    userName = request.data['username']
    userPassword = request.data['password']
    userEmail = request.data['email']
    u, created = STUser.objects.get_or_create(
        username=userName,
        email=userEmail,
    )
    newUser = u
    newUser.set_password(userPassword)
    newUser.save()
    userInfo = {
        'email': str(userEmail),
        'token': str(newUser.auth_token),
    }
    if created:
        return Response(userInfo, status=status.HTTP_201_CREATED)
    else:
        return Response(json.dumps({'error': "user existed"}), status=status.HTTP_400_BAD_REQUEST)




class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = STUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# class MIDIFilesView(viewsets.ModelViewSet):
#     queryset = MIDIFiles.objects.all()
#     serializer_class = MIDIFilesSerializer
#     parser_classes = (parsers.FormParser, parsers.MultiPartParser,)
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser)
#
#     def perform_create(self, serializer):
#         if serializer.is_valid():
#             file = self.request.data.get('datafile')
#
#             # unsloved problem with saving data in one to one field
#             serializer.save(owner=self.request.user,
#                             datafile=file,
#                             )
#             _tempo, _timesignature, _duration, _key = musicInfo.getMusicInfo(MEDIA_ROOT + "/" + file.name)
#             _tracks = musicInfo.getTracks(MEDIA_ROOT + "/" + file.name)
#             info = MIDIInfo(
#                 filename=file.name,
#                 tempo=_tempo,
#                 timeSignature=_timesignature,
#                 duration=_duration,
#                 key=_key,
#                 tracks=_tracks,
#             )
#             info.save()
#             serializer.save(fileInfo=info)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'key': 'value'}, status=status.HTTP_200_OK)
#
# class MIDIInfoView(viewsets.ModelViewSet):
#     queryset = MIDIInfo.objects.all()
#     serializer_class = MIDIInfoSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser)

# class ArtistView(viewsets.ModelViewSet):
#     queryset = Artist.objects.all()
#     serializer_class = ArtistSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser)

