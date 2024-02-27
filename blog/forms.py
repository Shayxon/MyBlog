from django import forms
from .models import Email, Comment

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email']
        labels = {'email':''}
        widgets = {
            'email': forms.EmailInput(attrs={'id': 'semail', 'class': 'form-control me-md-1 semail', 'placeholder': 'Enter email'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']