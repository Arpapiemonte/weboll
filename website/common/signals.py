#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
import logging

from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

log = logging.getLogger(__name__)


def bulletin_saved(bulletin, instance, created, **kwargs):
    if created:
        message = "{bulletin} bulletin {pk} draft created".format(
            bulletin=bulletin,
            pk=instance.pk,
        )
        log.warning(message)
        LogEntry.objects.log_action(
            user_id=User.objects.get(username=instance.username).pk,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.pk,
            action_flag=ADDITION,
            object_repr=str(instance.pk),
            change_message=message,
        )
    else:
        if instance.status == "1":
            message = "{bulletin} bulletin {pk} sent".format(
                bulletin=bulletin,
                pk=instance.pk,
            )
        else:
            message = "{bulletin} bulletin {pk} saved".format(
                bulletin=bulletin,
                pk=instance.pk,
            )
        log.warning(message)
        LogEntry.objects.log_action(
            user_id=User.objects.get(username=instance.username).pk,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.pk,
            action_flag=CHANGE,
            object_repr=str(instance.pk),
            change_message=message,
        )


def bulletin_deleted(bulletin, instance, using, **kwargs):
    message = "{bulletin} bulletin {pk} draft deleted".format(
        bulletin=bulletin,
        pk=instance.pk,
    )
    log.warning(message)
    LogEntry.objects.log_action(
        user_id=User.objects.get(username=instance.username).pk,
        content_type_id=ContentType.objects.get_for_model(instance).pk,
        object_id=instance.pk,
        action_flag=ADDITION,
        object_repr=str(instance.pk),
        change_message=message,
    )
