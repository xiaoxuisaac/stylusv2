from __future__ import unicode_literals
import os
from django.db import models
from django.utils import timezone
from ums.models import Profile
from ums.signals import user_registered
from django.dispatch import receiver
from ums.models import Profile
import datetime

# Create your models here.
class OcrFile(models.Model):
    saved_date = models.DateTimeField(editable=False, default=timezone.now)
    owner = models.ForeignKey(Profile, blank=True, null=True, related_name='ocr_files')
    upload = models.FileField(upload_to='ocr/%Y/%m/')
    show = models.BooleanField(default=True)
    def filename(self):
            return os.path.basename(self.upload.name)

def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(models.signals.post_delete, sender=OcrFile)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.upload:
        _delete_file(instance.upload.path)

class OcrBundleBase(models.Model):
    initial_value=models.IntegerField(default=100)
    expiration_date=models.IntegerField(default=100)
    repeat=models.IntegerField(default=1)
    name=models.CharField(max_length=100, blank=True, default='New Customer')
    class Meta:
        abstract = True

class OcrBundleModel(OcrBundleBase):
    code=models.CharField(max_length=20, blank=True, default='NEW_CUSTOMER')

class OcrBundle(OcrBundleBase):
    user=models.ForeignKey(Profile, related_name='ocrbundles', on_delete=models.CASCADE,null=True)
    remains=models.IntegerField(default=100)
    repeat_remain=models.IntegerField(default=0)
    expired=models.BooleanField(default=False)
    activation_date=models.DateTimeField(editable=False)

    @classmethod
    def create_from_code(self,invitation,user=None):
        base=OcrBundleModel.objects.filter(code=invitation)
        if len(base)==0 or invitation=='': return
        else:
            base=base[0]
            b=OcrBundle(initial_value=base.initial_value,
                        expiration_date=base.expiration_date,
                        repeat=base.repeat,
                        name=base.name)
            try:
                b.user=user.profile
            except:
                b.user=user
            b.repeat_remain=b.repeat-1
            b.remains=b.initial_value
            b.save()
            return b
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.activation_date = timezone.now()
        return super(OcrBundle, self).save(*args, **kwargs)

    def copy(self,user=None):
        try:
            b=OcrBundle(user=user,initial_value=self.initial_value,
                        expiration_date=self.expiration_date,
                        repeat=self.repeat,
                        name=self.name)
            b.repeat_remain=b.repeat-1
            b.remains=b.initial_value
            b.save()
            return b
        except:
            return False

    def renew(self):
        expiration_date = datetime.timedelta(self.expiration_date*(self.repeat-self.repeat_remain))
        if self.activation_date + expiration_date > timezone.now():
            return True
        elif self.repeat_remain <= 0:
            self.expired=True
            self.save()
            return False
        else:
            self.repeat_remain=self.repeat_remain-1
            self.remains=self.initial_value
            self.save()
            return self.renew()


    def remain(self):
        self.renew()
        if self.expired: return 0
        return self.remains
    def __unicode__(self):
        return self.name

@receiver(user_registered)
def addocrfromregistration(user, request, **kwargs):
    ps=Profile.objects.filter(invitation=user.profile.invite_code)
    if ps.count()>0:
        OcrBundle.create_from_code('NEW_USER_INVITED', user.profile)
        p=OcrBundle.create_from_code('NEW_INVITEE', ps[0])
        p.name=('New Invitee '+user.get_username())
        p.save()
    else:
        OcrBundle.create_from_code(user.profile.invite_code, user.profile)