from django.conf.urls.defaults import *
from DecisionCandy.app.views import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'media/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.MEDIA_ROOT}),
                       (r'^$',index),
                       (r'^index/$',index),
                       (r'(\w+)/(\d{1,2})/rank/$',rank),
                       (r'(\w+)/thanks/$',thanks),
                       (r'choose/$',choose),
                       (r'(\w+)/results/$',results),
                       (r'(\w+)/rank/xhr/(?P<format>\w+)$',rank_xhr),
    # Example:
    # (r'^decision_candy/', include('decision_candy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
