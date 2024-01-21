from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import NewsForm, ArticleForm
from django import forms

from newsportal.models import Post



class PostList(ListView):
    model = Post
    ordering = 'dateCreation'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts_count'] = self.filterset.qs.count()
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'newsportal/post.html'
    context_object_name = 'post'

class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'newsportal/news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)
    
class NewsEdit(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'newsportal/post_edit.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Сохраняем информацию о типе объекта в атрибуте
        self.object_type = obj.categoryType

        if obj.categoryType != 'NW':
            raise forms.ValidationError("По этому пути нельзя редактировать СТАТЬИ")
        
        return obj

class NewsDelete(DeleteView):
    model = Post
    template_name = 'newsportal/post_delete.html'
    success_url = reverse_lazy('posts')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Сохраняем информацию о типе объекта в атрибуте
        self.object_type = obj.categoryType

        if obj.categoryType != 'NW':
            raise forms.ValidationError("По этому пути нельзя удалить СТАТЬИ")
        
        return obj
    
class ArticlesCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'newsportal/article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)
    
class ArticlesEdit(UpdateView):
    form_class = ArticleForm
    model = Post
    template_name = 'newsportal/post_edit.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Сохраняем информацию о типе объекта в атрибуте
        self.object_type = obj.categoryType

        if obj.categoryType != 'AR':
            raise forms.ValidationError("По этому пути нельзя редактировать НОВОСТИ")
        
        return obj
    
class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'newsportal/post_delete.html'
    success_url = reverse_lazy('posts')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Сохраняем информацию о типе объекта в атрибуте
        self.object_type = obj.categoryType

        if obj.categoryType != 'AR':
            raise forms.ValidationError("По этому пути нельзя удалить НОВОСТИ")
        
        return obj
    


