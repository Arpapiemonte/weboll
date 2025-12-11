#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from rest_framework import serializers

from w36.back import models


class W36DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W36Data
        fields = "__all__"


class W36Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W36
        fields = "__all__"


class W36SerializerFull(serializers.ModelSerializer):
    w36data_set = W36DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W36
        fields = "__all__"


class W36ParametriEquazioneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W36ParametriEquazione
        fields = "__all__"
