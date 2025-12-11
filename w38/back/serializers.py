#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from rest_framework import serializers

from w38.back import models


class W38DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W38Data
        fields = "__all__"


class W38Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W38
        fields = "__all__"


class W38SerializerFull(serializers.ModelSerializer):
    w38data_set = W38DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W38
        fields = "__all__"


class W38DatiIvreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W38DatiIvrea
        fields = "__all__"
