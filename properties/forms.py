from django import forms
from .models import ContactMessage, NewsletterSubscriber, Newsletter


class ContactForm(forms.Form):
    """
    Contact form for user inquiries
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adınız',
            'required': True
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-posta Adresiniz',
            'required': True
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telefon Numaranız (Opsiyonel)'
        })
    )
    
    subject = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Konu (Opsiyonel)'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Mesajınız',
            'rows': 5,
            'required': True
        })
    )


class NewsletterSubscribeForm(forms.ModelForm):
    """
    Newsletter subscription form for popup
    """
    dont_show_again = forms.BooleanField(
        required=False,
        label='Bir daha gösterme',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adınız Soyadınız',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-posta Adresiniz',
                'required': True
            }),
        }
        labels = {
            'name': 'Ad Soyad',
            'email': 'E-posta',
        }


class NewsletterForm(forms.ModelForm):
    """
    Admin form for creating newsletters
    """
    class Meta:
        model = Newsletter
        fields = ['title', 'subject', 'content', 'scheduled_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
