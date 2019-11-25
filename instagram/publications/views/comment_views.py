from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from ..models import Post, Comment


class CommentCreateView(View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('post_pk'))

        comment = Comment()
        comment.author = self.request.user
        comment.post = post
        comment.text = self.request.POST.get('text')
        comment.save()

        return redirect(reverse('publications:post_detail', kwargs={'post_pk': kwargs.get('post_pk')}))


class CommentDeleteView(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('comment_pk'))
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER'))

    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('comment_pk'))
        return self.request.user.pk == comment.author.pk
