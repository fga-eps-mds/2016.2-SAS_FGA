from django.forms import ModelForm
from .models import UserProfile
from django import forms

class UserForm(ModelForm):
  name = forms.CharField(label = 'Nome:')
  email = forms.CharField(label = 'Email:')
  password = forms.CharField(label = 'Senha:', widget = forms.PasswordInput())
  repeat_password = forms.CharField(label = 'Repetir Senha:', widget = forms.PasswordInput())

  def save(self):
    user = User()
    user.name = self.name
    user.email = self.email
    user.set_password(self.password)
    user.save()
    super(UserForm,self).save()
  def clean(self):
    cleaned_data = super(UserForm,self).clean()
    if cleaned_data.get('password') != cleaned_data.get('repeat_password'):
        self.add_error('password','Senhas não conferem.')
  class Meta:
    model = UserProfile
    exclude = ['user']
