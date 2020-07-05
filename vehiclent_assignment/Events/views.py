from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from .forms import CreateUserForm,EventForm
from django.contrib.auth import authenticate,login as django_login,logout as django_logout
from django.contrib import messages
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views import generic
from django.utils.safestring import mark_safe
from .models import Event
from .utils import Calendar
import calendar
from django.urls import reverse


def home(request):
    return render(request,'home.html')


def register(request):
    form = CreateUserForm()
    context = {'form': form}
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return redirect('register')
    else:
        return render(request, 'register.html', context)

def login(request):
    if request.method == "POST":
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')
        user = authenticate(username = username1, password =password1)
        if user is not None:
            django_login(request,user)
            messages.success(request,'Thank You for Login')
            return redirect('home')
        else:
            messages.warning(request,'Username or Password is Wrong')
    return render(request,'login.html')

def logout(request):
    django_logout(request)
    return redirect('login')

@login_required(login_url='login')
def invitations(request):
    invite=Event.objects.filter(User=request.user)
    context={'invite':invite}
    return render(request,'invitations.html',context)

@login_required(login_url='login')
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'event.html', {'form': form})


class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


