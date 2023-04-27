#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#

# import datetime

from rest_framework import serializers

from w31.back import models


class W31LivelliSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W31Livelli
        fields = "__all__"


class W31MicroareeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W31Microaree
        fields = "__all__"


class W31DataMicroareeParametriSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W31DataMicroareeParametri
        fields = "__all__"


class W31DataMicroareeLivelliSerializer(serializers.ModelSerializer):
    w31datamicroareeparametri_set = W31DataMicroareeParametriSerializer(
        many=True, read_only=True
    )
    id_w31_microaree = W31MicroareeSerializer()

    class Meta:
        model = models.W31DataMicroareeLivelli
        fields = "__all__"


class W31MacroareeInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W31MacroareeInput
        fields = "__all__"


class W31MacroareeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.W31Macroaree
        fields = "__all__"


class W31DataMacroareeLivelliSerializer(serializers.ModelSerializer):
    id_w31_macroaree = W31MacroareeSerializer()

    class Meta:
        model = models.W31DataMacroareeLivelli
        fields = "__all__"


class W31Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.W31
        fields = "__all__"


class W31SerializerFull(serializers.ModelSerializer):
    w31datamicroareelivelli_set = serializers.SerializerMethodField()
    w31datamacroareelivelli_set = serializers.SerializerMethodField()

    def get_w31datamicroareelivelli_set(self, obj):
        w31datamicroareelivelli_set = obj.w31datamicroareelivelli_set.order_by(
            "id_time_layouts", "id_w31_microaree"
        )
        return W31DataMicroareeLivelliSerializer(
            w31datamicroareelivelli_set, many=True
        ).data

    def get_w31datamacroareelivelli_set(self, obj):
        w31datamacroareelivelli_set = obj.w31datamacroareelivelli_set.order_by(
            "id_time_layouts", "id_w31_macroaree"
        )
        return W31DataMacroareeLivelliSerializer(
            w31datamacroareelivelli_set, many=True
        ).data

    class Meta:
        model = models.W31
        fields = "__all__"
