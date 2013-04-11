# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from tours.models import TourReq
from django.utils import timezone

from django.core.mail import send_mail

from datetime import datetime, timedelta

def index(request):
    unclaimed_reqs = TourReq.objects.filter(claimed=False).order_by('-req_time')
    claimed_reqs = TourReq.objects.filter(claimed=True).order_by('-req_time')
    context = {
        'unclaimed': unclaimed_reqs,
        'claimed': claimed_reqs,
    }

    return render(request, 'tours/index.html', context)

def newreq(request):
    unclaimed_reqs = TourReq.objects.filter(claimed=False).order_by('-req_time')
    if len(unclaimed_reqs) > 0 and unclaimed_reqs[0].req_time - timezone.now() < timedelta(minutes=1):
        return HttpResponse("Must wait at least 1 minute between requests!")
            
    req_time = timezone.now()
    tr = TourReq(req_time=req_time,claim_time=None)
    tr.save()

    subject = "[Sim-CPW-Tours] - "+req_time.strftime("%I:%m%p") +" tour requested!"
    msg = "A tour was requested at "+req_time.strftime("%I:%m%p") +". If you're free, go to desk and press the black button on the back of the 'easy button' to claim it."
    from_email = "simmons-tech@mit.edu"
    to_emails = ["larsj@mit.edu"]
    send_mail(subject, msg, from_email, to_emails, fail_silently=False)
    return HttpResponse("email sent: "+subject)


    return HttpResponse("You created a new request!")

def notifyreq(request):
    unclaimed_reqs = TourReq.objects.filter(claimed=False).order_by('req_time')
    num_unclaimed = len(unclaimed_reqs)
    if num_unclaimed > 0:
        req_time = unclaimed_reqs[0].req_time
        req_delay = (timezone.now() - req_time)
        subject = "[Sim-CPW-Tours] - "+req_time.strftime("%I:%m%p") +" tour request unclaimed for "+str(req_delay.seconds / 60)+" minutes!"
        msg = "[Sim-CPW-Tours] - "+req_time.strftime("%I:%m%p") +" tour request unclaimed for "+str(req_delay.seconds / 60)+" minutes!  If you're free, go to desk and press the black button on the back of the 'easy button' to claim it." 
        from_email = "simmons-tech@mit.edu"
        to_emails = ["larsj@mit.edu"]
        send_mail(subject, msg, from_email, to_emails, fail_silently=False)
        return HttpResponse("email sent: "+subject)
    else:
        return HttpResponse("None")

def claimreq(request):
    unclaimed_reqs = TourReq.objects.filter(claimed=False).order_by('-req_time')
    if len(unclaimed_reqs) == 0:
        return HttpResponse("Nothing to claim")

    req_time = unclaimed_reqs[0].req_time
    for req in unclaimed_reqs:
        req.claimed = True
        req.claimed_time = timezone.now()
        req.save()
    subject = "[Sim-CPW-Tours] - "+req_time.strftime("%I:%m%p") +" tour request claimed!"
    msg = "Thanks for playing! The "+req_time.strftime("%I:%m%p") +" tour request has been claimed."
    from_email = "simmons-tech@mit.edu"
    to_emails = ["larsj@mit.edu"]
    send_mail(subject, msg, from_email, to_emails, fail_silently=False)
    return HttpResponse("email sent: "+subject)
