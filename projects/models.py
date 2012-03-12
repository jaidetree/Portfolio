from django.db import models
from django.template.defaultfilters import slugify
from markdown import markdown
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.text import normalize_newlines
from django.contrib.contenttypes import generic
from media.models import Media
import re

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug if self.slug else self.title)

        super(Category, self).save(*args, **kwargs)

class Resource(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, unique=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug if self.slug else self.title)

        super(Resource, self).save(*args, **kwargs)

class Identity(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name_plural = "identities"

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug if self.slug else self.title)

        super(Identity, self).save(*args, **kwargs)


class CompletedProjectsManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return super(CompletedProjectsManager, self).get_query_set().filter(complete=True)

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_launched = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True)
    content = models.TextField(blank=True)
    html = models.TextField(editable=False)
    category = models.ForeignKey(Category, related_name="projects")
    featured = models.BooleanField(default=False)
    #image = models.ImageField(upload_to='projects', blank=True)
    image = ThumbnailerImageField(upload_to='projects', resize_source=dict(size=(800, 1020), crop=False), blank=True)
    identity = models.ForeignKey(Identity, related_name="projects", blank=False, null=True)
    work_involved = models.TextField(blank=True)
    resources = models.ManyToManyField(Resource, related_name="projects", blank=False)
    side_notes = models.TextField(blank=True)
    images = generic.GenericRelation(Media)
    complete = models.BooleanField(default=False)
    objects = models.Manager()
    completed = CompletedProjectsManager()

    class Meta:
        ordering = ['-date_launched'] # change to '-date_created' if you want reverse chrono (newest first)

    def work(self):
        if len(self.work_involved) < 1:
            return ""

        lines = normalize_newlines(self.work_involved).split("\n")
        for i in range(0, len(lines)):
            if lines[i] == "": 
                del lines[i]
                continue
            lines[i] = '* ' + re.sub(r'^\s*\*\s*', '', lines[i])

        return "\n".join(lines)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.html = markdown(self.content)
        self.slug = slugify(self.slug if self.slug else self.title)

        super(Project, self).save(*args, **kwargs)


