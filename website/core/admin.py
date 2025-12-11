#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.contrib import admin
from django.contrib.admin.models import DELETION
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from w06.back.models import W06, W06Data
from w07.back.models import W07, W07Data
from w12.back.models import W12, W12Data
from w15.back.models import W15, W15Data
from w17.back.models import W17, W17Data
from w17verifica.back.models import w17_verifica, w17_verifica_data
from w20.back.models import W20, W20Data
from w21.back.models import W21, W21Data
from w22.back.models import W22, W22Data
from w22verifica.back.models import W22Verifica
from w23.back.models import W23, W23Data
from w23verifica.back.models import W23Verifica
from w24.back.models import W24, W24Data
from w26.back.models import W26, W26Data
from w28.back.models import W28, W28Data
from w29.back.models import W29, W29Data
from w30.back.models import W30, W30Data
from w31.back.models import W31
from w32.back.models import W32, W32Data
from w33.back.models import W33, W33Data
from w34.back.models import W34, W34Data
from w35.back.models import W35, W35Data
from w36.back.models import W36, W36Data
from w37.back.models import W37, W37Data
from w38.back.models import W38, W38Data

from .models import W05, W16, Bulletins, Destinazioni, W05Data, W16Data

admin.register(
    W05,
    W05Data,
    W06,
    W06Data,
    W07,
    W07Data,
    W12,
    W12Data,
    W15,
    W15Data,
    W16,
    W16Data,
    W17,
    W17Data,
    w17_verifica,
    w17_verifica_data,
    W20,
    W20Data,
    W21,
    W21Data,
    W22,
    W22Data,
    W22Verifica,
    W23,
    W23Data,
    W23Verifica,
    W24,
    W24Data,
    W26,
    W26Data,
    W28,
    W28Data,
    W29,
    W29Data,
    W30,
    W30Data,
    W31,
    W32,
    W32Data,
    W33,
    W33Data,
    W34,
    W34Data,
    W35,
    W35Data,
    W37,
    W37Data,
    W38,
    W38Data,
    W36,
    W36Data,
)(admin.ModelAdmin)


@admin.register(admin.models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = "action_time"

    # to filter the resultes by users, content types and action flags
    list_filter = ["user", "content_type", "action_flag"]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = ["object_repr", "change_message"]

    list_display = [
        "action_time",
        "user",
        "content_type",
        "action_flag",
        "change_message",
        "object_link",
    ]

    list_select_related = True

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        text = escape(obj.object_repr)
        if obj.action_flag == DELETION:
            link = text.strip()
        else:
            ct = obj.content_type
            url = reverse(
                "admin:%s_%s_change" % (ct.app_label, ct.model),
                args=(obj.object_id,),
            )
            link = '<a href="%s">%s</a>' % (url.strip(), text.strip())
        return mark_safe(link)


@admin.register(Destinazioni)
class DestinazioniAdmin(admin.ModelAdmin):
    list_display = [
        "prodotto",
        "destinazione",
        "endpoint",
        "segreto",
        "enabled",
        "auto",
    ]


@admin.register(Bulletins)
class BulletinsAdmin(admin.ModelAdmin):
    list_display = ["prodotto", "auto", "time"]
