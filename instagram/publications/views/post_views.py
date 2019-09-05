from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import *

# from instagram.users.models import *
from ..models import *
from ..forms import *


class PostListView(ListView):
    template_name = 'post/list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     kwargs['recommended_users'] = User.objects.random()[:3]
    #     return super().get_context_data(**kwargs)


class PostDeleteView(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        return redirect('publications:post_list')

    def test_func(self):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_id)
        return self.request.user.pk == post.author.pk


class PostCreateView(CreateView):
    template_name = 'post/create.html'
    model = Post
    form_class = PostCreateView
    # success_url = 'publications:post_list'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('publications:post_list')
