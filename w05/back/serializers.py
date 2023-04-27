#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from rest_framework import serializers

from website.core import models


class SkyConditionClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SkyConditionClasses
        fields = ["id_parametro", "ordinamento"]


class SkyConditionSerializer(serializers.ModelSerializer):
    classes = SkyConditionClassesSerializer(many=True)

    class Meta:
        model = models.SkyCondition
        fields = [
            "id_sky_condition",
            "sky_condition",
            "description",
            "description_ita",
            "classes",
        ]


class W05DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W05Data
        fields = "__all__"


class W05ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W05Classes
        fields = "__all__"


class ClassesValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClassesValue
        fields = ["id_classes_value", "description"]


class ClassesSerializer(serializers.ModelSerializer):
    classes_value = ClassesValueSerializer(many=True, read_only=True)
    # classes_value = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Classes
        fields = ["id_classes", "id_parametro", "description", "classes_value"]


class W05Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W05
        fields = "__all__"


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Venue
        fields = "__all__"


class W05SerializerFull(serializers.ModelSerializer):
    w05data_set = W05DataSerializer(many=True, read_only=True)
    w05classes_set = W05ClassesSerializer(many=True, read_only=True)

    class Meta:
        model = models.W05
        fields = "__all__"
