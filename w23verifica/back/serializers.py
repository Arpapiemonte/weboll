#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from rest_framework import serializers

from w23verifica.back import models


class W23ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W23Zone
        fields = "__all__"


class W23VerificaDataSerializer(serializers.ModelSerializer):
    id_w23_zone = W23ZoneSerializer(many=False, read_only=True)

    class Meta:
        model = models.W23VerificaData
        fields = "__all__"


class W23VerificaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W23Verifica
        fields = "__all__"


class W23GiudizioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W23Giudizio
        fields = "__all__"


class W23SeveritaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W23Severita
        fields = "__all__"


class W23verificaCriticitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W23verificaCriticita
        fields = "__all__"


class W23VerificaSerializerFull(serializers.ModelSerializer):
    w23verificadata_set = serializers.SerializerMethodField()

    def get_w23verificadata_set(self, obj):
        w23verificadata_set = obj.w23verificadata_set.order_by("id_w23_zone")
        return W23VerificaDataSerializer(w23verificadata_set, many=True).data

    class Meta:
        model = models.W23Verifica
        fields = "__all__"
