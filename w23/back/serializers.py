#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from rest_framework import serializers

from w23.back import models
from website.core.models import TimeLayouts


class W23EffettiterritorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W23Effettiterritorio
        fields = "__all__"


class W23ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W23Zone
        fields = "__all__"


class W23PericoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W23Pericolo
        fields = "__all__"


class W23DataSerializer(serializers.ModelSerializer):
    id_w23_zone = W23ZoneSerializer(many=False, read_only=True)
    # idrogeologico_oggi_for = W23PericoloSerializer(many=False, read_only=True)
    # idrogeologico_domani_for = W23PericoloSerializer(many=False, read_only=True)
    # idraulico_oggi_for = W23PericoloSerializer(many=False, read_only=True)
    # idraulico_domani_for = W23PericoloSerializer(many=False, read_only=True)
    # temporali_oggi_for = W23PericoloSerializer(many=False, read_only=True)
    # temporali_domani_for = W23PericoloSerializer(many=False, read_only=True)
    # neve_oggi_for = W23PericoloSerializer(many=False, read_only=True)
    # neve_domani_for = W23PericoloSerializer(many=False, read_only=True)
    # valanghe_oggi_for = W23PericoloSerializer(many=False, read_only=True)
    # valanghe_domani_for = W23PericoloSerializer(many=False, read_only=True)
    # idrogeologico_oggi = W23PericoloSerializer(many=False, read_only=True)
    # idrogeologico_domani = W23PericoloSerializer(many=False, read_only=True)
    # idraulico_oggi = W23PericoloSerializer(many=False, read_only=True)
    # idraulico_domani = W23PericoloSerializer(many=False, read_only=True)
    # temporali_oggi = W23PericoloSerializer(many=False, read_only=True)
    # temporali_domani = W23PericoloSerializer(many=False, read_only=True)
    # neve_oggi = W23PericoloSerializer(many=False, read_only=True)
    # neve_domani = W23PericoloSerializer(many=False, read_only=True)
    # valanghe_oggi = W23PericoloSerializer(many=False, read_only=True)
    # valanghe_domani = W23PericoloSerializer(many=False, read_only=True)

    class Meta:
        model = models.W23Data
        fields = "__all__"


class W23Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W23
        fields = "__all__"


class W23SerializerFull(serializers.ModelSerializer):
    w23data_set = serializers.SerializerMethodField()

    def get_w23data_set(self, obj):
        w23data_set = obj.w23data_set.order_by("id_w23_zone")
        return W23DataSerializer(w23data_set, many=True).data

    class Meta:
        model = models.W23
        fields = "__all__"


class TimeLayoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLayouts
        fields = [
            "id_time_layouts",
            "start_day_offset",
            "end_day_offset",
            "start_time",
            "end_time",
        ]


class SoglieNivoAreaPrevSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SoglieNivoAreaPrev
        fields = [
            "idtab_allertamento",
            "ambito",
            "soglia_cod1",
            "soglia_cod2",
            "soglia_cod3",
        ]


class SogliePluvAreaPrevMassimiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SogliePluvAreaPrevMassimi
        fields = ["idtab_allertamento", "codice_allertamento", "h6", "h12", "h24"]


class SogliePluvAreaPrevMedieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SogliePluvAreaPrevMedie
        fields = [
            "idtab_allertamento",
            "codice_allertamento",
            "h6",
            "h12",
            "h24",
            "h48",
        ]


class W23Pluvossh6Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W23Pluvossh6
        fields = "__all__"
