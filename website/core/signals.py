#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
import logging

from django.contrib.admin.models import ADDITION, LogEntry
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_login_failed
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

log = logging.getLogger(__name__)


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    log.warning(
        "login failed for user {username}".format(username=credentials["username"])
    )


@receiver(post_save, sender=User)
def user_saved(instance, created, **kwargs):
    if created:
        log.warning(
            "user created: {username}".format(
                username=instance.username,
            )
        )
        LogEntry.objects.log_action(
            user_id=instance.pk,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.pk,
            action_flag=ADDITION,
            object_repr=instance.username,
            change_message="user created",
        )
