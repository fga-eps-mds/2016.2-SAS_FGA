from django.utils.translation import ugettext as _
from django.forms import ModelForm
from .models import UserProfile
from django import forms
from django.contrib.auth.models import User

class NewUserForm(ModelForm):
  name = forms.CharField(label = _('Name'))
  username = forms.CharField(label = _('Username'))
  email = forms.CharField(label = _('Email'))
  password = forms.CharField(label = _('Password'), widget = forms.PasswordInput())
  repeat_password = forms.CharField(label = _('Repeat Password'), widget = forms.PasswordInput())

  def save(self, force_insert=False, force_update=False, commit=True):
    userprofile = super(NewUserForm, self).save(commit=False)
    user = User()
    user.first_name = self.cleaned_data.get('name')
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
    cleaned_data = super(NewUserForm,self).clean()
    if cleaned_data.get('password') != cleaned_data.get('repeat_password'):
        self.add_error('password','Senhas não conferem.')
  class Meta:
    model = UserProfile
    exclude = ['user']

class EditUserForm (ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'email']        

    