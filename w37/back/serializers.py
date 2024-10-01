#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from rest_framework import serializers

from w37.back import models


class W37DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W37Data
        fields = "__all__"


class W37Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W37
        fields = "__all__"


class W37SerializerFull(serializers.ModelSerializer):
    w37data_set = W37DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W37
        fields = "__all__"
