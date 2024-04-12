from django.shortcuts import render,HttpResponse,redirect
from .forms import receiverForm
from user.models import senderFileModel,receiverFileModel
from .tasks import bulk_mail_sender,add
from celery.result import AsyncResult
from django.contrib.auth.models import User
from django.contrib import messages 
import re


from django.core.mail import EmailMultiAlternatives
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
            
 
# Create your views here.

def  home(request):
      try:
            if request.session['otp']:
                  del request.session['otp']
            if request.session['email']:
                  del request.session['email']
      except:
            pass
      
      
      return render(request,'index.html')

def sendmail(request):
      if request.method == "POST":
            subject = request.POST['subject']
            message = request.POST['message']
            number = request.POST['number']
            task_name = request.POST['task_name']
            try:
                  id = request.POST['file']
            except:
                  messages.success(request,'Please select Recipients email list')
                  return render(request,'composeMail.html')

            file = receiverFileModel.objects.get(id=id)

            receiver=[]
            failed_receiver = []
            with open(file.file.path,'r') as f:
                  f=f.read().splitlines()
                  for i in f:
                        if re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9][A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',i):
                              receiver.append(i)
                        else:
                              failed_receiver.append(i)
            try:
                  files = senderFileModel.objects.all()
            except:
                  messages.success(request,'Please Upload sender email cridential file')
                  return render(request,'composeMail.html')

            sender = []
            esp = str
            port = int

            for file in files:
                  if request.user == file.author:
                        esp = file.esp
                        port = file.port

                        with open(file.file.path,"r") as f:
                              f=f.read().splitlines()
                              for email in f:
                                    sender.append(email.split(','))
            
            sender = dict(sender)
            context=[sender, receiver,  subject, message, number, task_name, failed_receiver,esp,port]
            task = bulk_mail_sender.delay(context)
            request.session['task'] = task.id
            messages.success(request,'Mail sending in progress! you can check progress in result tab.  do not refresh page.')

      return redirect('home')

def result(request,id):
      try:
            task_result = AsyncResult(id)
            sender, recipients, failed_recipients, failed_sender,success_recipient,    task_name = task_result.result
            context = {"sender":sender, "recipients":recipients,  "failed_recipients":failed_recipients, "failed_sender":failed_sender,    "success_recipient":success_recipient, "task_name":task_name}
      except Exception as e:
            pass

      print(task_name)
      return render(request,"result.html",context)






