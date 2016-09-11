from django.utils.translation import ugettext as _
from django.forms import ModelForm
from .models import UserProfile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

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

    def clean_registration_number(self):
        registration_number = self.cleaned_data.get('registration_number')
        if not registration_number.isdigit():
            self.add_error('registration_number','Insira apenas números')
        return registration_number

    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if name is (None or ''):
            self.add_error('name','Insira um nome válido!')
        
        if ((len(name) < 3) or (len(name) > 30)):
            self.add_error('name','Nomes entre 3 e 50 caracteres!')       
        
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email is (None or ''):
            self.add_error('email','Email inválido!')

        if not ('@' and '.com') in email :
            self.add_error('email','Email inválido!')        

        return email


    def clean(self):
        cleaned_data = super(NewUserForm,self).clean()
        
        if ((len(cleaned_data.get('password')) < 6) or (len(cleaned_data.get('password')) > 15)):
            self.add_error('password','Senhas entre 6 e 15 caracteres!')
            self.add_error('repeat_password','')

        else:    
            if cleaned_data.get('password') != cleaned_data.get('repeat_password'):
                self.add_error('password','Senhas não conferem.')
                self.add_error('repeat_password','')

        return cleaned_data    

    class Meta:
        model = UserProfile
        exclude = ['user']

class EditUserForm (ModelForm):

    current_password = forms.CharField(label = _('Current Password'), widget = forms.PasswordInput())
    new_password = forms.CharField(label = _('New Password'), widget = forms.PasswordInput())
    repeat_new_password = forms.CharField(label = _('Repeat New Password'), widget = forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['first_name', 'email','password']   
        widgets = {'password': forms.HiddenInput()}

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        if first_name is (None or ''):
            self.add_error('first_name','Insira um nome válido!')
        
        if (len(first_name) < 3) and (len(first_name) < 30):
            self.add_error('first_name','Nomes entre 3 e 50 caracteres!')       
        
        return first_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email is (None or ''):
            self.add_error('email','Email inválido!')

        return email

    

    def clean(self):
        cleaned_data = super(EditUserForm,self).clean()
        current_password = cleaned_data['current_password']
        password = cleaned_data['password']
        new_password = cleaned_data['new_password']
        repeat_new_password = cleaned_data['repeat_new_password']

        if not check_password(current_password,password):
            self.add_error('current_password','Senha atual inválida!')

            if new_password != repeat_new_password:    
                self.add_error('new_password','Senhas não conferem.') 
                self.add_error('repeat_new_password','')

        else:
            if new_password == repeat_new_password:
                self.instance.set_password(new_password)
                cleaned_data['password'] = self.instance.password   
            else:
                self.add_error('new_password','Senhas não conferem.') 
                self.add_error('repeat_new_password','') 
        
        return cleaned_data


