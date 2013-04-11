# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader

from tours.models import TourReq

def index(request):
    latest_req_list = TourReq.objects.order_by('-req_time')[:5]
    template = loader.get_template('tours/index.html')
    context = Context({
            'latest_req_list': latest_req_list,
            })

    return HttpResponse(template.render(context))

def newreq(request):
    return HttpResponse("You're making a new request!")

def notifyreq(request):
    return HttpResponse("You're checking and emailing out a notice")

def claimreq(request):
    return HttpResponse("You're claiming a response")
