#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from rest_framework import serializers

from w12.back import models


class W12DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W12Data
        fields = "__all__"


class W12Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W12
        fields = "__all__"


class W12SerializerFull(serializers.ModelSerializer):
    w12data_set = W12DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W12
        fields = "__all__"
