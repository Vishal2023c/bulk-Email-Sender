from django.shortcuts import render,redirect,HttpResponse
from .forms import UserRegisterForm,receiverFileForm,senderFileForm
from django.contrib.auth.models import User
from .models import senderFileModel,receiverFileModel
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .tasks import signup_otp, signup_success,pass_reset_otp
import random



def sendMail(request):
      if request.method == "POST":
            otp = random.randrange(11111, 99999)
            email = request.POST.get('email', False)

            if User.objects.filter(username=email).first():
                  messages.success(request,'Email is already registered')
                  return redirect(registration)

            else : 
                  task = signup_otp(email,otp) 
                  if task == True:
                        request.session['otp'] = otp
                        request.session['email'] = email
                        messages.success(request,'Otp sent ')
                        return redirect(registration)
      return redirect('login')

def registration(request):

      return render(request,"emailvarify.html")

def varifyotp(request):
      if request.method == 'POST':
            s_otp = request.session['otp']
            email = request.session['email']
            otp = request.POST['userotp']
            if int(otp) == (s_otp):

                  messages.success(request,'OTP Verify SuccessFully...')
                  return redirect(register)
            else:
                  messages.success(request,'Wrong OTP Please Try Again')
                  return render(request,"emailvarify.html")
                  
def register(request):
      if request.method == "POST":
             
            u_fm = UserRegisterForm(request.POST, instance=request.user.id)
            try:
                  if request.session['otp']:
                        del request.session['otp']
                  if request.session['email']:
                        del request.session['email']
            except:
                  pass

            if u_fm.is_valid():
                  username = request.POST['username']
                  request.session['Username'] = username
                  u_fm.save()

                  email = request.session['Username']
                  try:
                        task = signup_success(email)
                  except:
                        pass
                  messages.success(request,'Sing-Up SuccessFully...')

                  return redirect("login")
            else:
                  pass
            
      form = UserRegisterForm()
      return render(request,"register.html",{'form':form})


@login_required
def profile(request):  
      user = request.user
      file = senderFileModel.objects.get(author=user)
      receiverfile = receiverFileModel.objects.all()
      context = {'file':file, "receiver":receiverfile}

      return render(request, 'profile.html',context)

def resetPassword(request):
      if request.method == "POST":
            otp = random.randrange(11111, 99999)
            email = request.POST.get('email', False)
            task = pass_reset_otp(email,otp)
            request.session['otp'] = otp
            request.session['email'] = email
            return render(request,"passwordReset.html",{'temp':'temp'}  )
      
      return render(request,'passwordReset.html')

def changePassword(request):
      if request.method == "POST":
            password1 = request.POST['password1'] 
            password2 = request.POST['password2']
            user_otp = request.POST['userotp']
            email = request.session['email']
            otp = request.session['otp']
            if int(user_otp) == otp:
                  if password1 == password2:
                        user = User.objects.get(username=email )
                        user.set_password(password1)
                        user.save()
                        messages.success(request,'Password changed successfully')
                        del request.session['email']
                        del request.session['otp']
                        return redirect("login")
            else:
                  messages.error(request,'wrong otp please try again')
                  return render(request,'passwordReset.html')
      return render('home')
                   
                  



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
                  esp = request.POST['esp']
                  port = request.POST['port']
                  model = senderFileModel.objects.all()
                  for i in model:
                        if request.user==i.author:
                              i.delete()
                  senderFileModel.objects.create(file=file,author=user,esp=esp,port=port)
                  messages.success(request,' Sender Email File Uploaded successfully')
                  temp = True

            elif int(value) == 2:
                  user = request.user
                  file = request.FILES['file']
                  receiverFileModel.objects.create(file=file,author=user)
                  messages.success(request,'Recipients Email File Uploaded successfully')
                  temp = True

      context = {'form1':form1,'form2':form2}

      return render(request,'uploadfiles.html',context)


#to delete file from user action
def deletefile(request,id):
      
      receiverFileModel.objects.get(id=id).delete()

      return redirect('profile')


def updatefile(request,id,value):
      if value == 0:
            data = senderFileModel.objects.get(id=id)
            sender = []
            if request.user == data.author:
                  with open(data.file.path,"r") as f:
                        f=f.read().splitlines()
                        for email in f:
                              sender.append(email.split(','))
            sender.sort()
            datalist = dict(sender)
            x=0
            return render(request,'updatefile.html',{'data':datalist,'x':x})


      elif value == 1:
            data = receiverFileModel.objects.get(id=id)
            datalist = []
            if request.user == data.author:
                  with open(data.file.path) as f:
                        f=f.read().splitlines()
                        datalist = list(f)
                  x=1
            datalist.sort()
            return render(request,'updatefile.html',{'data':datalist,'x':x})


@login_required
def composeMail(request):
      user = request.user
      listfile=[]
      try:
            files = receiverFileModel.objects.all()
            for file in files:
                  if file.author == user:
                        listfile.append(file)
            return render(request,'composeMail.html',{'files':listfile})
            
      except:
            messages.error(request,'Please first upload Recipients list ')

      return render(request,'composeMail.html')






