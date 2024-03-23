from django.db import models

# Create your models here.
class senderModel(models.Model):
      file = models.FileField( upload_to="media/sender", max_length=100)
class receiverModel(models.Model):
      file = models.FileField( upload_to="media/receiver", max_length=100)