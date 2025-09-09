from django import forms
from .models import Ticket
from django.contrib.auth.models import User

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['agent_id', 'status', 'category', 'description', 'location']
        widgets = {
            'agent_id': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }