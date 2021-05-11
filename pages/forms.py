from django.contrib.gis import forms

class NumberOfRecordForm(forms.Form):
    n_rows = forms.IntegerField(
        label='Number of Records to Upload',
        max_value =50000,
        widget=forms.NumberInput(
            attrs={'class':'form-control mr-sm-1',}
            ))



class SearchWardForm(forms.Form):
    ward_name = forms.CharField(
        label='Search Ward',
        max_length=25,
        widget=forms.TextInput(
            attrs={
                'class':'form-control me-2',
                'type':'search',
                'placeholder':'Search Ward',
                'aria-label':'Search',
            }
        ))