from django.shortcuts import render
from .forms import UserForm
from .models import UserProfile
def new_user(request):
  if request.method == "POST":
    form = UserForm(request)
    if not(form.is_valid()):
      return render(request, 'booking/newUser.html', {'form_user':form})
    else:
      user_profile = form.save()
  else:
    form = UserForm()
    return render(request, 'booking/newUser.html', {'form_user':form})


