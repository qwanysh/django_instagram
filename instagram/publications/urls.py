from django.urls import path
from .views import *

app_name = 'publications'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
]
