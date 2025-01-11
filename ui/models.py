'''This file contains the models for the Django'''
from django.db import models

class Corpus(models.Model):
    '''Model for a corpus'''
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    username = models.CharField(max_length=100)
    ingest_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

class Document(models.Model):
    '''Model for a document'''
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    num_chunks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document in {self.name}"

class Chunk(models.Model):
    '''Model for a document'''
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    seq = models.IntegerField()
    chunk_txt = models.TextField()
    vector = models.JSONField()
    chunk_size = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chunk {str(self.seq)} in {self.document.name}"

class Keyword(models.Model):
    '''Model for a keyword'''
    word = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=255)
    long_desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.word} in {self.word}"

class Score(models.Model):
    '''Model for a score'''
    chunk = models.ForeignKey(Chunk, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='keyword_scores')
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #pylint: disable=E1101
        return f"Score {self.score} for {self.keyword.pk} in {self.chunk.pk}"
        # pylint: enable=E1101

class KeywordReport(models.Model):
    '''Model for a keyword report'''
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    scores = models.JSONField()
    summary = models.TextField()
    report = models.TextField()
    review = models.TextField()
    reviewer = models.CharField(max_length=100)

    def __str__(self):
        #pylint: disable=E1101
        return f"Keyword Report {self.title} for {self.keyword.pk}"
        #pylint: enable=E1101

class DocumentReport(models.Model):
    '''Model for a document report'''
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    scores = models.JSONField()
    desc = models.TextField()
    summary = models.TextField()
    report = models.TextField()
    review = models.TextField()
    reviewer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document Report {self.title} for document {self.document.name}"

class CorpusReport(models.Model):
    '''Model for a document report'''
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    summary = models.TextField()
    scores = models.JSONField()
    report = models.TextField()
    review = models.TextField()
    reviewer = models.CharField(max_length=100)

    def __str__(self):
        #pylint: disable=E1101
        return f"Corpus Report {self.corpus.pk} for corpus {self.corpus.name}"
        #pylint: enable=E1101
