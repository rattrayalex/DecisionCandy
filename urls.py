from django.conf.urls.defaults import *
from django.contrib import admin

import app

admin.autodiscover()

urlpatterns = patterns('',
    (r'^app/', include(app.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    )
