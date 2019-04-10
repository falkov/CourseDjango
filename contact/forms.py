from django import forms

from .models import ContactFormModel


class ContactForm(forms.ModelForm):
    """Форма обратной связи"""
    class Meta:
        model = ContactFormModel
        fields = ['full_name', 'email', 'text']
