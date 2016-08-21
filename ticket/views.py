from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from models import Ticket
import uuid
from django.contrib.auth.decorators import login_required
from mysite.views import ListView, TemplateView
from mysite.views import FormView
from forms import TicketForm


class GenerateTicketView(TemplateView):
    template_name = 'ticket/ticket_detail.html'
    def get(self, request, *args, **kwargs):
        uid = uuid.uuid4()
        t = Ticket.objects.create(ticket=uid, ip="0.0.0.0")
        t.save()
        context = super(GenerateTicketView, self). \
            get_context_data(**kwargs)
        context['ticket'] = t
        return self.render_to_response(context)

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


class CheckTicketView(FormView):
    template_name = "ticket/ticket_check.html"
    form_class = TicketForm
    def _show_form(self, request):
        t_form = TicketForm(request.POST)
        context = super(CheckTicketView, self). \
             get_context_data(**kwargs)
        context['form'] = t_form
        if not t_form.is_valid():
            return self.render_to_response(context)

    def _use_ticket(self, request, ticket, next=None):
        t = get_object_or_404(Ticket, ticket=ticket)
        if t.ip != '0.0.0.0':
            e = Http404('ticket in use')
            e.err_msg = "<h1>Ticket %s is already been used</h1>" % \
                t.ticket
            raise e
        t.ip = get_client_ip(request)
        t.save()
        request.session['ticket'] = str(t.ticket)
        request.session.set_expiry(2*3600)
        return redirect(next if next else '/nineone/list')

    def post(self, request, *args, **kwargs):
        t_form = TicketForm(request.POST)
        if not t_form.is_valid():
            context = super(CheckTicketView, self). \
                get_context_data(**kwargs)
            context['form'] = t_form
            return self.render_to_response(context)
        ticket = t_form.cleaned_data['ticket']
        next = kwargs.get('next')
        return self._use_ticket(request, ticket, next)

    def get(self, request, ticket=None, **kwargs):
        if ticket:
            return self._use_ticket(request, ticket)
        else:
            return super(CheckTicketView, self).get(request, ticket, **kwargs)
