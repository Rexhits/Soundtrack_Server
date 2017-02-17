"""SoundTrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from django.conf import settings
from api import views
from rest_framework.authtoken import views as defaultViews

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'musicblock', views.MusicBlockViewSet)
router.register(r'musicpiece', views.MusicPieceViewSet)
router.register(r'billboard', views.BillboardViewSet)
# router.register(r'midifiles', views.MIDIFilesView)
# router.register(r'midiinfo', views.MIDIInfoView)
# router.register(r'artist', views.ArtistView)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register/', views.create_auth),
    url(r'^api-token-auth/', defaultViews.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/', include('allauth.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
