from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.base import View

from CourseDjango import settings
from .models import ContactFormModel
from .forms import ContactForm


class ContactFormView(View):
    """Обработка контактной формы"""
    def get(self, request):
        return render(request, 'contact/contact-form.html', {'form': ContactForm()})

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, settings.MY_INFO, 'Ваше сообщение отправлено!')
        else:
            messages.add_message(request, settings.MY_INFO, 'Ошибка!')

        return redirect('contact')
