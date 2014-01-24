from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.conf import settings
import os.path

from wagtail.wagtailcore import urls as verdant_urls
from verdantadmin import urls as verdantadmin_urls
from verdantimages import urls as verdantimages_urls
from verdantembeds import urls as verdantembeds_urls
from verdantdocs import admin_urls as verdantdocs_admin_urls
from verdantdocs import urls as verdantdocs_urls
from verdantsnippets import urls as verdantsnippets_urls
from verdantsearch.urls import frontend as verdantsearch_frontend_urls, admin as verdantsearch_admin_urls
from verdantusers import urls as verdantusers_urls
from verdantredirects import urls as verdantredirects_urls

from donations import urls as donations_urls
from rca import app_urls as rca_app_urls, admin_urls as rca_admin_urls
from twitter import urls as twitter_urls

admin.autodiscover()


# Signal handlers
from verdantsearch import register_signal_handlers as verdantsearch_register_signal_handlers
verdantsearch_register_signal_handlers()

from rca_ldap.signal_handlers import register_signal_handlers as rca_ldap_register_signal_handlers
rca_ldap_register_signal_handlers()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'verdant.views.home', name='home'),
    # url(r'^verdant/', include('verdant.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^django-admin/', include(admin.site.urls)),

    # TODO: some way of getting verdantimages to register itself within verdant so that we
    # don't have to define it separately here
    url(r'^admin/images/', include(verdantimages_urls)),
    url(r'^admin/embeds/', include(verdantembeds_urls)),
    url(r'^admin/documents/', include(verdantdocs_admin_urls)),
    url(r'^admin/snippets/', include(verdantsnippets_urls)),
    url(r'^admin/search/', include(verdantsearch_admin_urls)),
    url(r'^admin/users/', include(verdantusers_urls)),
    url(r'^admin/redirects/', include(verdantredirects_urls)),
    url(r'^admin/', include(verdantadmin_urls)),
    url(r'^search/', include(verdantsearch_frontend_urls)),

    url(r'^documents/', include(verdantdocs_urls)),

    url(r'^admin/donations/', include(donations_urls)),

    url(r'^app/', include(rca_app_urls)),
    url(r'^admin/', include(rca_admin_urls)),

    url(r'^twitter/', include(twitter_urls)),

    # For anything not caught by a more specific rule above, hand over to
    # Verdant's serving mechanism
    url(r'', include(verdant_urls)),
)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns() # tell gunicorn where static files are in dev mode
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    urlpatterns += patterns('',
        (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'rca/images/favicon.ico'))
    )
