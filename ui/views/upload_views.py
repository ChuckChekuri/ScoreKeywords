from django.views import View
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from ..forms import BaseForm, CorpusForm

class BaseFileUploadView(View):
    """Base class for file upload views"""
    form_class = BaseForm
    template_name = None
    success_url = None

    def __init__(self):
        super().__init__()
        self.form_class = self.form_class() if self.form_class else None

    def handle_file(self, file):
        raise NotImplementedError

    #pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            self.handle_file(request.FILES['file'])
            instance.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
    #pylint: disable=unused-argument

class CorpusUploadView(BaseFileUploadView):
    """Specific view for corpus file uploads"""
    form_class = CorpusForm
    template_name = 'upload_corpus.html'
    success_url = 'manage_corpus'

    def handle_file(self, file):
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        return fs.url(filename)
