#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
import datetime

from rest_framework import serializers

from website.core import models


class W16Data1Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W16Data1
        fields = "__all__"


class W16DataSerializer(serializers.ModelSerializer):
    w16data1_set = W16Data1Serializer(many=True, read_only=True)

    class Meta:
        model = models.W16Data
        fields = "__all__"


class W16Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W16
        fields = "__all__"


class W16SerializerFull(serializers.ModelSerializer):
    w16data_set = serializers.SerializerMethodField()

    last_seq_num = serializers.SerializerMethodField()

    def get_last_seq_num(self, obj):
        today = datetime.datetime.today()
        try:
            return (
                models.W16.objects.filter(start_valid_time__year=today.year)
                .exclude(status="0")
                .latest("seq_num")
                .seq_num
            )
        except models.W16.DoesNotExist:
            return 0

    def get_w16data_set(self, obj):
        w16data_set = obj.w16data_set.order_by("id_scadenza", "id_ozono_zone")
        return W16DataSerializer(w16data_set, many=True).data

    class Meta:
        model = models.W16
        fields = "__all__"


class W16ConfSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W16Conf
        fields = "__all__"


class OzonoLivelliSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OzonoLivelli
        fields = [
            "id_ozono_livelli",
            "livelli",
            "rgb",
            "soglia_inferiore_mxd",
            "soglia_inferiore_mx8",
            "rgb",
            "sintesi_raccomandazioni",
            "descrizione",
            "raccomandazione",
        ]
