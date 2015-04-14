# coding: utf-8
from blog.models import Post, Category
from django.views.generic import ListView, DetailView
from utils.mixins import CacheControlMixin


class Counter(object):
    _instance = None
    _count = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Counter, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def get_count(self, path):
        count = self._count.get(path, 0) + 1
        self._count[path] = count

        return count


def print_request_info(request, title):
    print title.center(40, '-')

    print '#:', Counter().get_count(request.path)
    print 'Path: ', request.path
    print 'Cookies:', request.COOKIES
    print 'GET:', request.GET.keys()
    print 'POST:', request.POST.keys()

    headers = ['VARNISH', "IS_AUTH", 'PJAX', "LANG", "SESSIONID", "CSRFTOKEN"]
    for header in headers:
        print '%s: %s' % (
            header,
            request.META['HTTP_X_%s' % header] if 'HTTP_X_%s' % header in request.META else False
        )

    print '-' * 40


class CategoryDetailView(CacheControlMixin, DetailView):
    model = Category
    paginate_by = 6
    cache_timeout = 60 * 60 * 4
    template_name = 'blog/category_detail.html'
    context_object_name = 'category'


class PostsListView(CacheControlMixin, ListView):
    model = Post
    paginate_by = 6
    cache_timeout = 60 * 60 * 4  # 4 hours

    def dispatch(self, request, *args, **kwargs):
        print_request_info(request, 'ListView')
        return super(PostsListView, self).dispatch(request, *args, **kwargs)


class PostDetailView(CacheControlMixin, DetailView):
    model = Post
    cache_timeout = 86400  # 24 hours

    def dispatch(self, request, *args, **kwargs):
        print_request_info(request, 'DetailView')
        return super(PostDetailView, self).dispatch(request, *args, **kwargs)
