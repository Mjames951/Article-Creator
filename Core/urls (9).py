from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *

sitemaps = {
    "static": StaticSitemap,
    "products": ProductSitemap,
    "articles": ArticleSitemap
}

urlpatterns = [
    path('onetwothreethatsenoughforme/', include('django.contrib.auth.urls')),
    path('', include("shop.urls")),
    path('article/', include("blog.urls")),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),

    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT}), #serve static files when deployed
]
