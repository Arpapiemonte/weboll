#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

import website.common.signals as common_signals
from w17verifica.back.models import w17_verifica

log = logging.getLogger(__name__)


@receiver(post_save, sender=w17_verifica)
def bulletin_saved(instance, created, **kwargs):
    common_signals.bulletin_saved("verificameteo", instance, created, **kwargs)


@receiver(post_delete, sender=w17_verifica)
def bulletin_deleted(instance, using, **kwargs):
    common_signals.bulletin_deleted("verificameteo", instance, using, **kwargs)
