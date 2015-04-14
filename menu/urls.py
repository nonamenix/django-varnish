#coding: utf-8
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from blog.views import PostsListView, PostDetailView

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='menu/menu.html'), name='index'),
)
