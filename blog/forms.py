from django import forms
from .models import Email

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email']
        labels = {'email':''}
        widgets = {
            'email': forms.EmailInput(attrs={'id': 'semail', 'class': 'form-control me-md-1 semail', 'placeholder': 'Enter email'})
        }