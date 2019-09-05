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

