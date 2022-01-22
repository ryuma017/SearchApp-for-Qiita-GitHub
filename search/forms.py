import json

from django import forms

def get_info():
    with open('search/json/info.json', 'r') as f:
        info = json.load(f)
    return info


class SearchForm(forms.Form):
    names = get_info().keys()
    choices = ((value, name) for value, name in zip(names, names))
    q = forms.CharField(label='タイトル', max_length=200, required=True)
    name = forms.ChoiceField(label='どのサービスを検索するか', required=True, choices=choices, widget=forms.RadioSelect(
        attrs={
            'class': 'btn-check',
            'auto-complete': 'off'
        }
    ))
