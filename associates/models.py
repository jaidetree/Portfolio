from django.db import models
from django.template.defaultfilters import slugify
from easy_thumbnails.fields import ThumbnailerImageField
from markdown import markdown

class Associate(models.Model):
    TYPE_CHOICES = (
        ('P', 'Person'),
        ('B', 'Business'),
        ('T', 'Technology')
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    content = models.TextField(blank=False)
    html = models.TextField(editable=False, blank=True)
    url = models.URLField(null=True)
    avatar = ThumbnailerImageField(upload_to='associates', resize_source=dict(size=(200, 200), crop='smart'), blank=True)
    type = models.CharField(max_length=100, blank=True, choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0]) 
    inner_circle = models.BooleanField(default=False)
    specialty = models.CharField(max_length=100, default="Web")

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug if self.slug else self.name)
        self.html = markdown(self.content)
        super(Associate, self).save(*args, **kwargs)



