import logging
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings
from cms.sitemaps import CMSSitemap
from zinnia.sitemaps import EntrySitemap

admin.autodiscover()
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

sitemaps = {
    'cmspages': CMSSitemap,
    'blog': EntrySitemap,
}

urls = (
    url(r'^admin/', include(admin.site.urls)),  # NOQA
    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # This must be present for the appliaction attachment
    # url(r'^news/', include('zinnia.urls', namespace='zinnia')),
    url(r'^comments/', include('django_comments.urls')),
    # url(r'^tinymce/zinnia/', include('zinnia_tinymce.urls')),
    # url(r'^tinymce/', include('tinymce.urls')),
    # url(r'^ckeditor/', include('ckeditor.urls')),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)


urlpatterns = patterns('', *urls)

# Multilingual URLs
# http://django-cms.readthedocs.org/en/3.0/advanced/i18n.html#multilingual-urls
# urlpatterns += i18n_patterns('', url(r'^', include('cms.urls')))
urlpatterns += patterns('', url(r'^', include('cms.urls')))

# This is only needed when using runserver.
if settings.DEBUG:
    from django.conf.urls.static import static
    media_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
    static_urls = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar
    debug_toolbar_urls = patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
    url(r'^__debug__/', include(debug_toolbar.urls)),

    urlpatterns = static_urls + media_urls + debug_toolbar_urls + urlpatterns
