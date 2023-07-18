#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from rest_framework import serializers

from w26.back import models


class W26ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W26Zone
        fields = "__all__"


class W26DataSerializer(serializers.ModelSerializer):
    id_w26_zone = W26ZoneSerializer(many=False, read_only=True)

    class Meta:
        model = models.W26Data
        fields = "__all__"


class W26Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W26
        fields = "__all__"


class W26SerializerFull(serializers.ModelSerializer):
    w26data_set = serializers.SerializerMethodField()

    def get_w26data_set(self, obj):
        w26data_set = obj.w26data_set.order_by("id_w26_zone")
        return W26DataSerializer(w26data_set, many=True).data

    class Meta:
        model = models.W26
        fields = "__all__"


class BisBollettinoWebolimpiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BisBollettinoWebolimpia
        fields = "__all__"
