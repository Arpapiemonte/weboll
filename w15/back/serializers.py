#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from rest_framework import serializers

from w15.back import models


class W15DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W15Data
        fields = "__all__"


class W15Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W15
        fields = "__all__"


class W15SerializerFull(serializers.ModelSerializer):
    w15data_set = W15DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W15
        fields = "__all__"
