from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

from django.utils.translation import gettext_lazy as _ 

from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                    self).get_queryset()\
                        .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(_('title'),max_length=250)
    slug = models.SlugField(_('slug'),max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='blog_posts',
                                verbose_name=_('author'),)
    body = models.TextField(_('body'))
    publish = models.DateTimeField(_('publish'),default=timezone.now)
    created = models.DateTimeField(_('created'),auto_now_add=True)
    updated = models.DateTimeField(_('updated'),auto_now=True)
    status = models.CharField(_('status'),max_length=10,
                                choices=STATUS_CHOICES,
                                default='draft')
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.publish.year,
                            self.publish.month,
                            self.publish.day,
                            self.slug])

    
