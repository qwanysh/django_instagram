from django.urls import path
from .views import *

app_name = 'publications'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:post_pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:post_pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('<int:post_pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('<int:post_pk>/like/', LikeView.as_view(), name='like'),
    path('new_post/', PostCreateView.as_view(), name='post_create'),
    path('comments/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]
