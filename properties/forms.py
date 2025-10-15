from django import forms
from .models import ContactMessage, NewsletterSubscriber, Newsletter, ListingImage, ConstructionImage, ReferenceImage


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


# Multiple file upload widgets and forms

class MultipleFileInput(forms.ClearableFileInput):
    """
    Custom widget for uploading multiple files at once
    """
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """
    Custom field for handling multiple file uploads
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ListingImageUploadForm(forms.Form):
    """
    Form for uploading multiple listing images at once
    """
    images = MultipleFileField(
        label='İlan Resimleri',
        help_text='Birden fazla resim seçebilirsiniz (Ctrl/Cmd tuşuna basılı tutarak)',
        required=False
    )


class ConstructionImageUploadForm(forms.Form):
    """
    Form for uploading multiple construction images at once
    """
    images = MultipleFileField(
        label='İnşaat Resimleri',
        help_text='Birden fazla resim seçebilirsiniz (Ctrl/Cmd tuşuna basılı tutarak)',
        required=False
    )


class ReferenceImageUploadForm(forms.Form):
    """
    Form for uploading multiple reference images at once
    """
    images = MultipleFileField(
        label='Referans Resimleri',
        help_text='Birden fazla resim seçebilirsiniz (Ctrl/Cmd tuşuna basılı tutarak)',
        required=False
    )
