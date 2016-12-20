from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
# Create your models here.

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class MyUser(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        try:
            validate_email(self.email)
            validate_password(self.password, self)
            self.save()
            return self
        except ValidationError:
            return ValidationError

# Model for original MIDI Files
class MIDIFiles(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, to_field='id')
    datafile = models.FileField()
    fileInfo = models.OneToOneField('MIDIInfo', on_delete=models.CASCADE, blank=True, null=True)
    parsed = models.BooleanField(default=False)
    def delete(self, using=None, keep_parents=False):
        self.fileInfo.delete()

# Model for information retrieved from MIDI Files
class MIDIInfo(models.Model):
    filename = models.CharField(max_length=100, null=True)
    artist = models.ForeignKey('Artist', null=True)
    tempo = models.FloatField(max_length=10, null=True)
    key = models.CharField(max_length=2, null=True)
    timeSignature = models.CharField(max_length=20, null=True)
    duration = models.FloatField(max_length=100, null=True)
    tracks = models.TextField(null=True)


# Model for Artists
class Artist(models.Model):
    name = models.CharField(max_length=50)
    works = models.ManyToManyField('MIDIFiles', blank=True)