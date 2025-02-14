from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from ui.models import Corpus, Document, Chunk, Keyword, Score
from ui.forms.all_forms import BaseForm, CorpusForm, DocumentForm, ChunkForm, KeywordForm, ScoreForm

class GenericObjectView(View):
    template_name = 'manage_object.html'

    object_type = None
    action = None
    object_id = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # Store whatever you want from kwargs or elsewhere
        self.object_type = kwargs.get('object_type', None)
        self.action = kwargs.get('action', None)
        self.object_id = kwargs.get('object_id', None)

    # python trick to do if then else by looking up a dictionary
    def get_form_class(self):
        return {
            'corpus': CorpusForm,
            'document': DocumentForm,
            'chunk': ChunkForm,
            'keyword': KeywordForm,
        }.get(self.object_type)


    def get(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        form_class = self.get_form_class()

        instance = None
        form = form_class()
        model_class = form.get_model_class()
        if not self.object_id:
            objects = model_class.objects.all()
            title_prefix = "Edit "
        else:
            instance = get_object_or_404(model_class, pk=self.object_id)
            title_prefix = "List "
            form = form_class(instance=instance)

        context = {
                'form': form,
                'object_type': self.object_type, 
                'object_id': self.object_id,
                'action': self.action,
                'object_display_name': f"{title_prefix} {form.value_dict['display_name']}",
                'child_display_name': form.value_dict['child_name']
            }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        form = self.get_form_class()()
        model_class = form.get_model_class()
        if self.object_id:
            instance = get_object_or_404(model_class, pk=self.object_id)
            form = form(request.POST, instance=instance)
        else:
            form = form(request.POST)

        if form.is_valid():
            obj = form.save()
            return redirect(reverse('edit_object', kwargs={'object_type': self.object_type, 'object_id': obj.id}))

        context = {'form': form, 'action': 'edit' if self.object_id else 'create', 'object_id': self.object_id, 'object_type': self.object_type}
        return render(request, self.template_name, context)

    def delete(self, _request, *args, **kwargs):
        super().setup(_request, *args, **kwargs)

        model_class = self.get_model_class()
        instance = get_object_or_404(model_class, pk=self.object_id)
        instance.delete()
        return HttpResponseRedirect(reverse('edit_object', kwargs={'object_type': self.object_type}) + '?list')

class CorpusListView(LoginRequiredMixin, ListView):
    model = Corpus
    template_name = 'manage_object.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'corpus'
        context['action'] = 'list'
        return context

class CorpusCreateView(LoginRequiredMixin, CreateView):
    model = Corpus
    template_name = 'manage_object.html'
    fields = ['name', 'corpus_type', 'path', 'username']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CorpusUpdateView(LoginRequiredMixin, UpdateView):
    model = Corpus
    template_name = 'manage_object.html'
    fields = ['name', 'corpus_type', 'path', 'username']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
