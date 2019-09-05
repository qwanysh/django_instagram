from django.urls import path
from .views import *

app_name = 'publications'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:post_pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:post_pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('<int:post_pk>/', PostDetailView.as_view(), name='post_detail'),
    path('new_post/', PostCreateView.as_view(), name='post_create'),
]
