#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#

from rest_framework import serializers

from w17verifica.back import models


class W17verificaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.w17_verifica_data
        fields = "__all__"


class W17verificaMassimaliSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.w17_verifica_massimali
        fields = "__all__"


class W17verificaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.w17_verifica
        fields = "__all__"


class W17verificaSerializerFull(serializers.ModelSerializer):
    w17_verifica_data_set = W17verificaDataSerializer(many=True, read_only=True)

    class Meta:
        model = models.w17_verifica
        fields = "__all__"
