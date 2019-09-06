from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import *
from django.apps import apps
from random import randint

# from instagram.users.models import *
from ..models import *
from ..forms import *


class PostListView(ListView):
    template_name = 'post/list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        kwargs['recommended_users'] = self.get_recommended_users()
        return super().get_context_data(**kwargs)

    def get_recommended_users(self):
        recommended_users_needed = 3    # Сколько пользователей нужно показать
        recommended_users = []
        User = apps.get_model('users', 'User')
        users = User.objects.all()
        max_user_index = len(users)

        # Если пользователей меньше, чем нужно, то выведи сколько есть
        if (max_user_index - 1) < recommended_users_needed:
            recommended_users_needed = max_user_index - 1

        recommended_user_count = 0
        already_added_indexes = []
        while True:
            # Если пользователей уже достаточно
            if recommended_user_count == recommended_users_needed:
                break
            random_index = randint(1, max_user_index)

            # Не добавляй меня и уже добавленных пользователей
            if random_index == self.request.user.pk or random_index in already_added_indexes:
                continue

            already_added_indexes.append(random_index)
            recommended_users.append(User.objects.get(pk=random_index))
            recommended_user_count += 1
        return recommended_users


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
    form_class = PostForm

    # success_url = 'publications:post_list'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('publications:post_list')


class PostEditView(UserPassesTestMixin, UpdateView):
    template_name = 'post/edit.html'
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_pk'

    def get_success_url(self):
        return reverse('publications:post_list')

    def test_func(self):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_id)
        return self.request.user.pk == post.author.pk


class PostDetailView(DetailView):
    template_name = 'post/detail.html'
    pk_url_kwarg = 'post_pk'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        kwargs['comments'] = Comment.objects.filter(post__pk=self.kwargs.get('post_pk'))
        return super().get_context_data(**kwargs)
