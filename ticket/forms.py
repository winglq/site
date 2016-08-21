from models import Ticket
from django import forms


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('ticket',)
    def clean_ticket(self):
        t = self.cleaned_data['ticket']
        try:
            t_instance = Ticket.objects.get(ticket=str(t))
        except:
            raise forms.ValidationError("Ticket does not exist")
        if t_instance.ip != '0.0.0.0':
            raise forms.ValidationError("Ticket already in use")
        return t
