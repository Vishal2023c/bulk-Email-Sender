from celery import Celery, shared_task
from django.conf import settings
from django.core import mail
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from user.models import senderFileModel,receiverFileModel
from django.core.exceptions import *
from mainapp.tasks import *


# Create your tasks here
from celery import shared_task

app = Celery('tasks', broker='pyamqp://guest@localhost//')



# for files in senderfile:
#             if request.user == files.author:
#                   with open(files.file.path,"r") as f:
#                         f=f.read().splitlines()
#                         for email in f:
#                               ls.append(email.split(','))
#                               # print(email.split(','))

#       # print(ls[0][1])
#       print(dict(ls))

@shared_task
def send_mail(sender, receiver, message, subject, number):

      # sender={'gmahendrasingh304@gmail.com':'khblgwegzayibvxx',
      #         'mahendrasinghstudy6977@gmail.com':'wnpnidzcozxygqiy'}
      
      message = message
      number = int(number)
      subject = subject
      senderfailed = {''}
      x=0
      for m, p in sender.items():
            settings.EMAIL_HOST_USER = m
            settings.EMAIL_HOST_PASSWORD = p
            print(m)

            for i in range(1,number):
                  try:
                        sending = EmailMessage(subject, message,to=[receiver[x]])
                        sending.content_subtype='html'
                        sending.send()
                        # sending = mail.send_mail(subject, message, settings.EMAIL_HOST_USER,  [receiver[x]],fail_silently=False)
                        x+=1
                  except: 
                        senderfailed.add(m)                    
                        break
                  if x==len(receiver):
                        print(senderfailed)
                        return True
      
      
      else:
            return False
                  


@shared_task
def add(x,y):
      print(x+y)
      return x+y











