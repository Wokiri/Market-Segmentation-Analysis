from django import forms

from .models import Excel

class ExcellModelForm(forms.ModelForm):
    class Meta:
        model = Excel
        fields = ('file',)