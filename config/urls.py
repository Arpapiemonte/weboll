import typing
from datetime import datetime

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path, register_converter
from django.views import defaults as default_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


class DateConverter:
    regex = r"\d{4}-\d{2}-\d{2}"

    def to_python(self, value):
        date = datetime.strptime(value, "%Y-%m-%d").date()
        return date

    def to_url(self, value):
        return value.datetime.strptime("%Y-%m-%d")


register_converter(DateConverter, "yyyy-mm-dd")

URL = typing.Union[URLPattern, URLResolver]
URLList = typing.List[URL]

urlpatterns: URLList = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path(settings.ADMIN_URL, include("massadmin.urls")),
    path("", include("website.common.urls")),
    path("w05/", include("w05.back.urls")),
    path("w06/", include("w06.back.urls")),
    path("w07/", include("w07.back.urls")),
    path("w12/", include("w12.back.urls")),
    path("w16/", include("w16.back.urls")),
    path("w17/", include("w17.back.urls")),
    path("w23/", include("w23.back.urls")),
    path("w24/", include("w24.back.urls")),
    path("w26/", include("w26.back.urls")),
    path("w28/", include("w28.back.urls")),
    path("w29/", include("w29.back.urls")),
    path("w22/", include("w22.back.urls")),
    path("w30/", include("w30.back.urls")),
    path("w22verifica/", include("w22verifica.back.urls")),
    path("w17verifica/", include("w17verifica.back.urls")),
    path("w31/", include("w31.back.urls")),
    path("w32/", include("w32.back.urls")),
    path("w33/", include("w33.back.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
