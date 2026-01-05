from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from contact.models import Contact
from django import forms
from django.core.exceptions import ValidationError


# Create your views here.

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name', 'phone'
        )

    def clean(self) -> dict[str, Any]:
        cleaned_data = self.cleaned_data
        self.add_error(
            'first_name',
            ValidationError(
                'Mensagem de Erro',
                code='invalid'
            )
        )
        return super().clean()


def create(request):
    context = {
        'form': ContactForm()
    }

    if request.method == 'POST':
        context = {
            'form': ContactForm(request.POST)
        }

    return render(request, 'contact/create.html', context)