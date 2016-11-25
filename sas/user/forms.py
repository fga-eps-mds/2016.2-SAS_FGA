from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from .models import UserProfile, Validation
from .models import CATEGORY, ENGINEERING, Settings
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class UserProfileForm(forms.Form):
    name = forms.CharField(
        label=_('Name:'),
        widget=forms.TextInput(attrs={'placeholder': ''}))
    registration_number = forms.CharField(
        label=_('Registration number:'),
        widget=forms.TextInput(attrs={'placeholder': ''}))
    category = forms.ChoiceField(choices=CATEGORY, label=_('Category:'))
    email = forms.EmailField(
        label=_('Email:'),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'example@email.com'}),
        error_messages={'invalid': _('Email address must \
                                       be in a valid format.')})
    password = forms.CharField(
        label=_('Password:'),
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': ''}))



class LoginForm(UserProfileForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self ).__init__(*args, **kwargs)
        self.fields.pop("category")
        self.fields.pop("name")
        self.fields.pop("registration_number")

    def authenticate_user(self):
        username = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError({'password':
                                  [_('Email or Password does not match'), ]})
        return user

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        self.authenticate_user()
        return cleaned_data


class PasswordForm(UserProfileForm):

    new_password = forms.CharField(
        label=_('New Password:'),
        widget=forms.PasswordInput(attrs={'placeholder': ''}))
    renew_password = forms.CharField(
        label=_('Repeat Password:'),
        widget=forms.PasswordInput(attrs={'placeholder': ''}))

    def __init__(self, *args, **kwargs):
        super(PasswordForm, self ).__init__(*args, **kwargs)
        self.fields.pop("email")
        self.fields.pop("category")
        self.fields.pop("name")
        self.fields.pop("registration_number")

    def save(self, user):
        password = self.cleaned_data.get("new_password")
        user.set_password(password)
        user.save()

    def is_password_valid(self, username):
        cleaned_data = super(PasswordForm, self).clean()
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            self.add_error('password', _('Current password is wrong'))
            return False
        return True

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        password1 = cleaned_data.get('new_password')
        password2 = cleaned_data.get('renew_password')
        if password1 and password2 and password1 != password2:
            raise ValidationError({'renew_password': [_('Passwords \
                                                         do not match'), ]})

        if len(password1) < 6 or len(password1) > 15:
            raise ValidationError({'new_password': [_('Password must be \
                                                       between 6 and 15 \
                                                       characters.'), ]})

class UserForm(UserProfileForm):

    repeat_password = forms.CharField(
        label=_('Repeat Password:'),
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': ''}))

    engineering = forms.ChoiceField(choices=ENGINEERING,
                                    label=_('Engineering:'))
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop("instance", None)
        editing = kwargs.pop("editing", None)
        super(UserForm, self ).__init__(*args, **kwargs)
        if instance is not None:
            self.__dict__["instance"] = instance
        if instance is not  None or editing is not None:
            self.fields.pop("password")
            self.fields.pop("repeat_password")
        if editing is None and instance is not None:
            self.fields["email"].initial = instance.user.email
            self.fields["category"].initial = instance.category
            self.fields["name"].initial = instance.full_name()
            self.fields["registration_number"].initial = instance.registration_number
            self.fields['engineering'].initial = instance.engineering

    def set_fields(self, userprofile):
        userprofile.name(self.cleaned_data.get('name'))
        userprofile.user.email = self.cleaned_data.get('email')
        userprofile.user.username = userprofile.user.email
        userprofile.engineering = self.cleaned_data.get('engineering')
        userprofile.registration_number = self.cleaned_data.get('registration_number')
        userprofile.category = self.cleaned_data.get('category')

    def update(self, userprofile):
        self.set_fields(userprofile)
        try:
            userprofile.save()
        except:
           raise Exception(_("Something went wrong so we could not save \
                             your data. Try again later"))
        return userprofile

    def insert(self):
        userprofile = UserProfile()
        userprofile.user = User()
        self.set_fields(userprofile)
        userprofile.user.set_password(self.cleaned_data.get('password'))
        try:
            userprofile.save()
            userprofile.make_as_academic_staff()
        except e:
           raise Exception(_("Something went wrong so we could not save \
                             your data. Try again later"))
        return userprofile

    def clean_registration_number(self):
        validation = Validation()
        rn = self.cleaned_data["registration_number"]
        if hasattr(self, "instance") and self.instance.registration_number == rn:
            return rn
        elif UserProfile.objects.filter(registration_number=rn).exists():
                raise ValidationError(_('Registration Number already exists.'))
        if (len(rn) is not 9):
            raise ValidationError([_('Registration Number must have 9 characters.'), ])
        if validation.hasSpecialCharacters(rn):
            raise ValidationError([_('Registration Number cannot \
                                      contain special characters.'), ])
        if validation.hasLetters(rn):
            raise ValidationError([_('Registration Number cannot \
                                      contain letters.'), ])

        return rn

    def clean_email(self):
        email = self.cleaned_data["email"]
        if hasattr(self,"instance") and self.instance.user.email == email:
            return email
        elif User.objects.filter(email=email).exists():
                raise ValidationError(_('Email already used.'))

        return email

    def clean_name(self):
        validation = Validation()
        name = self.cleaned_data['name']

        if (len(name) < 2 or len(name) > 50):
            raise ValidationError([_('Name must be between 2 and \
                                               50 characters.'), ])

        if validation.hasSpecialCharacters(name):
            raise ValidationError([_('Name cannot contain special \
                                               characters.'), ])

        if validation.hasNumbers(name):
            raise ValidationError([_('Name cannot contain numbers.'), ])
        return name

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        if "password" in self.fields and "repeat_password" in self.fields:
            password1 = cleaned_data['password']
            password2 = cleaned_data['repeat_password']

            if len(password1) < 6 or len(password1) > 15:
                raise ValidationError({'password': [_('Password must be \
                                                       between 6 and 15 \
                                                       characters.'), ]})

            if password1 and password2 and password1 != password2:
                raise ValidationError({'repeat_password': [_('Passwords do \
                                                              not match.'), ]})
        return cleaned_data

class SettingsForm(forms.Form):
    start_semester = forms.DateField(
        label=_('Semester Start:'),
        widget=forms.widgets.DateInput(
            attrs={'class': 'datepicker1', 'placeholder': _("mm/dd/yyyy")}))
    end_semester = forms.DateField(
        label=_('Semester End:'),
        widget=forms.widgets.DateInput(
            attrs={'class': 'datepicker1', 'placeholder': _("mm/dd/yyyy")}))

    def clean(self):
        try:
            cleaned_data = super(SettingsForm, self).clean()
            start_semester = cleaned_data.get('start_semester')
            end_semester = cleaned_data.get('end_semester')
            if not (start_semester <= end_semester):
                msg = _('Semester start must be before the end of it.')
                self.add_error('start_semester', msg)
                self.add_error('end_semester', msg)
                raise forms.ValidationError(msg)
        except Exception as e:
            msg = _('Inputs are invalid')
            raise forms.ValidationError(msg)

    def save(self, force_insert=False, force_update=False, commit=True):
        settings = Settings()
        settings.start_semester = self.cleaned_data.get("start_semester")
        settings.end_semester = self.cleaned_data.get("end_semester")
        settings.save()
        return settings

    class Meta:
        model = Settings
        fields = ['start_semester', 'end_semester']
