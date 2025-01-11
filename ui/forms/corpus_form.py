from django import forms
from ui.models import Corpus

class CorpusForm(forms.ModelForm):
    class Meta:
        model = Corpus
        fields = ['name', 'type', 'path', 'username']
