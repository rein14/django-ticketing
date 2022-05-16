from django import forms
from .models import Folder, Memo, Comment, File
# from bootstrap_datepicker_plus.widgets import DatePickerInput
from cms.forms import BootstrapHelperForm
from django.forms import inlineformset_factory
from django_select2 import forms as s2forms
# from .widgets import XDSoftDateTimePickerInput, BootstrapDateTimePickerInput, FengyuanChenDatePickerInput


class MemoWidget(s2forms.ModelSelect2MultipleWidget):
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


class MemoForm(BootstrapHelperForm, forms.ModelForm):

    class Meta:
        model = Memo
        fields = ('title', 'date_sent', 'description',
                  'assigned_to', 'sent_by', 'folder',)

        widgets = {
            # 'assigned_to': MemoWidget,
            'folder': FolderWidget,
            # 'date_sent': DatePickerInput(format='%Y-%m-%d'),

        }


class MemoFolderForm(BootstrapHelperForm, forms.ModelForm):
    # date_sent = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=BootstrapDateTimePickerInput())

    class Meta:
        model = Memo
        fields = ('title', 'date_sent', 'description',
                  'assigned_to', 'sent_by',)
        widgets = {
            # 'assigned_to': MemoWidget,
            # 'date_sent': forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M']),
        }


class MemoDetailForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = Memo
        fields = ('title', 'date_sent', 'assigned_to',
                  'description',  'sent_by',)


class MemoUpdateForm(BootstrapHelperForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Memo
        fields = ('title', 'date_sent', 'description', 'sent_by')
        widgets = {
            # 'date_sent': DatePickerInput(format='%Y-%m-%d'),
            # 'assigned_to': MemoWidget,
        }


class MemoStatusUpdateForm(BootstrapHelperForm, forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(MemoStatusUpdateForm, self).__init__(*args, **kwargs)
    #    self.fields['memo'].required = False
        # self.fields['title'].widget.attrs['disabled'] = "disabled"
    title = forms.CharField(disabled=True)
    # def clean_buyer(self):
    #     instance = getattr(self, 'instance', None)
    #     if instance:
    #         return instance.buyer
    #     else:
    #         return self.cleaned_data.get('buyer', None)

    class Meta:
        model = Memo
        fields = ('title', 'memo_choices', 'assigned_to', 'waiting_for',)
        widgets = {

            # 'assigned_to': MemoWidget,
        }


class CommentForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('memo', 'comment')
        widgets = {
            'memo': forms.HiddenInput(),
            # 'user': forms.HiddenInput(),
        }


class FileForm(BootstrapHelperForm, forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', )


# MemoMetaInlineFormset = inlineformset_factory(
#     Memo,
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

MemoFileFormSet = inlineformset_factory(
    Memo, File, form=FileForm, extra=1, can_delete=False)
