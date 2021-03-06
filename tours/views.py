# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from django.utils import timezone

from django.core.mail import send_mail

from datetime import datetime, timedelta

from tours.models import TourReq

from events.models import Event

to_emails = [] #"simmons-cpw-tours-automated@mit.edu"]

def index(request):
    # events happening now
    events_happening_now = Event.objects.filter(start_time__lt = timezone.now()).filter(end_time__gt = timezone.now()).order_by('-start_time')
    
    # upcoming events
    upcoming_events = Event.objects.filter(start_time__gt=timezone.now()).order_by('start_time')
    if len(upcoming_events) > 3:
        upcoming_events = upcoming_events[:3]

    if len(upcoming_events) > 0:
        next_event = upcoming_events[0]
    else:
        next_event = None

    unclaimed_reqs = TourReq.objects.filter(claimed=False).order_by('-req_time')
    claimed_reqs = TourReq.objects.filter(claimed=True).order_by('-claim_time')

    # last request
    if len(unclaimed_reqs) == 0:
        last_request = None
    else:
        last_request = unclaimed_reqs[0].req_time

    # last tour
    if len(claimed_reqs) == 0:
        last_tour = None
    elif timezone.now() - claimed_reqs[0].claim_time > timedelta(minutes=60):
        last_tour = None
    else:
        last_tour = claimed_reqs[0].claim_time
        
    context = {
        'last_tour': last_tour,
        'last_request': last_request,
        'events_happening_now': events_happening_now,
        'next_event': next_event,
        'upcoming_events': upcoming_events,
        'events_beyond_next_event': upcoming_events[1:],
        'message': events_happening_now,
    }
    return render(request, 'tours/monitor-schedule.html', context)

def info(request):
    unclaimed_reqs = TourReq.objects.filter(claimed=False).order_by('-req_time')
    claimed_reqs = TourReq.objects.filter(claimed=True).order_by('-req_time')
    context = {
        'unclaimed': unclaimed_reqs,
        'claimed': claimed_reqs,
    }

    return render(request, 'tours/info.html', context)

def newreq(request):
    unclaimed_reqs = TourReq.objects.filter(claimed=False).order_by('-req_time')
    if len(unclaimed_reqs) > 0 and  timezone.now() - unclaimed_reqs[0].req_time < timedelta(minutes=1):
        return HttpResponse("Must wait at least 1 minute between requests!")
            
    req_time = timezone.now()
    tr = TourReq(req_time=req_time,claim_time=None)
    tr.save()

    subject = "[CPW Tours] Simmons CPW Tours"
    msg = "A tour was requested at "+timezone.localtime(req_time).strftime("%a %I:%M%p") +". If you're free, go speak to the desk worker to claim it (they will push 'w' on the computer keyboard that's there)"
    from_email = "simmons-tech@mit.edu"
#    to_emails = ["larsj@mit.edu"]
    send_mail(subject, msg, from_email, to_emails, fail_silently=False)
    return HttpResponse("email sent: "+subject)

def notifyreq(request):
    unclaimed_reqs = TourReq.objects.filter(claimed=False).order_by('req_time')
    num_unclaimed = len(unclaimed_reqs)
    if num_unclaimed > 0 and timezone.now() - unclaimed_reqs[0].req_time > timedelta(minutes=5):
        req_time = unclaimed_reqs[0].req_time
        req_delay = (timezone.now() - req_time)
        subject = "[CPW Tours] Simmons CPW Tours"
        msg = timezone.localtime(req_time).strftime("%a %I:%M%p") +" tour request unclaimed for "+str(req_delay.seconds / 60)+" minutes!  If you're free, go and speak to the desk worker to claim it (they will push 'w' on the computer keyboard that's there)"
        from_email = "simmons-tech@mit.edu"
 #       to_emails = ["larsj@mit.edu"]
        send_mail(subject, msg, from_email, to_emails, fail_silently=False)
        context = {'msg':subject}
        return render(request, 'tours/notify.html', context)
    else:
        context = {}
        return render(request, 'tours/notify.html', context)

def claimreq(request):
    unclaimed_reqs = TourReq.objects.filter(claimed=False).order_by('-req_time')
    if len(unclaimed_reqs) == 0:
        return HttpResponse("Nothing to claim")

    req_time = unclaimed_reqs[0].req_time
    for req in unclaimed_reqs:
        req.claimed = True
        req.claim_time = timezone.now()
        req.save()
    subject = "[CPW Tours] Simmons CPW Tours"
    msg = "The "+timezone.localtime(req_time).strftime("%a %I:%M%p") +" tour request has been claimed."
    from_email = "simmons-tech@mit.edu"
#    to_emails = ["larsj@mit.edu"]
    send_mail(subject, msg, from_email, to_emails, fail_silently=False)
    return HttpResponse("email sent: "+subject)
