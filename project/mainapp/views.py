from django.shortcuts import render,HttpResponse,redirect
from .forms import receiverForm
from project.celery import add


# Create your views here.

def  home(request):
      result = add.delay(5,10)      
      return render(request,'index.html')


def send(request):
      
      return redirect()


