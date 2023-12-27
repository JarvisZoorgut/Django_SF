from django.shortcuts import render
from django.views.generic import ListView, DetailView

from newsportal.models import Post



class PostList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'newsportal/news.html'
    context_object_name = 'news'


class PostDetail(DetailView):
    model = Post
    template_name = 'newsportal/new.html'
    context_object_name = 'new'
