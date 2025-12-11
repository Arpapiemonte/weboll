#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from rest_framework import serializers

from w33.back import models


class W33DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W33Data
        fields = "__all__"


class W33Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W33
        fields = "__all__"


class W33SerializerFull(serializers.ModelSerializer):
    w33data_set = W33DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W33
        fields = "__all__"
