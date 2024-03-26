from django.shortcuts import render,redirect
from .forms import UserRegisterForm,receiverFileForm,senderFileForm
from .models import senderFileModel,receiverFileModel
from django.views.generic import ListView
from django.core import mail
from django.conf import settings
from django.core import exceptions 
from django.contrib.auth.decorators import login_required
import random
import re 


# Create your views here.
# def login(request):
#       return render(request,'login.html')

def registration(request):
      if request.method == "POST":
            otp = random.randrange(11111, 99999)
            email = request.POST.get('email', False)
            msg = 'Your OTP is {}'.format(otp)
            sending = mail.send_mail('varification code', msg, settings.      EMAIL_HOST_USER, [ email], fail_silently=False)
            request.session['otp'] = otp
            request.session['email'] = email
            return render(request,"registration.html",{'temp':'temp'})


      return render(request,"registration.html")

def varifyotp(request):
      if request.method == 'POST':
            s_otp = request.session['otp']
            email = request.session['email']
            otp = request.POST['userotp']
            if int(otp) == (s_otp):

                  return redirect(register)
            else:
                  message = 'Wrong OTP Please Try Again'

                  return render(request,"registration.html",{'temp':'temp'})
                  
def register(request):
      if request.method == "POST":
             
            u_fm = UserRegisterForm(request.POST, instance=request.user.id)
            if request.session['otp']:
                  del request.session['otp']
            if u_fm.is_valid():
                 username = request.POST['username']
                 request.session['Username'] = username
                 u_fm.save()
                 return redirect("login")
      form = UserRegisterForm()
      return render(request,"register.html",{'form':form})




def profile(request):
    
      sender = senderFileModel.objects.all()
      receiver = receiverFileModel.objects.all()
      context = {'sender':sender, "receiver":receiver}

      return render(request, 'profile.html',context)
    
    
#     template_name = 'profile.html'

#     def get(self, request, *args, **kwargs):

@login_required
def uploadfile(request):
      form1 = senderFileForm()
      form2 = senderFileForm()
      temp = False

      if request.method == "POST":
            value = request.POST['value']
            
            if int(value) == 1:
                  user = request.user
                  file = request.FILES['file']
                  model = senderFileModel.objects.all()
                  for i in model:
                        if request.user==i.author:
                              i.delete()
                  senderFileModel.objects.create(file=file,author=user)
                  temp = True

            elif int(value) == 2:
                  user = request.user
                  file = request.FILES['file']
                  receiverFileModel.objects.create(file=file,author=user)
                  temp = True

      context = {'form1':form1,'form2':form2,'temp':temp}

      return render(request,'uploadfiles.html',context)

def deletefile(request,id):
      
      receiverFileModel.objects.get(id=id).delete()

      return redirect('profile')


@login_required
def composeMail(request):

      return render(request,'composeMail.html')


# def send(request):
#       if request.method == "POST":
#             subject = request.POST['subject']
#             message = request.POST['message']
#             number = request.POST['number']
#             email=

#             sending = mail.send_mail(subject, message, settings.      EMAIL_HOST_USER, [ email], fail_silently=False)*

      # if True:
      #       return redirect(composeMail)
      


def send(request):
      if request.method == "POST":
            subject = request.POST['subject']
            message = request.POST['message']
            number = request.POST['number']
            file = receiverFileModel.objects.all()
            
            for emailfile in file:
                  if emailfile.author == request.user:
                        with open(emailfile.file.path,'r') as f:
                              f=f.read().splitlines()
                              ls=[]
                              for i in f:
                                    print(i)
                                    if re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',i):
                                          print('matched')

                                          sending = mail.send_mail(subject, message, settings.EMAIL_HOST_USER,[i], 
                                          fail_silently=False)
                                          
                                          


            # sending = mail.send_mail('varification code', message, settings.      EMAIL_HOST_USER, [], fail_silently=False)
      else:
            print('no post')
      if True:
            return redirect(composeMail)





