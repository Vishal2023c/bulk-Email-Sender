from django.contrib import admin
from .models import senderModel,receiverModel
# Register your models here.

@admin.register(senderModel)
class registerSenderModel(admin.ModelAdmin):
      list_display=['file']


@admin.register(receiverModel)
class registerReceiverModel(admin.ModelAdmin):
      list_display=['file']
