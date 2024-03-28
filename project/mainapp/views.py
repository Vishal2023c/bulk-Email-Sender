from django.shortcuts import render,HttpResponse,redirect
from .forms import receiverForm
from user.models import senderFileModel,receiverFileModel
from project.celery import *
from .tasks import send_mail, add

import re


# Create your views here.

def  home(request): 
      return render(request,'index.html')

def sendmail(request):
      if request.method == "POST":
            subject = request.POST['subject']
            message = request.POST['message']
            number = request.POST['number']
            file = receiverFileModel.objects.all()

            emails=[]
            for emailfile in file:
                  if emailfile.author == request.user:
                        with open(emailfile.file.path,'r') as f:
                              f=f.read().splitlines()
                              for i in f:
                                    if re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',i):
                                          emails.append(i)
            sending = send_mail(args=[emails,message,subject,number])

      return render(request,'index.html')






