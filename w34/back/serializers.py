#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from rest_framework import serializers

from w34.back import models


class W34DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W34Data
        fields = "__all__"


class W34Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W34
        fields = "__all__"


class W34SerializerFull(serializers.ModelSerializer):
    w34data_set = W34DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W34
        fields = "__all__"
