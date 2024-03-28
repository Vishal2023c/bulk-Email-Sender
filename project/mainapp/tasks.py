from celery import Celery, shared_task
from django.conf import settings
from django.core import mail
from user.models import senderFileModel,receiverFileModel
from mainapp.tasks import *

# Create your tasks here
from celery import shared_task

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@shared_task
def send_mail(emails,msg,sub,number):

      sender={'gmahendrasingh304@gmail.com':'khblgwegzayibvxx',
              'mahendrasinghstudy6977@gmail.com':'wnpnidzcozxygqiy'}
      
      message = msg
      number = int(number)
      subject = sub
      file = receiverFileModel.objects.all()
      x=0
      for m, p in sender.items():
            settings.EMAIL_HOST_USER = m
            settings.EMAIL_HOST_PASSWORD = p
            print(m)

            for i in range(1,number):
                  sending = mail.send_mail(subject, message, settings.EMAIL_HOST_USER,  [emails[x]],fail_silently=False)
                  if x==len(emails):
                        return True
                  x+=1


@shared_task
def add(x,y):
      print(x+y)
      return x+y











