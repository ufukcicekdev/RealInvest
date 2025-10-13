from django import forms
from django.forms.widgets import TextInput
from .models import CustomSection


class ColorPickerWidget(TextInput):
    """
    A widget that provides a color picker input for hex color values
    """
    input_type = 'color'
    
    def __init__(self, attrs=None):
        default_attrs = {'style': 'width: 100px; height: 40px;'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def format_value(self, value):
        """
        Ensure the value is in the correct hex format
        """
        if value and not value.startswith('#'):
            return f'#{value}'
        return value


# Custom form for CustomSection to apply color picker only to specific fields
class CustomSectionForm(forms.ModelForm):
    """
    Custom form for CustomSection model with color picker widgets
    """
    class Meta:
        model = CustomSection
        fields = '__all__'
        widgets = {
            'background_color': ColorPickerWidget(),
            'text_color': ColorPickerWidget(),
        }