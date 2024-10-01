#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#

from rest_framework import serializers

from w17.back import models
from website.core import models as models_w05


class W17BlobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W17Blob
        fields = "__all__"


class W17ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W17Classes
        fields = "__all__"


class W17DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W17Data
        fields = "__all__"


class W17Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W17
        fields = "__all__"


class W17SerializerFull(serializers.ModelSerializer):
    w17data_set = W17DataSerializer(many=True, read_only=True)
    w17classes_set = W17ClassesSerializer(many=True, read_only=True)
    w17blob_set = W17BlobSerializer(many=True, read_only=True)

    class Meta:
        model = models.W17
        fields = "__all__"


class StazioneMisuraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models_w05.StazioneMisura
        fields = "__all__"


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models_w05.Trend
        fields = "__all__"
