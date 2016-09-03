from django.db import models
from django.contrib.auth.models import User

CATEGORY = (('1','Aluno'),('2','Docente'),('3','Servidor'))


class UserProfile(models.Model):
  registration_number = models.CharField(max_length = 20)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  category = models.CharField(choices = CATEGORY,max_length = 20)


