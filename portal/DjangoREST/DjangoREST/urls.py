from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DjangoREST.views.home', name='home'),
    # url(r'^DjangoREST/', include('DjangoREST.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^portal/$', 'portal.views.sensor_data_list'),
    url(r'^portal/temperature$', 'portal.views.temperature_list'),
    url(r'^portal/pressure$', 'portal.views.pressure_list'),
    url(r'^portal/altitude$', 'portal.views.altitude_list'),
    url(r'^portal/switch$', 'portal.views.switch_list'),
    url(r'^portal/soc_temp$', 'portal.views.soc_temp_list'),
    url(r'^portal/arm_freq$', 'portal.views.arm_freq_list'),
    url(r'^portal/core_freq$', 'portal.views.core_freq_list'),
    url(r'^portal/core_volt$', 'portal.views.core_volt_list'),
    url(r'^portal/sdram_volt$', 'portal.views.sdram_volt_list'),
)
