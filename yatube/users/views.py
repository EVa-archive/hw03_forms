from django.views.generic import CreateView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class PasswordChange(PasswordChangeView):
    success_url = 'done/'
    template_name = 'user/password_change_done.html'
