from django.db import models
from markdown import markdown
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from datetime import datetime

class MediaType(models.Model):
    title = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name_plural = "Media Types"

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug if self.slug else self.title)
        
        super(MediaType, self).save(*args, **kwargs)

class Media(models.Model):
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(blank=True)
    file = models.FileField(upload_to="media/%Y/%B", blank=False)
    type = models.ForeignKey(MediaType, blank=False, related_name='media', default=MediaType.objects.get(slug='image').id)
    content = models.TextField(blank=True)
    html = models.TextField(editable=False, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    featured = models.BooleanField(blank=True, default=False)

    class Meta:
        verbose_name_plural = "media"

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.html = markdown(self.content)
        self.slug = slugify(self.title if self.title else datetime.now())
        super(Media, self).save(*args, **kwargs)

