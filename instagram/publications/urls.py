from django.urls import path
from .views import *

app_name = 'publications'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:post_pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
