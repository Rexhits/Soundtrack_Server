from django.contrib.auth.models import Group
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.auth.models import User
from django.core import serializers
from rest_framework import filters
from rest_framework import permissions, viewsets, parsers, status
from rest_framework.decorators import api_view, permission_classes, list_route
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer, MusicBlockSerializer, BillboardSerializer, MusicPieceSerializer
from django.http import JsonResponse
from .models import STUser, MusicBlock, Billboard, MusicPiece, fxStatus, instStatus
from . import musicInfo
import simplejson as json
# Create your views here.

@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def create_auth(request):
    userName = STUser.GenerateUsername()
    displayName = request.data['username']
    userPassword = request.data['password']
    userEmail = request.data['email']
    u, created = STUser.objects.get_or_create(
        username=userName,
        email=userEmail,
        displayName = displayName
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
    permission_classes = (permissions.IsAuthenticated,)
    @list_route(methods=['get'], permission_classes=(permissions.IsAuthenticated,))
    def current(self, request):
        serialized = self.get_serializer(instance=request.user, many=False)
        return Response(serialized.data)

    @list_route(methods=['post'], permission_classes=(permissions.IsAuthenticated,))
    def avatar(self, request):
        user = self.request.user
        avatar = request.data.get('avatar')
        user.avatar = avatar
        user.save()
        serialized = self.get_serializer(instance=user, many=False)
        return Response(serialized.data)



class MusicBlockViewSet(viewsets.ModelViewSet):
    queryset = MusicBlock.objects.all()
    serializer_class = MusicBlockSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    ordering = ('-createdAt')

    def perform_create(self, serializer):
        block = serializer.save(composedBy=self.request.user)
        fxfiles = self.request.FILES.getlist('fxStatus')
        instfiles = self.request.FILES.getlist('instStatus')
        for i in fxfiles:
            fxStatusData = fxStatus(file=i, block=block)
            fxStatusData.save()
        for i in instfiles:
            instStatusData = instStatus(file=i, block=block)
            instStatusData.save()

    def partial_update(self, request, *args, **kwargs):
        block = self.get_object()
        if request.data.get('title'):
            block.title = request.data.get('title')
        if request.data.get('midiFile'):
            block.midiFile = request.data.get('midiFile')
        if request.data.get('jsonFile'):
            block.jsonFile = request.data.get('jsonFile')
        if request.data.get('onboard'):
            block.onboard = request.data.get('onboard')

        fxfiles = self.request.FILES.getlist('fxStatus')
        if len(fxfiles) > 0:
            fxStatus.objects.filter(block=block).delete()
            for i in fxfiles:
                fxStatusData = fxStatus(file=i, block=block)
                fxStatusData.save()

        instfiles = self.request.FILES.getlist('instStatus')
        if len(instfiles) > 0:
            instStatus.objects.filter(block=block).delete()
            for i in instfiles:
                instStatusData = instStatus(file=i, block=block)
                instStatusData.save()
        block.save()
        serialized = self.get_serializer(instance=block)
        return Response(serialized.data)

class MusicPieceViewSet(viewsets.ModelViewSet):
    queryset = MusicPiece.objects.all()
    serializer_class = MusicPieceSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)
    permission_classes = (permissions.IsAuthenticated,)

class BillboardViewSet(viewsets.ModelViewSet):
    queryset = Billboard.objects.all()
    serializer_class = BillboardSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)
    permission_classes = (permissions.IsAuthenticated,)
    @list_route(methods=['post'], permission_classes = (permissions.IsAuthenticated,))
    def lookup(self, request):
        lat = float(request.data['latitude'])
        lon = float(request.data['longitude'])
        radius = float(request.data['distance'])
        point = Point(lat, lon)
        print(point)
        result = Billboard.objects.filter(location__distance_lte=(point, D(mi=radius))).distance(point).order_by('distance')
        serialized = self.get_serializer(instance=result, many=True)
        print(serialized.data)
        return Response(serialized.data)

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

