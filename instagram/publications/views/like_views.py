from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from ..models import Post, Like


class LikeView(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('post_pk'))
        response = {}

        try:
            like = Like.objects.get(post=post, user=self.request.user)
            like.delete()
            response['is_liked'] = False
        except Like.DoesNotExist:
            Like.objects.create(post=post, user=self.request.user)
            response['is_liked'] = True

        response['total_likes'] = len(post.likes.all())

        return JsonResponse(response)
