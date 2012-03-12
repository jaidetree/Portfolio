from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from blog.feeds import LatestPostsFeed 
# from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'portfolio.views.home', name='home'),
    # url(r'^portfolio/', include('portfolio.foo.urls')),

    #(r'^$', direct_to_template, { 'template': 'home.html', 'extra_context': { 'is_home': True } }),
    (r'^', include('oneoffs.urls')),
    (r'^blog/', include('blog.urls')),
    (r'^projects/', include('projects.urls')),
    (r'^associates/', include('associates.urls')),
    url(r'^feed/blog/$', LatestPostsFeed(), name="feed-blog"),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

)                                    

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns( '', 
            (r'^uploads/(?P<path>.*)$', 
        'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

