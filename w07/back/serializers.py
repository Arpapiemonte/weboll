#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from rest_framework import serializers

from w07.back import models


class W07DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W07Data
        fields = "__all__"


class W07Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W07
        fields = "__all__"


class W07SerializerFull(serializers.ModelSerializer):
    w07data_set = W07DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W07
        fields = "__all__"
