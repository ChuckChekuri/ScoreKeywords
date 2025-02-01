from rest_framework import serializers
from .models import Corpus, Document, Chunk

class CorpusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corpus
        fields = ['id', 'name', 'type', 'path', 'username', 'ingest_at']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'corpus', 'name', 'description', 'num_chunks', 'created_at']

class ChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chunk
        fields = ['id', 'document', 'seq', 'chunk_txt', 'vector', 'chunk_size', 'created_at']
