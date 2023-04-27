#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
import datetime
import math

from django.utils import timezone
from rest_framework import serializers

from w30.back import models
from website.core.models import TimeLayouts

current_tz = timezone.get_current_timezone()
tls_lookup = {}  # type: ignore


class W30DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W30Data
        fields = "__all__"


class W30Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W30
        fields = "__all__"


class W30SerializerFull(serializers.ModelSerializer):
    w30data_set = W30DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W30
        fields = "__all__"


today = datetime.datetime.now().date()


def get_minutes(tl):
    return (
        round(
            (
                datetime.datetime.combine(today, tl.end_time)
                - datetime.datetime.combine(today, tl.start_time)
            ).total_seconds()
            / 60
        )
        + (tl.end_day_offset - tl.start_day_offset) * 24 * 60
    )


class W30CurrentDataViewSerializer(serializers.ModelSerializer):
    id_time_layouts_corrected = serializers.SerializerMethodField()

    class Meta:
        model = models.W30Data
        fields = "__all__"

    def get_id_time_layouts_corrected(self, obj):
        global tls_lookup
        if tls_lookup == {}:
            start_day_offsets = [
                tl.start_day_offset
                for tl in TimeLayouts.objects.distinct("start_day_offset")
            ]
            minutes = list(set([get_minutes(tl) for tl in TimeLayouts.objects.all()]))
            tls_lookup = {sdo: {m: {} for m in minutes} for sdo in start_day_offsets}
            tls = TimeLayouts.objects.all()
            for tl in tls:
                if tl.start_day_offset in tls_lookup:
                    tls_lookup[tl.start_day_offset][get_minutes(tl)][
                        tl.start_time
                    ] = tl.id_time_layouts
            print(tls_lookup)
        midnight = datetime.datetime.combine(
            datetime.date.today(), datetime.datetime.min.time()
        )
        delta = obj.start - midnight
        start_day_offset = math.floor(delta.total_seconds() / 86400)
        minutes = round((obj.end - obj.start).total_seconds() / 60)  # type: ignore
        start_time = obj.start.astimezone(current_tz).time()
        if start_day_offset in tls_lookup:
            lu = tls_lookup[start_day_offset][minutes]
            if start_time in lu:
                return lu[start_time]
            else:
                # print(f"start time {start_time} not found")
                return None
        else:
            # print(f"start day offset {start_day_offset} not found")
            return None
