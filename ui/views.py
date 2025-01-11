# filepath: ui/views.py
''' This module contains the view functions for the UI app. '''
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from ui.models import Corpus, Keyword
from ui.forms import CorpusForm, KeywordForm

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

## Corpus Management Views
def manage_corpus(request):
    if request.method == 'POST':
        form = CorpusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_corpus')
        else:
            return render(request, 'manage_corpus.html', {'form': form, 'show_form': True})
    else:
        form = CorpusForm()
        corpora = Corpus.objects.all()
        return render(request, 'manage_corpus.html', {'form': form, 'corpora': corpora, 'show_form': False})

def corpus_list(request):
    corpora = Corpus.objects.all()
    return render(request, 'corpus_list.html', {'corpora': corpora, 'show_form': False})

def create_corpus(request):
    if request.method == 'POST':
        form = CorpusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_corpus')
    else:
        form = CorpusForm()
    return render(request, 'manage_corpus.html', {'form': form, 'show_form': True})

## Keyword Management Views

def manage_keywords(request):
    '''Renders the manage keywords page'''
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_keywords')
        else:
            return render(request, 'manage_keywords.html', {'form': form, 'show_form': True})
    else:
        form = KeywordForm()
        keywords = Keyword.objects.all()
        return render(request, 'manage_keywords.html', {'keywords': keywords, 'show_form': False})

def keyword_list(request):
    keywords = Keyword.objects.all()
    return render(request, 'keyword_list.html', {'keywords': keywords})


def create_keyword(request):
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_keywords')
    else:
        form = KeywordForm()
    return render(request, 'manage_keywords.html', {'form': form, 'show_form': True})
