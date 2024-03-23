from django import forms
from .models import senderModel,receiverModel

class senderForm(forms.ModelForm):

      class Meta:
            model = senderModel
            fields = {'file'}
      
      def __init__(self, *args, **kwargs):
            super(senderForm, self).__init__(*args, **kwargs)
            self.fields['file'].widget.attrs['class'] = 'form-class'
            self.fields['file'].widget.attrs['accept'] = '.csv, .txt'


class receiverForm(forms.ModelForm):

      class Meta:
            model = receiverModel
            fields = {'file'}
      
      def __init__(self, *args, **kwargs):
            super(receiverForm, self).__init__(*args, **kwargs)
            self.fields['file'].widget.attrs['class'] = 'form-class'
            self.fields['file'].widget.attrs['accept'] = '.csv, .txt'
