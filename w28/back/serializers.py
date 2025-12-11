#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from rest_framework import serializers

from w28.back import models


class W28DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W28Data
        fields = "__all__"


class W28Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W28
        fields = "__all__"


class W28SerializerFull(serializers.ModelSerializer):
    w28data_set = W28DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W28
        fields = "__all__"
