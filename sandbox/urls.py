from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'sandbox.views.home', name='home'),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^menu/', include('menu.urls', namespace='menu')),
    url(r'^admin/', include(admin.site.urls)),

)
