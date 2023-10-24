#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from rest_framework import serializers

from w06.back import models


class W06DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W06Data
        fields = "__all__"


class W06Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W06
        fields = "__all__"


class W06SerializerFull(serializers.ModelSerializer):
    w06data_set = W06DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W06
        fields = "__all__"
