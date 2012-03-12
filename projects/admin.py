from projects.models import Project, Category, Resource, Identity
from django.contrib import admin
from django.db import models
from django.contrib.contenttypes import generic
from media.models import Media

class MediaInline(generic.GenericStackedInline):
    fields = ('file',)
    model = Media
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'url', 'category', 'slug', 'content', 'featured', 'work_involved', 'image', 'identity', 'complete'] }),
        ('Notes', {'fields': ['side_notes']}),
        ('Date Information', {'fields': ['date_launched']}),
        ('Resources', {'fields': ['resources']}),
    ]

    inlines = [
        MediaInline,
    ]

    filter_horizontal = ('resources'),


admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)
admin.site.register(Resource)
admin.site.register(Identity)

