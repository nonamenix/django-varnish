# coding: utf-8
from django.conf.urls import patterns, url
from django.views.generic import ListView
from blog.models import Post, Category

from blog.views import PostsListView, PostDetailView, CategoryDetailView


urlpatterns = patterns(
    '',
    url(r'^$', PostsListView.as_view(), name='list'),
    url(r'^importants/$', ListView.as_view(
        queryset=Post.important_objects.all()[0:5],
        template_name='blog/importants.html',
        context_object_name='posts'
    ), name='importants'),
    url(r'^categories/$', ListView.as_view(
        queryset=Category.objects.all(),
        template_name='blog/categories.html',
        context_object_name='categories'
    ), name='categories'),
    url(r'^category/(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category'),
    url(r'^(?P<slug>[-\w]+)/$', PostDetailView.as_view(), name='detail'),
)
