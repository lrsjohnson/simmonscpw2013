# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from events.models import Event
from django.utils import timezone

from django.core.mail import send_mail

from datetime import datetime, timedelta


def index(request):
    # now event
    now_events = Event.objects.filter(start_time__lt =timezone.now()).filter(end_time__gt = timezone.now())
    if len(now_events) > 0:
        now_event = now_events[0]
    else:
        now_event = None
    
    # next event
    next_events = Event.objects.filter(start_time__gt=timezone.now())
    if len(next_events) > 0:
        next_event = next_events[0]
    else:
        next_event = None
    
    context = {
        'now_event': now_event,
        'next_event': next_event,
        'next_events': next_events,
    }

    return render(request, 'events/index.html', context)


def info(request):
    all_events = Event.objects.order_by('start_time')
    context = {
        'all_events': all_events,
    }

    return render(request, 'events/info.html', context)
