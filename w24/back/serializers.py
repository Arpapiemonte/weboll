#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from rest_framework import serializers

from w24.back import models


class W24DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W24Data
        fields = "__all__"


class W24Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W24
        fields = "__all__"


class W24SerializerFull(serializers.ModelSerializer):
    w24data_set = W24DataSerializer(many=True, read_only=True)

    # w24data_set = serializers.SerializerMethodField()
    # def get_w24data_set(self, obj):
    #     w24data_set = obj.w24data_set.order_by("id_w24_zone")
    #     return W24DataSerializer(w24data_set, many=True).data

    class Meta:
        model = models.W24
        fields = "__all__"


class W24SoglieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W24Soglie
        fields = "__all__"


class ForecastZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForecastZone
        fields = "__all__"
