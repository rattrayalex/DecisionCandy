from django.conf.urls.defaults import *
from DecisionCandy.app.views import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^rank/(.+)/$', rank), 
    (r'^choices/(.+)/$', choices), 
    (r'^choose/$', choose), 
    (r'^thanks/(.+)/$', thanks), 
    (r'^results/(.+)/$', results), 
    (r'(\w+)/rank/xhr/(?P<format>\w+)$', rank_xhr),
    (r'^signin/$', signin),
    (r'^signup/$', signup),
    (r'^$', index), 
    (r'^loggedin/$', loggedin),
    (r'^logout/$', logout),
    (r'^upload/$', upload_files),
    (r'vote/w/(.+)/l/(.+)/$', vote)
    )
