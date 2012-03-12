from blog.models import Post, Category, PostMeta
from media.models import Media
from django.contrib import admin
from django.contrib.contenttypes import generic

class MediaInline(generic.GenericStackedInline):
    model = Media
    extra = 1
    template = 'admin/blog/edit_inline/stacked.html'

class MetaInline(admin.StackedInline):
    model = PostMeta
    extra = 1
    template = 'admin/blog/edit_inline/stacked.html'

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'slug', 'excerpt', 'content', 'type', 'status', 'template', 'meta_content'] }),
        ('Date Information', {'fields': ['date_published']}),
        ('Organization', {'fields': ['categories']}),
        ('Advanced', {'fields': ['related_articles', 'project' ], 'classes': ['collapse']}),
    ]

    inlines = [
        MediaInline,
        MetaInline
    ]

    filter_horizontal = ['categories', 'related_articles']

    def save_model(self, request, obj, form, change):
        if request.POST and request.POST.has_key('_publish') and request.POST['_publish']:
            obj.publish_article()

        obj.html = ""
        obj.user = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        formset.save()

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
