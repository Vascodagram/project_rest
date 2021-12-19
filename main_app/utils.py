from django.shortcuts import render
from .models import Post


class ModelCategoryMixin(Post):
    paginate_by = 3
    model = Post
    template_name = None
    ordering = ['-date']

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(self.model, self).get_context_data()
        data['post'] = self.model.objects.all()
        return data


class ContactAboutMixin:
    template_name = None

    def get(self, request):
        return render(request, self.template_name)
