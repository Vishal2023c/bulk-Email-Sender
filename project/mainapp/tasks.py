from celery import Celery, shared_task
from django.core.exceptions import *
from mainapp.tasks import *  
from time import sleep
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep
from django.core.mail import send_mail


from django.core.mail import EmailMultiAlternatives

# Create your tasks here
from celery import shared_task

app = Celery('tasks', broker='pyamqp://guest@localhost//')



@shared_task
def bulk_mail_sender(context):
      return True


# @shared_task
# def sendMail(context):
#       sender = context[0]
#       recipients = context[1]
#       subject = context[2]
#       number= int(context[4])
#       task_name = context[5]
#       failed_recipients = context[6]
#       # esp = context[7]
#       failed_sender = {''}
#       success_sender = {''}
#       index = 0
#       # settings.EMAIL_HOST = 'mail.geektheo.com'

#       try:
#             for username, password in sender.items():#smtp username and pass to login smtp serve
#                   settings.EMAIL_HOST_USER = username
#                   settings.EMAIL_HOST_PASSWORD = password
#                   print(username)
#                   print(password)

#                   # for i in range(1,number):
#                   #       try:
#                   #             msg_content= f"""{context[3]}"""
#                   #             # msg = EmailMultiAlternatives(subject,msg_content, username,[recipients[index]])
#                   #             # msg.attach_alternative(msg_content, "text/html")
#                   #             # msg.send()  
#                   #             ssend = send_mail(subject,msg_content,settings.EMAIL_HOST_USER,[recipients[index]])
#                   #             success_sender.add(username)                    
#                   #             index +=1  
#                   #       except Exception as e: 
#                   #             print(e)
#                   #             failed_sender.add(username)                    
#                   #             break
#                   #       if index==len(recipients):
#                   #             contetx = {'sender':sender, 'recipients':recipients, 'failed_recipients':failed_recipients, 'failed_sender':failed_sender, 'task_name':task_name} 
#                   #             return context
#                   return 0
#       except Exception as e:
#             return 'not sent'
                  


@shared_task
def add(x,y):
      sleep(10)
      return x+y





# subject, from_email, to = "hello", "bulkmail1@geektheo.com", "mahendrasinghstudy6977@gmail.com"
#       text_content = "This is an important message."
#       html_content = "<p>This is an <br><strong>i<h1>mportant</h1></strong> message.</p>"
#       msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#       msg.attach_alternative(html_content, "text/html")
#       msg.send()