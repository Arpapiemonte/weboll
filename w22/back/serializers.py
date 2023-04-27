#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from rest_framework import serializers

from w22.back import models


class W22ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W22Zone
        fields = "__all__"


class W22DataSerializer(serializers.ModelSerializer):
    id_w22_zone = W22ZoneSerializer(many=False, read_only=True)

    class Meta:
        model = models.W22Data
        fields = "__all__"


class W22Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W22
        fields = "__all__"


class W22TendenzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W22Tendenza
        fields = "__all__"


class W22CriticitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W22Criticita
        fields = "__all__"


class W22SerializerFull(serializers.ModelSerializer):
    w22data_set = serializers.SerializerMethodField()

    def get_w22data_set(self, obj):
        w22data_set = obj.w22data_set.order_by("id_w22_zone")
        return W22DataSerializer(w22data_set, many=True).data

    class Meta:
        model = models.W22
        fields = "__all__"
