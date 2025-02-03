'''This file contains the models for usage in the ui app'''
from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    '''Base model with common fields'''
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True

class Corpus(BaseModel):
    '''Model for a corpus'''
    name = models.CharField(max_length=255)
    corpus_type = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    username = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class Document(BaseModel):
    '''Model for a document'''
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    description = models.TextField()
    num_chunks = models.IntegerField()

    def __str__(self):
        return f"Document in {self.name}"

class Chunk(BaseModel):
    '''Model for a chunk'''
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    seq = models.IntegerField()
    chunk_txt = models.TextField()
    start_index = models.IntegerField(default=0)  # Add 'start_index', 'end_index'
    end_index = models.IntegerField(default=-1)
    vector = models.JSONField()
    chunk_size = models.IntegerField(default = 128)

    def __str__(self):
        return f"Chunk {self.seq} of Document {self.document.name}"

class Keyword(BaseModel):
    '''Model for a keyword'''
    word = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=255)
    long_desc = models.TextField()

    def __str__(self):
        return f"{self.word} in {self.word}"

class Score(BaseModel):
    '''Model for a score'''
    chunk = models.ForeignKey(Chunk, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='keyword_scores')
    value = models.FloatField()

    def __str__(self):
        return f"Score {self.value} for Chunk {self.chunk.seq}"

class KeywordReport(BaseModel):
    '''Model for a keyword report'''
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=100)
    scores = models.JSONField()
    summary = models.TextField()
    report = models.TextField()
    review = models.TextField()
    reviewer = models.CharField(max_length=100)

    def __str__(self):
        return f"Keyword Report {self.title} for {self.keyword.pk}"

class DocumentReport(BaseModel):
    '''Model for a document report'''
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    scores = models.JSONField()
    desc = models.TextField()
    summary = models.TextField()
    report = models.TextField()
    review = models.TextField()
    reviewer = models.CharField(max_length=100)

    def __str__(self):
        return f"Document Report {self.title} for document {self.document.name}"

class CorpusReport(BaseModel):
    '''Model for a document report'''
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    summary = models.TextField()
    scores = models.JSONField()
    report = models.TextField()
    review = models.TextField()
    reviewer = models.CharField(max_length=100)

    def __str__(self):
        return f"Corpus Report {self.corpus.pk} for corpus {self.corpus.name}"
