#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from rest_framework import serializers

from w29.back import models


class W29ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W29Zone
        fields = "__all__"


class W29PericoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W29Pericolo
        fields = "__all__"


class W29ProbabilitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W29Probabilita
        fields = "__all__"


class W29DataSerializer(serializers.ModelSerializer):
    id_w29_zone = W29ZoneSerializer(many=False, read_only=True)

    class Meta:
        model = models.W29Data
        fields = "__all__"


class W29Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W29
        fields = "__all__"


class W29SerializerFull(serializers.ModelSerializer):
    w29data_set = serializers.SerializerMethodField()

    def get_w29data_set(self, obj):
        w29data_set = obj.w29data_set.order_by("id_w29_zone")
        return W29DataSerializer(w29data_set, many=True).data

    class Meta:
        model = models.W29
        fields = "__all__"
