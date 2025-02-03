from django import forms
from ui.models import Corpus, Document, Chunk, Keyword, Score

#pylint: disable=R0903
class BaseForm(forms.ModelForm):
    class Meta:
        model = None

    view_fields = ['action',  'type', 'child_type', 'display_name', 'child_name', 'display_attributes']
    value_dict = {}

    def init_view_fields(self, value_dict :dict):
        for field in self.view_fields:
            if field in value_dict.keys():
                self.fields[field] = forms.CharField(initial=value_dict[field], required=True)
                self.fields[field].widget.attrs['readonly'] = True
                self.fields[field].widget.attrs['disabled'] = True
                self.fields[field].widget.attrs['style'] = 'background-color: #f9f9f9'
                self.fields[field].widget.attrs['class'] = 'form-control-plaintext'
                self.fields[field].widget.attrs['value'] =  value_dict[field]
            else:
                raise ValueError(f"Field '{field}' does not exist in this form. Check Form Definition")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_view_fields(self.value_dict)

    def get_model_class(self):
        return self._meta.model

class CorpusForm(BaseForm):
    file = forms.FileField(required=False)

    value_dict = {
            'action': 'create',
            'type': 'corpus',
            'child_type': 'document',
            'display_name': 'Corpus',
            'child_name': 'Document',
            'display_attributes': ['name', 'path']
        }

    class Meta:
        model = Corpus
        fields = ['name', 'corpus_type', 'path', 'username', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False
        self.init_view_fields(self.value_dict)

class DocumentForm(BaseForm):
    value_dict = {
            'action': 'list',
            'type': 'corpus',
            'child_type': 'chunk',
            'display_name': 'Document',
            'child_name': 'Chunk',
            'display_attributes': ['name', 'description', 'num_chunks']
        }

    class Meta:
        model = Document
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_view_fields(self.value_dict)

class ChunkForm(BaseForm):
    value_dict = {
            'action': 'list',
            'type': 'chunk',
            'child_type': None,
            'display_name': 'Chunk',
            'child_name': None,
            'display_attributes': ['seq', 'chunk_txt']
        }

    class Meta:
        model = Chunk
        fields = ['document', 'chunk_txt', 'start_index', 'end_index']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_view_fields(self.value_dict)

class KeywordForm(BaseForm):
    value_dict = {
            'action': 'list',
            'type': 'score',
            'child_type': None,
            'display_name': 'Score',
            'child_name': None,
            'display_attributes': None
        }

    class Meta:
        model = Keyword
        fields = ['word', 'short_desc', 'long_desc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_view_fields(self.value_dict)

class ScoreForm(BaseForm):
    value_dict = {
            'action': 'list',
            'type': 'score',
            'child_type': None,
            'display_name': 'Score',
            'child_name': None,
            'display_attributes': None
        }

    class Meta:
        model = Score
        fields = ['chunk', 'keyword', 'value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_view_fields(self.value_dict)
