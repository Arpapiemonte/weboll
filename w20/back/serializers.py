#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from rest_framework import serializers

from w20.back import models


class W20PericoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W20Pericolo
        fields = "__all__"


class W20ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W20Zone
        fields = "__all__"


class W20DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W20Data
        fields = "__all__"


class W20Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W20
        fields = "__all__"


class W20SerializerFull(serializers.ModelSerializer):
    w20data_set = serializers.SerializerMethodField()

    def get_w20data_set(self, obj):
        w20data_set = obj.w20data_set.order_by("id_w20_zone")
        return W20DataSerializer(w20data_set, many=True).data

    class Meta:
        model = models.W20
        fields = "__all__"
