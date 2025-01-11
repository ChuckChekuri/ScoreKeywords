#filepath: ui/urls.py
'''urls for the app'''
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('manage_keywords/', views.manage_keywords, name='manage_keywords'),
    path('view_scores/', views.view_scores, name='view_scores'),
    path('search_corpus/', views.search_corpus, name='search_corpus'),
    path('corpora/', views.manage_corpus, name='manage_corpus'),
    path('corpora/new/', views.create_corpus, name='create_corpus'),
    path('corpora/list/', views.corpus_list, name='corpus_list'),
    path('keywords/', views.manage_keywords, name='manage_keywords'),
    path('keywords/list/', views.keyword_list, name='keyword_list'),
    path('keywords/new/', views.create_keyword, name='create_keyword'),
]
