from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import generic
from .models import Work
from .forms import CheckForm
from datetime import datetime
from django.utils.safestring import mark_safe
from .utils import Calendar

# Create your views here.


def index(request):
    return render(request, 'commute/index.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('commute:login')
    template_name = 'registration/register.html'


def myWork_detail(request, date):
    work = Work.objects.filter(start__date=date, name=request.user)
    return render(request, 'commute/blank.html', {'work': work, 'date': date})


def addWork(request, date):
    todays = Work.objects.filter(name = request.user, start__date = date)
    if todays is not None:
        pass #처리해야합니다 이부분
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            work = Work(
                name=request.user, start=form.cleaned_data['start'], end=form.cleaned_data['end'])
            work.save()
            return redirect('commute:myWork')
    else:
        form = CheckForm(
            initial={'name': request.user, 'start': date, 'end': date})
    return render(request, 'commute/blank2.html', {'form': form})


class CalendarView(generic.ListView):
    model = Work
    template_name = 'commute/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))
        work = Work.objects.filter(name=self.request.user)
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True, work=work)
        context['calendar'] = mark_safe(html_cal)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
