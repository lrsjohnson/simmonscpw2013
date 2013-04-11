# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from tours.models import TourReq
from django.utils import timezone

from django.core.mail import send_mail

def index(request):
    unclaimed_reqs = TourReq.objects.filter(claimed=False).order_by('-req_time')
    claimed_reqs = TourReq.objects.filter(claimed=True).order_by('-req_time')
    context = {
        'unclaimed': unclaimed_reqs,
        'claimed': claimed_reqs,
    }

    return render(request, 'tours/index.html', context)

def newreq(request):
    tr = TourReq(req_time=timezone.now())
    tr.save()
    return HttpResponse("You created a new request!")

def notifyreq(request):
    unclaimed_reqs = TourReq.objects.filter(claimed=False).order_by('req_time')
    num_unclaimed = len(unclaimed_reqs)
    if num_unclaimed > 0:
        oldest_time = unclaimed_reqs[0].req_time

        subject = "Simmons CPW Tour Notification - "+str(num_unclaimed)+ " requests waiting!"
        msg = "There are "+str(num_unclaimed)+ " requests for tours waiting at desk, the oldest being from "+oldest_time.strftime("%I:$m:%s")
        from_email = "simmons-tech@mit.edu"
        to_emails = ["larsj@mit.edu"]
        send_mail(subject, msg, from_email, to_emails, fail_silently=False)
    return HttpResponse("You're checking and emailing out a notice")

def claimreq(request):
    unclaimed_reqs = TourReq.objects.filter(claimed=False).order_by('-req_time')
    for req in unclaimed_reqs:
        req.claimed = True
        req.save()
    return HttpResponse("You're claiming a response")
