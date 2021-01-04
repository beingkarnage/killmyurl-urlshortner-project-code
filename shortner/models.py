from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Url(models.Model):
    original_link = models.CharField(max_length=255,unique=True ,null=False, blank=True)
    generated_link = models.CharField(max_length=20,null=False,blank=True)
    visits = models.BigIntegerField(null=False,blank=False,default=0)
    date_created = models.DateField(auto_now=True)
    uid = models.IntegerField(primary_key=True)
    def __str__(self):
        return self.generated_link

def createUserProfile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(createUserProfile,sender=User)

class UserProfile(models.Model):
    user = models.OneToOneField(User , blank=True,null= True,on_delete=models.CASCADE)
    email_confirm =models.BooleanField(default=False,null=False,blank=False)

    def __str__(self):
        return str(self.user)