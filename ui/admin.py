'''admin module for the app'''
from django.contrib import admin
from .models import Corpus, Keyword, Document

@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    list_display = ('name', 'corpus_type', 'path', 'username', 'created_at')
    search_fields = ('name', 'corpus_type', 'username')
    list_filter = ('corpus_type', 'created_at')

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('word', 'short_desc', 'long_desc', 'created_at')
    search_fields = ('word', 'short_desc')
    list_filter = ('word',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('corpus', 'name', 'description', 'num_chunks', 'created_at')
    search_fields = ('name', 'description', 'username')
    list_filter = ('name',)
