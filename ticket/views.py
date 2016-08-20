from django.shortcuts import render, redirect, get_object_or_404
from models import Ticket
import uuid
from django.contrib.auth.decorators import login_required
from mysite.views import ListView
from mysite.views import FormView
from forms import TicketForm

# Create your views here.

@login_required
def generate(request):
    uid = uuid.uuid4()
    t = Ticket.objects.create(ticket=uid, ip="0.0.0.0",
                              expired=False)
    t.save()
    return render(request, 'ticket/ticket_detail.html', {'ticket': t})

class TicketListAvailableView(ListView):
    model = Ticket

    def get_queryset(self):
        return Ticket.objects.filter(ip="0.0.0.0")

class TicketListView(ListView):
    model = Ticket

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def check(request, ticket=None, next=None):
    if request.method == "POST":
        ticket = request.POST['ticket']
    if ticket:
        t = get_object_or_404(Ticket, ticket=ticket)
        if t.ip == '0.0.0.0':
            t.ip = get_client_ip(request)
            t.save()
            request.session['ticket'] = str(t.ticket)
            request.session.set_expiry(2*3600)
            if next:
                return redirect(next)
            else:
                return redirect('/nineone/list')
        else:
            raise Exception("%s is already in use", str(t.ticket))
    form = TicketForm()
    return render(request, "ticket/ticket_check.html",
                  {"form": form})
