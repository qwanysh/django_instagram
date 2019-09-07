from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import *

from ..models import *


class UserSubscribeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('user_pk'))
        response = {}

        try:
            subscription = Subscription.objects.get(subscriber=self.request.user, subscribed_to=user)
            subscription.delete()
            response['is_subscribed'] = False
        except Subscription.DoesNotExist:
            Subscription.objects.create(subscriber=self.request.user, subscribed_to=user)
            response['is_subscribed'] = True

        return JsonResponse(response)
