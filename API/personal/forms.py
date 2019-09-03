from django import forms

class ReportForm(forms.Form):
    date = forms.DateField()
    
class TextForm(forms.Form):
    your_text = forms.CharField(label='Your test')