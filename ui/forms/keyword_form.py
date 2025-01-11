from django import forms
from ui.models import Keyword

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ['word', 'short_desc', 'long_desc']
