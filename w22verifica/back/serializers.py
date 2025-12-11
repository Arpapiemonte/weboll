#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from rest_framework import serializers

from w22verifica.back import models


class W22ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W22Zone
        fields = "__all__"


class W22VerificaDataSerializer(serializers.ModelSerializer):
    id_w22_zone = W22ZoneSerializer(many=False, read_only=True)

    class Meta:
        model = models.W22VerificaData
        fields = "__all__"


class W22VerificaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W22Verifica
        fields = "__all__"


class W22GiudizioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W22Giudizio
        fields = "__all__"


class W22SeveritaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W22Severita
        fields = "__all__"


class W22verificaCriticitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W22verificaCriticita
        fields = "__all__"


class W22VerificaSerializerFull(serializers.ModelSerializer):
    w22verificadata_set = serializers.SerializerMethodField()

    def get_w22verificadata_set(self, obj):
        w22verificadata_set = obj.w22verificadata_set.order_by("id_w22_zone")
        return W22VerificaDataSerializer(w22verificadata_set, many=True).data

    class Meta:
        model = models.W22Verifica
        fields = "__all__"
