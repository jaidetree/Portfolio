from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('oneoffs.views',
    (r'^about/$', 'about'),
    (r'^contact/$', 'contact'),
    (r'^contact/thanks/$', 'contact_thanks'),
    (r'^$', 'home'),
    (r'^dribbble/latest_shot$', 'latest_dribbble_shot' ),
)
