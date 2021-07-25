from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Article
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin  # new
from django.core.exceptions import PermissionDenied  # new


# Create your views here.
# class ArticleListView(ListView):
class ArticleListView(LoginRequiredMixin, ListView):  # new
    model = Article
    template_name = 'article_list.html'
    login_url = 'login'  # new


# class ArticleDetailView(DetailView):
class ArticleDetailView(LoginRequiredMixin, DetailView):  # new
    model = Article
    template_name = 'article_detail.html'
    login_url = 'login'  # new


"""
We will check if the author of the article is indeed the same user who is currently
logged-in and trying to make a change. At the top of our articles/views.py
file add a line importing PermissionDenied. Then add a dispatch method for both
ArticleUpdateView and ArticleDeleteView.
"""


# class ArticleUpdateView(UpdateView):
class ArticleUpdateView(LoginRequiredMixin, UpdateView):  # new
    model = Article
    fields = ('title', 'body',)
    template_name = 'article_edit.html'
    login_url = 'login'  # new

    def dispatch(self, request, *args, **kwargs):  # new
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


# class ArticleDeleteView(DeleteView):
class ArticleDeleteView(LoginRequiredMixin, DeleteView):  # new
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'  # new

    def dispatch(self, request, *args, **kwargs):  # new
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


"""
We will remove author from the fields and instead set it automatically via the form_valid method.
If you create a new article and then go into the admin you will see it is automatically set to the current logged-in user.
with LoginRequiredMixin, if you are not login, You’ll see the  “Page not found” error.
for redirects users to the log in page use login_url field.
"""


# class ArticleCreateView(CreateView):
class ArticleCreateView(LoginRequiredMixin, CreateView):  # new
    model = Article
    template_name = 'article_new.html'
    # fields = ('title', 'body', 'author',)
    fields = ('title', 'body')  # new
    login_url = 'login'  # new

    def form_valid(self, form):  # new
        form.instance.author = self.request.user
        return super().form_valid(form)
