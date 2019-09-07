from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import *
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.apps import apps

from ..models import User
from ..forms import *


class UserDetailView(DetailView):
    template_name = 'user/details.html'
    pk_url_kwarg = 'user_pk'
    model = User
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        Post = apps.get_model('publications', 'Post')
        posts = Post.objects.filter(author__pk=self.kwargs.get('user_pk'))
        kwargs['posts'] = posts
        kwargs['posts_count'] = len(posts)
        return super().get_context_data(**kwargs)


class UserEditView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user/edit.html'
    form_class = UserEditForm
    context_object_name = 'account'
    pk_url_kwarg = 'user_pk'

    def test_func(self):
        return self.request.user.pk == self.kwargs['user_pk']

    def get_success_url(self):
        return reverse('users:details', kwargs={'user_pk': self.object.pk})


class UserPasswordChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user/password_change.html'
    form_class = UserPasswordChangeForm
    context_object_name = 'account'
    pk_url_kwarg = 'user_pk'

    def test_func(self):
        return self.request.user.pk == self.kwargs['user_pk']

    def get_success_url(self):
        return reverse('users:login')


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(request.META.get('HTTP_REFERER'))


def account_login_view(request):
    if request.method == 'POST':
        context = {
            'form': UserLoginForm(data=request.POST)
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('publications:post_list')
        else:
            context['has_error'] = True
            return render(request, 'user/login.html', context=context)
    context = {
        'form': UserLoginForm()
    }
    return render(request, 'user/login.html', context=context)


def account_register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('publications:post_list')
        else:
            context = {
                'form': form,
                'has_error': True
            }
            return render(request, 'user/register.html', context=context)
    else:
        form = UserRegisterForm()
        context = {
            'form': form
        }
        return render(request, 'user/register.html', context=context)
