from django.shortcuts import render,HttpResponse,redirect
from .forms import senderForm,receiverForm
from .models import senderModel,receiverModel

# Create your views here.

def  home(request):
      sform = senderForm
      rform = receiverForm
      context = {"sform":sform,"rform":rform}
      return render(request,'index.html',context)

def upload(request):
      
      if request.method == "POST":
            value = request.POST['value']
            if int(value)==1:
                  form = senderForm(request.POST)
                  file = request.FILES['file']
                  print('sender')
                  model = senderModel.objects.create(file = file)
                  
            elif int(value)==2:
                  form = receiverForm(request.POST)
                  file = request.FILES['file']
                  print('receiver')
                  model = receiverModel.objects.create(file = file)
      return redirect(home)