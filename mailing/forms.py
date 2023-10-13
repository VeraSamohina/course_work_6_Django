from django import forms

from mailing.models import Mailing, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ('slug',)

    # widgets = {
    #     'title': forms.TextInput(attrs={'class': 'form-control'}),
    #     'period': forms.TextInput(attrs={'class': 'form-control'}),
    #     'start_time': forms.TextInput(attrs={'class': 'form-control'}),
    # }


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('slug',)
