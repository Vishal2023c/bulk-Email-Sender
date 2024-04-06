from django.shortcuts import render,HttpResponse,redirect
from .forms import receiverForm
from user.models import senderFileModel,receiverFileModel
from project.celery import add
from .tasks import send_mail, add
from django.contrib.auth.models import User
from django.contrib import messages 

import re


# Create your views here.

def  home(request): 

      return render(request,'index.html')

def sendmail(request):
      if request.method == "POST":
            subject = request.POST['subject']
            message = request.POST['message']
            number = request.POST['number']
            try:
                  id = request.POST['file']
            except:
                  messages.success(request,'Please select Recipients email list')
                  return render(request,'composeMail.html')

            file = receiverFileModel.objects.get(id=id)

            receiver=[]
            with open(file.file.path,'r') as f:
                  f=f.read().splitlines()
                  for i in f:
                        if re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9][A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',i):
                              receiver.append(i)
            sender = []
            try:
                  files = senderFileModel.objects.all()
                  print(files)
            except:
                  messages.success(request,'Please Upload sender email cridential file')
                  return render(request,'composeMail.html')


            for file in files:
                  if request.user == file.author:
                        with open(file.file.path,"r") as f:
                              f=f.read().splitlines()
                              for email in f:
                                    sender.append(email.split(','))
                                    # print(email.split(','))
            
            sender = dict(sender)
                                          
            sending = send_mail.delay(sender, receiver, message, subject, number)
            messages.success(request,'Mail sending in progress! do not refresh page')

      return redirect('home')






