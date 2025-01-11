'''admin module for the app'''
from django.contrib import admin
from .models import Corpus, Keyword

@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'path', 'username', 'ingest_at')
    search_fields = ('name', 'type', 'username')
    list_filter = ('type', 'ingest_at')

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('word', 'short_desc', 'long_desc', 'created_at')
    search_fields = ('word', 'short_desc')
    list_filter = ('created_at',)
