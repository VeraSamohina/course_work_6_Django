from django import forms

from mailing.models import Mailing, Message, Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(owner=owner)
        self.fields['message'].queryset = Message.objects.filter(owner=owner)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    class Meta:
        model = Mailing
        exclude = ('slug', 'owner', 'is_active')


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('slug', 'owner')


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('slug', 'owner')
