from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import *
from django.apps import apps
from random import randint

from ..models import *
from ..forms import *


class PostListView(ListView):
    template_name = 'post/list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        subscribed_users = self._get_subscribed_users()

        if self.request.user.is_authenticated:
            subscribed_users_posts = Post.objects.filter(author__pk__in=subscribed_users)
            posts_of_current_user = Post.objects.filter(author__pk=self.request.user.pk)
            return (subscribed_users_posts | posts_of_current_user).order_by('-created_at')
        else:
            return Post.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            kwargs['recommended_users'] = self._get_recommended_users()
            kwargs['liked_posts'] = self._get_liked_posts()
            kwargs['subscribed_users'] = self._get_subscribed_users()
        return super().get_context_data(**kwargs)

    def _get_subscribed_users(self):
        Subscription = apps.get_model('users', 'Subscription')
        subscriptions = Subscription.objects.filter(subscriber__pk=self.request.user.pk)
        subscribed_users = []
        for subscription in subscriptions:
            subscribed_users.append(subscription.subscribed_to.pk)
        return subscribed_users

    def _get_liked_posts(self):
        User = apps.get_model('users', 'User')
        liked_posts = []
        likes = get_object_or_404(User, pk=self.request.user.pk).likes.all()
        for like in likes:
            liked_posts.append(like.post.pk)
        return liked_posts

    def _get_recommended_users(self):
        recommended_users_needed = 3  # Сколько пользователей нужно показать
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
        kwargs['comments'] = Comment.objects.filter(post__pk=self.kwargs.get('post_pk')).order_by('created_at')
        if self.request.user.is_authenticated:
            kwargs['liked_posts'] = self._get_liked_posts()
        return super().get_context_data(**kwargs)

    def _get_liked_posts(self):
        User = apps.get_model('users', 'User')
        liked_posts = []
        likes = get_object_or_404(User, pk=self.request.user.pk).likes.all()
        for like in likes:
            liked_posts.append(like.post.pk)
        return liked_posts
