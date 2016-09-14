from django.db import models
from django.contrib.auth.models import User

CATEGORY = (('1','Aluno'),('2','Docente'),('3','Servidor'))


class UserProfile(models.Model):
	registration_number = models.CharField(max_length = 20)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_user")
	category = models.CharField(choices = CATEGORY,max_length = 20)

	def name(self,name):
		if self.user is None:
			self.user = User()
		names = name.split()
		self.user.first_name = names.pop(0)
		self.user.last_name = str.join(" ",names)

	def full_name(self):
		name = str.join(" ",[self.user.first_name,self.user.last_name])
		return name

	def save(self,*args,**kwargs):
		self.user.save()
		self.user_id = self.user.pk
		super(UserProfile,self).save(*args,**kwargs)
