#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from rest_framework import serializers

from w21.back import models


class W21DataSerializer(serializers.ModelSerializer):
    numeric_value = serializers.DecimalField(
        max_digits=7, decimal_places=2, coerce_to_string=False
    )

    class Meta:
        model = models.W21Data
        fields = "__all__"


class W21Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W21
        fields = "__all__"


class W21SerializerFull(serializers.ModelSerializer):
    w21data_set = W21DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W21
        fields = "__all__"
