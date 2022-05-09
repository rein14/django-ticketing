from django import forms
from .models import Folder, Ticket, Comment, File
from bootstrap_datepicker_plus import DatePickerInput
from cms.forms import BootstrapHelperForm
from django.forms import inlineformset_factory
from django_select2 import forms as s2forms


class TicketWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "last_name__icontains",
        "first_name__icontains",
        "roles__icontains",
    ]

class FolderWidget(s2forms.Select2Widget):
    search_fields = [

        "title__icontains",
    ]


class FolderForm(BootstrapHelperForm, forms.ModelForm):

    class Meta:
        model = Folder
        fields = ('title',)
       


class TicketForm(BootstrapHelperForm, forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('title', 'date_sent', 'description',
                  'assigned_to', 'sent_by','folder',)
        widgets = {
           #x 'assigned_to': TicketWidget,
            'folder': FolderWidget,
        }

class TicketFolderForm(BootstrapHelperForm, forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('title', 'date_sent', 'description',
                  'assigned_to', 'sent_by',)
        widgets = {
           # 'assigned_to': TicketWidget,
         }



class TicketDetailForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'date_sent','assigned_to',  'description',  'sent_by',)

 


class TicketUpdateForm(BootstrapHelperForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    class Meta:
        model = Ticket
        fields = ('title', 'date_sent', 'description', 'sent_by')
        widgets = {
            'date_sent': DatePickerInput(format='%Y-%m-%d'),
            #'assigned_to': TicketWidget,
        }


class TicketStatusUpdateForm(BootstrapHelperForm, forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(TicketStatusUpdateForm, self).__init__(*args, **kwargs)
    #    self.fields['ticket'].required = False
        # self.fields['title'].widget.attrs['disabled'] = "disabled"
    title = forms.CharField(disabled=True)
    # def clean_buyer(self):
    #     instance = getattr(self, 'instance', None)
    #     if instance:
    #         return instance.buyer
    #     else:
    #         return self.cleaned_data.get('buyer', None)

    class Meta:
        model = Ticket
        fields = ('title', 'ticket_choices', 'assigned_to', 'waiting_for',)
        widgets = {
        
            #'assigned_to': TicketWidget,
        }


class CommentForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('ticket', 'comment')
        widgets = {
            'ticket': forms.HiddenInput(),
            # 'user': forms.HiddenInput(),
        }


class FileForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', )


# TicketMetaInlineFormset = inlineformset_factory(
#     Ticket,
#     File,
#     form=FileForm,
#     extra=1,
#     # max_num=5,
#     # fk_name=None,
#     # fields=None, exclude=None, can_order=False,
#     # can_delete=True, max_num=None, formfield_callback=None,
#     # widgets=None, validate_max=False, localized_fields=None,
#     # labels=None, help_texts=None, error_messages=None,
#     # min_num=None, validate_min=False, field_classes=None
# )

TicketFileFormSet = inlineformset_factory(Ticket, File, form=FileForm, extra=1, can_delete=False)
