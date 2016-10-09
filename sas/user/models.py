from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.exceptions import ValidationError

CATEGORY = (('', '----'), ('1', _('Student')),
            ('2', _('Teaching Staff')), ('3', _('Employees')))


class UserProfile(models.Model):
    registration_number = models.CharField(max_length=20, unique=True, error_messages={'unique':_('Registration Number already used.')})
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_user")
    category = models.CharField(choices=CATEGORY, max_length=20)

    def name(self, name):
        if not hasattr(self, 'user'):
 
            self.user = User()
        names = name.split()
        self.user.first_name = names.pop(0)
        self.user.last_name = str.join(" ", names)

    def full_name(self):
        name = str.join(" ", [self.user.first_name, self.user.last_name])
        return name

    def clean_fields(self, exclude=None):
        validation = Validation()

        # Registration Number validation
        registration_number = self.registration_number

        if (len(registration_number) != 9):
            raise ValidationError({'registration_number': [_('Registration number must have 9 digits.'), ]})

        if validation.hasLetters(registration_number):
            raise ValidationError({'registration_number': [_('Registration number cannot contain letters.'), ]})

        if validation.hasSpecialCharacters(registration_number):
            raise ValidationError({'registration_number': [_('Registration number cannot contain special characters.'), ]})

    def save(self, *args, **kwargs):
        self.user.save()
        self.user_id = self.user.pk
        super(UserProfile, self).save(*args, **kwargs)


class Validation():

    def hasNumbers(self, string):
        if (string is not None):
            if any(char.isdigit() for char in string):
                return True

            return False

        else:
            return False

    def hasLetters(self, number):
        if (number is not None):
            if any(char.isalpha() for char in number):
                return True

            return False

        else:
            return False

    def hasSpecialCharacters(self, string):
        if (string is not None):
            for character in '@#$%^&+=/\{[]()}-_+=*!§|':
                if character in string:
                    return True

        return False
