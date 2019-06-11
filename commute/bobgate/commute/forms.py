from django import forms
from .models import Work


class CheckForm(forms.Form):
    name = forms.CharField()
    start = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
    end = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
