#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from rest_framework import serializers

from w32.back import models


class W32ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W32Zone
        fields = "__all__"


class W32MbaciniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W32Mbacini
        fields = "__all__"


class W32PericoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W32Pericolo
        fields = "__all__"


class W32PericolombaciniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W32Pericolombacini
        fields = "__all__"


class W32DataSerializer(serializers.ModelSerializer):
    id_w32_zone = W32ZoneSerializer(many=False, read_only=True)

    class Meta:
        model = models.W32Data
        fields = "__all__"


class W32MbaciniDataSerializer(serializers.ModelSerializer):
    id_w32_mbacini = W32MbaciniSerializer(many=False, read_only=True)

    class Meta:
        model = models.W32MbaciniData
        fields = "__all__"


class W32Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W32
        fields = "__all__"


class W32SerializerFull(serializers.ModelSerializer):
    w32data_set = serializers.SerializerMethodField()
    w32mbacinidata_set = serializers.SerializerMethodField()

    def get_w32data_set(self, obj):
        w32data_set = obj.w32data_set.order_by("id_w32_zone")
        return W32DataSerializer(w32data_set, many=True).data

    def get_w32mbacinidata_set(self, obj):
        w32mbacinidata_set = obj.w32mbacinidata_set.order_by("id_w32_mbacini")
        return W32MbaciniDataSerializer(w32mbacinidata_set, many=True).data

    class Meta:
        model = models.W32
        fields = "__all__"
