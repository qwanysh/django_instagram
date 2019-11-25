from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.apps import apps
from django.views.generic import DetailView, UpdateView, View

from ..forms import UserEditForm, UserPasswordChangeForm, UserLoginForm, UserRegisterForm
from ..models import Subscription, User


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
        if self.request.user.is_authenticated:
            kwargs['is_subscribed'] = self._is_subscribed()
        return super().get_context_data(**kwargs)

    def _is_subscribed(self):
        user_id = self.kwargs.get('user_pk')
        try:
            Subscription.objects.get(subscriber=self.request.user.pk, subscribed_to=get_object_or_404(User, pk=user_id))
            return True
        except Subscription.DoesNotExist:
            return False


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
