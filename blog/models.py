from django.db import models
from markdown import markdown
from django.template.defaultfilters import slugify, urlize
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime                
from projects.models import Project
from django.contrib.contenttypes import generic
from media.models import Media
from django import template

import re

class Category(models.Model):
    title = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug if self.slug else self.title)

        super(Category, self).save(*args, **kwargs)

class PublishedPostsManager(models.Manager):
    def get_query_set(self):
        return super(PublishedPostsManager, self).get_query_set().filter(date_published__lte=datetime.now()).filter(status="published")

class Post(models.Model):
    POST_TYPE_CHOICES = (
        ('article', 'Article'),
        ('photo', 'Photo'),
        ('gallery', 'Gallery'),
        ('link', 'Link'),
        ('project', 'Project'),
        ('quote', 'Quote'),
        ('code', 'Code Snippet'),
        ('tweet', 'Tweet'),
    )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=200, unique=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    html = models.TextField()
    slug = models.SlugField(blank=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField()
    template = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    user = models.ForeignKey(User, related_name='+', null=True)
    categories = models.ManyToManyField(Category, related_name="posts", blank=False)
    related_articles = models.ManyToManyField("self", blank=True)
    views = models.BigIntegerField(default=0)
    popularity_rank = models.FloatField(default=0)
    type = models.CharField(max_length=100, blank=True, choices=POST_TYPE_CHOICES, default=POST_TYPE_CHOICES[0][0]) 
    objects = models.Manager()
    published_posts = PublishedPostsManager()
    project = models.ForeignKey(Project, null=True, blank=True)
    media = generic.GenericRelation(Media)
    meta_content = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_published']

    def get_excerpt(self):
        return self.excerpt if self.excerpt else self.content.partition(".")[0] + ".."

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        # return reverse('blog.views.show', None, [str(self.slug)])
        return ('blog.views.show', [str(self.slug)])

    def categories_list(self):
        return ", ".join(category.title for category in self.categories.all())

    def publish_article(self):
        self.status = self.STATUS_CHOICES[1][0]

    def parse_content(self, content):
        tmpl = template.Template(content)

        # Mark our content as HTML safe and strip trailing/leading newlines.
        content = tmpl.render(template.Context({ 'article': self }))

        # Return the rendered template file's html with the content now inside of it. 
        return urlize(markdown(content, ['codehilite']))

    def get_html(self):
        if not self.html:
            self.save_html()
            return self.html
        else:
            return self.html
    
    def save_html(self):
        if not self.html:
            self.html = self.parse_content(self.content)
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug if self.slug else self.title)

        if self.type == "tweet":
            self.meta_content = get_tweet_id(self.meta_content)

        super(Post, self).save(*args, **kwargs)


class PostMeta(models.Model):
    post = models.ForeignKey(Post, related_name='meta')
    key = models.CharField(max_length=100)
    value = models.TextField()

    class Meta:
        verbose_name_plural = "Meta"

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.key = slugify(self.key)

        super(PostMeta, self).save(*args, **kwargs)

def get_tweet_id(content):
    p = re.compile('^http.*/([\d]+)$')
    match = p.match(content)

    if match:
        return match.group(1)
    else:
        return content
