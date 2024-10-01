#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
import logging

from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.urls import include, path
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import routers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from website.common.views import VersionView

log = logging.getLogger(__name__)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # https://stackoverflow.com/a/55859751
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)  # type: ignore
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)  # type: ignore

        # Add extra responses here
        data["username"] = self.user.username  # type: ignore
        data["groups"] = self.user.groups.values_list("name", flat=True)  # type: ignore

        log.warning("login {username}".format(username=self.user.username))  # type: ignore
        LogEntry.objects.log_action(
            user_id=self.user.pk,  # type: ignore
            content_type_id=ContentType.objects.get_for_model(self.user).pk,  # type: ignore
            object_id=self.user.pk,  # type: ignore
            action_flag=CHANGE,
            object_repr=self.user.username,  # type: ignore
            change_message="login",
        )

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer  # type: ignore


router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("version", VersionView.as_view()),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "token/",
        ensure_csrf_cookie(MyTokenObtainPairView.as_view()),
        name="token_obtain_pair",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
