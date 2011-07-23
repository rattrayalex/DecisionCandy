from django.conf.urls.defaults import *
from DecisionCandy.app.views import index, style, rank, choose, thanks, signin, create_account

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$',index),
                       (r'^index/$',index),
                       (r'/DC-style.css$',style),
                       (r'/rank/$',rank),
                       (r'/thanks/$',thanks),
                       (r'/choose/$',choose),
    # Example:
    # (r'^decision_candy/', include('decision_candy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
