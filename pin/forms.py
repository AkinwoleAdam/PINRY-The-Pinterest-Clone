from django import forms
from django.forms import ModelForm
from .models import *

class PinForm(forms.ModelForm):
  class Meta:
    model = Pin
    fields = '__all__'
    exclude = ['user']
  def __init__(self, user, *args, **kwargs):
    super(PinForm, self).__init__(*args, **kwargs)
    self.fields['board'].queryset = Board.objects.filter(user=user)
 
class EditPinForm(forms.ModelForm):
  class Meta:
    model = Pin
    fields = '__all__'
    exclude = ['user','board','file']
 
class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = '__all__'
    exclude = ['user','pin']

class SaveToBoardForm(forms.ModelForm):
  class Meta:
    model = Pin
    fields = ['board']
    def __init__(self, user, *args, **kwargs):
      super(SaveToBoardForm, self).__init__(*args, **kwargs)
      self.fields['board'].queryset = Board.objects.filter(user=user)
        
class BoardForm(forms.ModelForm):
  class Meta:
    model = Board
    fields = '__all__'
    exclude = ['user']
  
class EditProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = '__all__'
    exclude = ['user']
    
class UserUpdateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username','first_name','last_name']