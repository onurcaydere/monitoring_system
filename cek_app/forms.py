from django import forms

class CommandForm(forms.Form):
    your_name = forms.CharField(label='command', max_length=100)