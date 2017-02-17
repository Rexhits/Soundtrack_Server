from django.contrib.gis.db import models
import random
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.geos import Point
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from multiupload.fields import MultiFileField
# Create your models here.


class STUser(AbstractUser):
    email = models.EmailField(unique=True)
    displayName = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(upload_to='avator',null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    selfIntro = models.CharField(max_length=200, null=True, blank=True)
    favoriteGenres = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    def GenerateUsername():
        i = 0
        MAX = 1000000
        while (i < MAX):
            username = str(random.randint(0, MAX))
            try:
                STUser.objects.get(username=username)
            except STUser.DoesNotExist:
                return username
            i += 1
        raise Exception('All random username are taken')

@receiver(post_save, sender=STUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class MusicBlock(models.Model):
    title = models.CharField(max_length=50, default='')
    createdAt = models.DateTimeField(auto_now=True)
    midiFile = models.FileField(upload_to="midiFile", blank=True, null= True)
    jsonFile = models.FileField(upload_to="jsonFile", blank=True, null= True)
    tempo = models.IntegerField(default=120)
    onboard = models.ForeignKey('Billboard', blank=True, null=True, related_name='blockOnBoard')
    composedBy = models.ForeignKey(STUser, blank=True, related_name='composedBlocks', null=True, on_delete=models.CASCADE)
    collectedBy = models.ForeignKey(STUser, related_name='collectedBlocks', null=True, blank=True, on_delete=models.CASCADE)

class MusicPiece(models.Model):
    title = models.CharField(max_length=50, default='')
    composedBy = models.ForeignKey(STUser, blank=True, related_name='composedMusic', null=True, on_delete=models.CASCADE)
    collectedBy = models.ForeignKey(STUser, related_name='collectedMusic', null=True, blank=True, on_delete=models.CASCADE)
    musicBlocks = models.ForeignKey(MusicBlock, blank=True, related_name='block', null=True)
    audioFile = models.FileField(blank=True, null=True)
    onboard = models.ForeignKey('Billboard', blank=True, null=True, related_name='pieceOnBoard')
    
class Billboard(models.Model):
    setupAt = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    info = models.CharField(max_length=120, null=True, blank=True)
    address1 = models.CharField(max_length=50, null=True, blank=True)
    address2 = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location = models.PointField(u'LocationPoint', geography=True)
    objects = models.GeoManager()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.location = Point(self.latitude, self.longitude)
        super(Billboard, self).save()

class instStatus(models.Model):
    file = models.FileField(upload_to="instStatus", blank=True, null= True)
    block = models.ForeignKey(MusicBlock, blank=True, related_name='instStatus', null=True, on_delete=models.CASCADE)

class fxStatus(models.Model):
    file = models.FileField(upload_to="fxStatus", blank=True, null= True)
    block = models.ForeignKey(MusicBlock, blank=True, related_name='fxStatus', null=True, on_delete=models.CASCADE)


# # Model for original MIDI Files
# class MIDIFiles(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     owner = models.ForeignKey(User, to_field='id')
#     datafile = models.FileField()
#     fileInfo = models.OneToOneField('MIDIInfo', on_delete=models.CASCADE, blank=True, null=True)
#     parsed = models.BooleanField(default=False)
#     def delete(self, using=None, keep_parents=False):
#         self.fileInfo.delete()
#
# # Model for information retrieved from MIDI Files
# class MIDIInfo(models.Model):
#     filename = models.CharField(max_length=100, null=True)
#     artist = models.ForeignKey('Artist', null=True)
#     tempo = models.FloatField(max_length=10, null=True)
#     key = models.CharField(max_length=2, null=True)
#     timeSignature = models.CharField(max_length=20, null=True)
#     duration = models.FloatField(max_length=100, null=True)
#     tracks = models.TextField(null=True)
