from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Work

# Create your views here.
def index(request):
    return render(request, 'commute/index.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('commute:login')
    template_name = 'registration/register.html'


class Calendar(generic.MonthArchiveView):
    model = Work
    date_field = 'start'