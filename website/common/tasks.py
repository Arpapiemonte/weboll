#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
import datetime
import logging
import tempfile
from os import getenv
from subprocess import call

import requests
from django.db import connection

from config import celery_app
from w26.back.models import W26
from website.core.models import Bulletins, Destinazioni

log = logging.getLogger(__name__)


def send_with_celery(prodotto, id):
    """Send prodotto bulletin to all configured destinations"""
    my_date = datetime.datetime.today()
    if prodotto == "bis":
        w26 = W26.objects.get(pk=id)
        if w26 is not None:
            my_date = datetime.datetime.combine(
                w26.data_validita, datetime.datetime.min.time()
            )
    to_send = 0
    for d in Destinazioni.objects.filter(prodotto=prodotto).filter(enabled=True):
        url = "http://django:8000" + d.endpoint.replace("{{id}}", str(id))
        destinazione = (
            d.destinazione.replace("{{id}}", str(id))
            .replace("{{year}}", str(my_date.year))
            .replace("{{month}}", str(my_date.month).zfill(2))
            .replace("{{day}}", str(my_date.day).zfill(2))
            .replace(
                "{{time}}",
                str(my_date.hour).zfill(2)
                + str(my_date.minute).zfill(2)
                + str(my_date.second).zfill(2),
            )
        )
        if destinazione[0] == "/":
            # write to local filesystem (i.e. inside the django container)
            send_bulletin_to_file.delay(url=url, destinazione=destinazione)
        elif destinazione[:3] == "ftp":
            # write to remote using ftp
            send_bulletin_with_ftp.delay(
                url=url, destinazione=destinazione, segreto=d.segreto
            )
        else:
            # write to remote using scp
            send_bulletin_with_scp.delay(
                url=url, destinazione=destinazione, segreto=d.segreto
            )
        to_send += 1
    return to_send


@celery_app.task
def send_bulletin_to_file(url, destinazione):
    print("========== send_bulletin_to_file")
    with requests.get(url) as r:
        r.raise_for_status()
        with open(destinazione, "wb") as f:
            f.write(r.content)
    return "ok"


class TaskFailure(Exception):
    pass


@celery_app.task
def send_bulletin_with_scp(url, destinazione, segreto):
    print("========== send_bulletin_with_scp")
    with requests.get(url) as r:
        r.raise_for_status()
        with tempfile.NamedTemporaryFile() as f:
            f.write(r.content)
            f.flush()
            command = 'sshpass -p "%s" scp -o StrictHostKeyChecking=no "%s" "%s"' % (
                segreto,
                f.name,
                destinazione,
            )
            retcode = call(command, shell=True)
            if retcode != 0:
                error = "scp failed with code: %d" % retcode
                raise TaskFailure(error)
    return "ok"


@celery_app.task
def send_bulletin_with_ftp(url, destinazione, segreto):
    print("========== send_bulletin_with_ftp")
    # destinazione = ftp://user@servername.example.com:9999/path/to/qqq.pdf
    protocol = destinazione.split("/")[0]  # ftp:
    remote_filename = destinazione.split("/")[-1]  # qqq.pdf
    remote_path = "/" + "/".join(destinazione.split("/")[3:-1])  # /path/to
    username = destinazione.split("/")[2].split("@")[0]  # user
    host = destinazione.split("/")[2].split("@")[1]  # servername.example.com:9999
    with requests.get(url) as r:
        r.raise_for_status()
        with tempfile.NamedTemporaryFile() as f:
            f.write(r.content)
            f.flush()
            command = [
                "lftp",
                "-u",
                "%s:%s" % (username, segreto),
                "%s//%s" % (protocol, host),
                "-e",
                "put %s -o %s/%s; exit" % (f.name, remote_path, remote_filename),
            ]
            retcode = call(command)
            if retcode != 0:
                error = "lftp failed with code: %d" % retcode
                raise TaskFailure(error)
    return "ok"


@celery_app.task
def auto_create_and_send():
    """Create and send all automatic bulletins, if they are not yet sent today"""
    to_send = 0
    time_now = datetime.datetime.now().time()
    log.info("create and send at {time_now}".format(time_now=time_now))
    login_url = "http://django:8000/token/"
    password = getenv("AUTO_PASSWORD", default="auto")
    with requests.post(login_url, json={"username": "auto", "password": password}) as r:
        r.raise_for_status()
        token = r.json()["access"]
    headers = {"Authorization": "Bearer %s" % token}
    for bulletin in Bulletins.objects.filter(time__lte=time_now).filter(auto=True):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM {} WHERE start_valid_time::DATE = NOW()::DATE AND status = '1'".format(
                    bulletin.tabella
                ),
            )
            row = cursor.fetchone()
        count = row[0]
        if count == 0:
            log.info(
                "-- automatic create and send for {bulletin}".format(bulletin=bulletin)
            )
            url_new = "http://django:8000/%s/bulletins/new/" % bulletin.tabella
            with requests.get(url_new, headers=headers) as r:
                r.raise_for_status()
                id = r.json()["id_%s" % bulletin.tabella]
            url_send = "http://django:8000/%s/bulletins/%s/send/" % (
                bulletin.tabella,
                id,
            )
            with requests.get(url_send, headers=headers) as r:
                r.raise_for_status()
            to_send += 1
    return to_send
