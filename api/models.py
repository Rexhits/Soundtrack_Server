from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
import cities
# Create your models here.

class STUser(AbstractUser):
    avatar = models.ImageField()
    birthday = models.DateField(null=True)
    selfIntro = models.CharField(max_length=200)
    favoriteGenres = models.CharField(max_length=200)
    contry = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20, null=True)

@receiver(post_save, sender=STUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class MusicBlock(models.Model):
    midiFile = models.FileField()
    createdAt = models.DateTimeField(auto_now=True)
    genre = models.CharField(max_length=30)
    tempo = models.IntegerField()
    blockConfigFile = models.FileField()
    engineConfigFile = models.FileField()
    collectedBy = models.OneToOneField(STUser, blank=True, related_name='musicBlock_collectedBy')
    composedBy = models.ForeignKey(STUser, on_delete=models.CASCADE, related_name='musicBlock_composedBy')



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
