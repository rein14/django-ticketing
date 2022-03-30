from django import forms
from .models import Ticket, Comment, File
from bootstrap_datepicker_plus import DatePickerInput
from cms.forms import BootstrapHelperForm
from django_select2 import forms as s2forms


class TicketWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
         "last_name__icontains",
        "first_name__icontains",
    ]

class TicketForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'date_sent', 'ticket_choices', 'description',
                  'assigned_to', 'sent_by')
        widgets = {
            'date_sent': DatePickerInput(format='%Y-%m-%d'),
            'assigned_to' : TicketWidget,
        }


class TicketUpdateForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'date_sent', 'ticket_choices', 'description',
                  'assigned_to', 'waiting_for', 'sent_by')
        widgets = {
            'date_sent': DatePickerInput(format='%Y-%m-%d'),
            'assigned_to' : TicketWidget,
        }


class CommentForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('ticket', 'comment')
        widgets = {
            'ticket': forms.HiddenInput(),
            #'user': forms.HiddenInput(),
        }


class FileForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', )
