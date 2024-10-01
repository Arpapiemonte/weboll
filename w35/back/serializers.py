#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from rest_framework import serializers

from w35.back import models


class W35DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W35Data
        fields = "__all__"


class W35Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W35
        fields = "__all__"


class W35SerializerFull(serializers.ModelSerializer):
    w35data_set = W35DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.W35
        fields = "__all__"


class AreeMeteoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AreeMeteo
        fields = "__all__"


class ForecastValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForecastValues
        fields = "__all__"


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DjangoCeleryResultsTaskresult
        fields = "__all__"


class ForecastComuniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForecastComuni
        fields = "__all__"
