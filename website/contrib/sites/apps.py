from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SitesConfig(AppConfig):
    name = "website.contrib.sites"
    verbose_name = _("Sites")
    label = "sites_override"
