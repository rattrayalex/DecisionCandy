from django.conf.urls.defaults import *
from DecisionCandy.app.views import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'rank/$', rank), 
    (r'choices/$', choices), 
    (r'(\w+)/thanks/$', thanks), 
    (r'choose/$', choose), 
    (r'(\w+)/results/$', results), 
    (r'(\w+)/rank/xhr/(?P<format>\w+)$', rank_xhr), 

    (r'^$', index), 
    )
