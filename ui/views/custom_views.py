# filepath: ui/views.py
''' This module contains the view functions for the UI app. '''
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views.generic.edit import FormView
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from ui.models import Corpus, Document, Chunk, Keyword
from ui.forms.all_forms import CorpusForm, DocumentForm, ChunkForm, KeywordForm
from ui.serializers import CorpusSerializer, DocumentSerializer, ChunkSerializer


import pandas as pd
import sqlite3
import faiss
import os

def home(request):
    '''Renders the home page'''
    return render(request, 'home.html')

def view_scores(request):
    '''Renders the scoring results page'''
    # Add logic to fetch and display scoring results
    return render(request, 'view_scores.html')

def search_corpus(request):
    '''Renders the search corpus page'''
    # Add logic to handle search functionality
    return render(request, 'search_corpus.html')


def upload_corpus(request):
    '''Renders the upload corpus page'''
    if request.method == 'POST':
        form = CorpusForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('edit_corpus')
    else:
        form = CorpusForm()
    return render(request, 'upload_corpus.html', {'form': form})

class ProcessDocumentView(View):
    #pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        try:
            document = Document.objects.create(
                corpus_id=request.POST.get('corpus_id'),
                name=request.POST.get('title'),
                description=request.POST.get('description'),
                num_chunks=0,
                created_by=request.user
            )
            self.chunk_and_encode(document)
            return JsonResponse({'status': 'success'}, status=201)
        except (Document.DoesNotExist, ValueError, KeyError) as e:
            return JsonResponse({'error': str(e)}, status=400)
        #pylint: enable=unused-argument

    def chunk_and_encode(self, document):
        content = document.description
        words = content.split()
        chunk_size = 400
        overlap = 100
        chunks = []

        for start in range(0, len(words), chunk_size - overlap):
            end = min(start + chunk_size, len(words))
            chunk_content = ' '.join(words[start:end])
            encoding = self.encode_chunk(chunk_content)
            chunk = Chunk.objects.create(
                document=document,
                seq=len(chunks) + 1,
                chunk_txt=chunk_content,
                vector=encoding.decode('utf-8'),
                chunk_size=len(chunk_content.split()),
                created_by=document.created_by
            )
            chunks.append(chunk)

        document.num_chunks = len(chunks)
        document.save()

    def encode_chunk(self, chunk_content):
        # Example encoding logic
        # Replace with your actual encoding logic
        return chunk_content.encode('utf-8')
