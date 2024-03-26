from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class receiverFileModel(models.Model):
      file = models.FileField( upload_to='reciever/', max_length=100)
      author = models.ForeignKey(User,  on_delete=models.CASCADE)


class senderFileModel(models.Model):
      file = models.FileField( upload_to='sender/', max_length=100)
      author = models.ForeignKey(User,  on_delete=models.CASCADE)
    
