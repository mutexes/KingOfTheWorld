from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'kotw.views.home', name='home'),
    # url(r'^kotw/', include('kotw.foo.urls')),
    url(r'^register/', 'kotw.views.register'),
    url(r'^login/', 'kotw.views.signin'),
    url(r'^hq/', 'kotw.views.main'),
    url(r'^explore/', 'kotw.countries.views.explore'),
    url(r'^build/', 'kotw.countries.views.build'),
    url(r'^military/', 'kotw.countries.views.military'),
    url(r'^research/', 'kotw.countries.views.research'),
    url(r'^attack/', 'kotw.views.attack'),
    url(r'^ranks/', 'kotw.views.ranks'),
    url(r'^logout/', 'kotw.views.signout'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
