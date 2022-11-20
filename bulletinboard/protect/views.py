from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/default.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_staff'] = self.request.user.is_superuser
        return context

def upgrade_me(request):
    print('!!!! SUCCESS !!!!')
    return redirect('/')