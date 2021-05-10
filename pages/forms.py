from django.contrib.gis import forms

class NumberOfRecordForm(forms.Form):
    n_rows = forms.IntegerField(label='Number of Records to Upload',
        widget=forms.NumberInput(
            attrs={'class':'form-control mr-sm-1'}
            ))