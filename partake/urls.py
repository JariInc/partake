from django.conf.urls import patterns, include, url
import partake.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
		'',
		url(r'^$', partake.views.seasonsPerQuarter),
		url(r'^(\d{4})[Ss](\d)/$', partake.views.seasonsPerQuarter),
    url(r'^serie/(\d+)$', partake.views.singleSeries),
		url(r'^statistics/?$', partake.views.statistics),
		
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    
)
