from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from blog.managers import ImportantManager
from utils.varnish import ban as varnish_ban


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.title

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    datetime = models.DateTimeField('Publication date')
    content = models.TextField(max_length=10000)
    is_important = models.BooleanField(default=False)
    category = models.ForeignKey(Category, blank=True, null=True)
    objects = models.Manager()
    important_objects = ImportantManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-datetime', )

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})


@receiver(post_delete, sender=Post)
@receiver(post_save, sender=Post)
def detail_page_cache_invalidation(sender, **kwargs):
    post = kwargs['instance']

    # Invalidate detail page of post
    varnish_ban(post.get_absolute_url())


@receiver(post_delete, sender=Post)
@receiver(post_save, sender=Post)
def list_page_cache_invalidation(sender, **kwargs):
    if kwargs.get('created', False) or 'created' not in kwargs:
        # Invalidate main blog page
        varnish_ban('/blog/$')

        # Invalidate pagination
        varnish_ban('/blog/\\?')


