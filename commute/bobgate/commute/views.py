from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import generic
from .models import Work, Board
from .forms import CheckForm, BoardForm
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
    todays = Work.objects.filter(name=request.user, start__date=date)
    if todays:
        return redirect('commute:editWork', date)
    else:
        if request.method == 'POST':
            form = CheckForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['start'] > form.cleaned_data['end'] or form.cleaned_data['start'].day != form.cleaned_data['end'].day:
                    if form.cleaned_data['start'] > form.cleaned_data['end']:
                        messages = '근무 시작 시간이 종료 시간보다 나중입니다.'
                    else:
                        messages = '근무 시작일과 종료일이 다릅니다.'
                    return render(request, 'commute/blank2.html', {'form': form, 'messages': messages})
                else:
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


def editWork(request, date):
    today = Work.objects.filter(name=request.user, start__date=date).first()
    message = '이미 오늘의 근무가 등록되어있습니다. 수정하세요.'
    if request.method == 'POST':
        form = CheckForm(request.POST)
        print("포스트")
        if form.is_valid():
            print("폼 괜찮")
            if form.cleaned_data['start'] > form.cleaned_data['end'] or form.cleaned_data['start'].day != form.cleaned_data['end'].day:
                print("날짜 이상")
                if form.cleaned_data['start'] > form.cleaned_data['end']:
                    messages = '근무 시작 시간이 종료 시간보다 나중입니다.'
                else:
                    messages = '근무 시작일과 종료일이 다릅니다.'
                return render(request, 'commute/blank2.html', {'form': form, 'messages': messages})
            else:
                today.delete()
                work = Work(
                 name=request.user, start=form.cleaned_data['start'], end=form.cleaned_data['end'])
                work.save()
                return redirect('commute:myWork')
    else:
        form = CheckForm(
            initial={'name': request.user, 'start': today.start, 'end': today.end})
    return render(request, 'commute/blank2.html', {'form': form, 'message': message})


class BoardLV(generic.ListView):
    model = Board
    paginate_by = 6
    ordering = ['-idx']


class BoardDV(generic.DetailView):
    model = Board


def addBoard(request):
    if request.method == 'POST':
        form = BoardForm(request.POST, request.FILES)
        board = Board()
        if form.is_valid():
            board.name = request.user
            board.title = form.cleaned_data['title']
            board.image = form.cleaned_data['image']
            board.save()
            return redirect('commute:board')
    else:
        form = BoardForm()
    return render(request, 'commute/board_add.html', {'form':form})