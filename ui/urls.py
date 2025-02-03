#filepath: ui/urls.py
'''urls for the app'''
from django.urls import path
from django.contrib.auth import views as auth_views
from ui.views.generic_views import GenericObjectView
from ui.views.upload_views import CorpusUploadView
from ui.views.custom_views import home, view_scores, search_corpus

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('view_scores/',  view_scores, name='view_scores'),
    path('search_corpus/', search_corpus, name='search_corpus'),

    # Manage Corpus
    path('corpora/', GenericObjectView.as_view(), {'object_type': 'corpus', 'action': 'list'}, name='corpus_list'),
    path('corpora/new/', GenericObjectView.as_view(), {'object_type': 'corpus', 'action': 'create'}, name='create_corpus'),
    path('corpora/<int:object_id>/', GenericObjectView.as_view(), {'object_type': 'corpus', 'action': 'edit'}, name='edit_corpus'),

    # Manage Documents
    path('docuements/', GenericObjectView.as_view(), {'object_type': 'corpus', 'action': 'list'}, name='corpus_list'),
    path('docuements/new/', GenericObjectView.as_view(), {'object_type': 'corpus', 'action': 'create'}, name='create_corpus'),
    path('docuemnts/<int:object_id>/', GenericObjectView.as_view(), {'object_type': 'corpus', 'action': 'edit'}, name='edit_corpus'),

    # Using GenericObjectView for Keyword operations
    path('keywords/', GenericObjectView.as_view(), {'object_type': 'keyword', 'action': 'list'}, name='keyword_list'),
    path('keywords/new/', GenericObjectView.as_view(), {'object_type': 'keyword', 'action': 'create'}, name='create_keyword'),
    path('keywords/<int:object_id>/', GenericObjectView.as_view(), {'object_type': 'keyword', 'action': 'edit'}, name='edit_keyword'),
    path('uploadcorpus/', CorpusUploadView.as_view(), name='upload_corpus'),
]
