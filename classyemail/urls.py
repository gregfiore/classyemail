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

    url(r'email$', 'promo_app.views.all_email_view'),    # View to see all emails
    url(r'email/(?P<email_pk>\d+)/$', 'promo_app.views.email_detail_view'),  # View details of a specific email
    url(r'email/(?P<email_pk>\d+)/set_promotion$', 'promo_app.views.email_set_promotion'),  # View details of a specific email
)
