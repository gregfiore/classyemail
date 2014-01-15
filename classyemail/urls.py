from django.conf.urls import patterns, include, url

import promo_app.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'classyemail.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'promo_app.views.index_view'),
    url(r'^login$', 'promo_app.views.login'),
    url(r'^home$', 'promo_app.views.home_view'),
    url(r'^classify$','promo_app.views.classify_view'),
    url(r'^extract$','promo_app.views.extract_view'),
)
