from django.db import models
from markdown import markdown
from django.template.defaultfilters import slugify

class ContentSection(models.Model):
    title = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(blank=True, unique=True)
    content = models.TextField(blank=True)
    html = models.TextField(editable=False, blank=True)

    class Meta:
        verbose_name_plural = "Content Sections"

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug if self.slug else self.title)
        self.html = markdown(self.content)

        super(ContentSection, self).save(*args, **kwargs)


