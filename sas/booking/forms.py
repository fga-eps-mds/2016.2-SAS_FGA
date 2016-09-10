from django.forms import ModelForm
from .models import UserProfile
from django import forms
from django.contrib.auth.models import User
from booking import models
class UserForm(ModelForm):
  name = forms.CharField(label = 'Nome Completo:', widget=forms.TextInput(attrs={'placeholder': ''}))
  email = forms.CharField(label = 'Email:', widget=forms.TextInput(attrs={'placeholder': ''}))
  password = forms.CharField(label = 'Senha:', widget = forms.PasswordInput(attrs={'placeholder': ''}))
  repeat_password = forms.CharField(label = 'Repetir Senha:', widget = forms.PasswordInput(attrs={'placeholder': ''}))
  registration_number = forms.CharField(label = 'Matricula:', widget=forms.TextInput(attrs={'placeholder': ''}))
  category = forms.ChoiceField(choices = models.CATEGORY, label = 'Categoria:')

  def save(self, force_insert=False, force_update=False, commit=True):
    userprofile = super(UserForm, self).save(commit=False)
    user = User()
    user.name = self.cleaned_data.get('name')
    user.email = self.cleaned_data.get('email')
    user.username = self.cleaned_data.get('username')
    user.set_password(self.cleaned_data.get('password'))
    user.save()

    userprofile.user = user
    # do custom stuff
    if commit:
        userprofile.save()
    return userprofile

  def clean(self):
    cleaned_data = super(UserForm,self).clean()
    if cleaned_data.get('password') != cleaned_data.get('repeat_password'):
        self.add_error('password','Senhas nao conferem.')
  class Meta:
    model = UserProfile
    exclude = ['user']
