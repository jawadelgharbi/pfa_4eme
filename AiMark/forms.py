from django.contrib.auth.models import User
from django import forms


class MyMarkForm(forms.Form):
    id = forms.IntegerField(label='Id', required=False, widget=forms.HiddenInput)
    utilisateur = forms.ModelChoiceField(queryset=User.objects.all(), required=False,
                                  widget=forms.HiddenInput)
    nom = forms.CharField(label='Title', max_length=100, required=True
                            , widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label='Image', max_length=100, required=False,
                             widget=forms.FileInput(attrs={'class': 'form-control'}), )
    desctiption = forms.CharField(label='Description', max_length=500, required=True
                                  , widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    gravit = forms.IntegerField(label='Gravity', required=True
                                 , widget=forms.NumberInput(attrs={'class': 'form-range', 'type': 'range'
            , 'min': '1', 'max': '10'}))

    date = forms.DateField(label='Created_at', required=False)
