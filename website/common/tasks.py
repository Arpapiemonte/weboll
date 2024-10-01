#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
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
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db import connection

from config import celery_app
from w17.back.models import W17
from w26.back.models import W26
from website.core import models as W05
from website.core.models import Bulletins, Destinazioni

log = logging.getLogger(__name__)


def send_with_celery(prodotto, id, auto=False):
    """Send prodotto bulletin to all configured destinations"""
    my_date = datetime.datetime.today()
    if prodotto == "bis":
        w26 = W26.objects.get(pk=id)
        if w26 is not None:
            my_date = datetime.datetime.combine(
                w26.data_validita, datetime.datetime.min.time()
            )
    if prodotto == "analisi":
        w17 = W17.objects.get(pk=id)
        if w17 is not None:
            my_date = datetime.datetime.combine(
                w17.data_analysis, datetime.datetime.min.time()
            )
    to_send = 0
    if auto:
        destinations = (
            Destinazioni.objects.filter(prodotto=prodotto)
            .filter(enabled=True)
            .filter(auto=True)
        )
    else:
        destinations = Destinazioni.objects.filter(prodotto=prodotto).filter(
            enabled=True
        )
    for d in destinations:
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
        elif destinazione[:4] == "mail":
            # write to remote using mail
            send_bulletin_with_mail.delay(url=url, destinazione=destinazione)
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
    try:
        with requests.get(url) as r:
            r.raise_for_status()
            with open(destinazione, "wb") as f:
                f.write(r.content)
    except Exception as e:
        error = "send_bulletin_to_file failed %s" % e
        send_mail(url, destinazione, error)
        raise TaskFailure(error)
    return "ok"


class TaskFailure(Exception):
    pass


@celery_app.task
def send_bulletin_with_scp(url, destinazione, segreto):
    # username@host:/path/to#KexAlgorithms=+diffie-hellman-group1-sha1/HostKeyAlgorithms=+ssh-dss/Ciphers=+aes256-cbc
    # username@host:/path/to#HostKeyAlgorithms=+ssh-dss
    # username@host:/path/to
    print("========== send_bulletin_with_scp")
    ssh_options = ""
    ssh_command = destinazione
    if destinazione.__contains__("#"):
        ssh_options_list = destinazione.split("#")[1]
        if ssh_options_list.__contains__("/"):
            for ssh_option in ssh_options_list.split("/"):
                ssh_options = ssh_options + " -o " + ssh_option
        else:
            ssh_options = " -o " + ssh_options_list
        ssh_command = destinazione.split("#")[0]
    try:
        with requests.get(url) as r:
            r.raise_for_status()
            with tempfile.NamedTemporaryFile() as f:
                f.write(r.content)
                f.flush()
                command = (
                    'sshpass -p "%s" scp -o StrictHostKeyChecking=no %s "%s" "%s"'
                    % (
                        segreto,
                        ssh_options,
                        f.name,
                        ssh_command,
                    )
                )
                retcode = call(command, shell=True)
                if retcode != 0:
                    error = "scp nonzero return code = %d" % retcode
                    raise Exception(error)
    except Exception as e:
        error = "send_bulletin_with_scp failed %s" % e
        send_mail(url, destinazione, error)
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
    try:
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
                    error = "lftp nonzero return code = %d" % retcode
                    raise Exception(error)
    except Exception as e:
        error = "send_bulletin_with_ftp failed %s" % e
        send_mail(url, destinazione, error)
        raise TaskFailure(error)
    return "ok"


@celery_app.task
def send_bulletin_with_mail(url, destinazione):
    print("========== send_bulletin_with_mail ")
    my_date = datetime.datetime.today()
    # destinazione = mail://user@example.com/file_attach_name/subject/body
    email = destinazione.split("/")[2]
    file_attach_name = destinazione.split("/")[3]
    subject = destinazione.split("/")[4]
    subject = (
        subject.replace("{{id}}", str(id))
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
    body = destinazione.split("/")[5]
    body = (
        body.replace("{{id}}", str(id))
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
    # http://django:8000/w34/pdf/1
    bulletin = url.split("/")[3]
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[email],
        )
        with requests.get(url) as r:
            r.raise_for_status()
            email.attach(file_attach_name, r.content)
        if bulletin == "w34":
            # allega anche il bollettino meteo
            last_w05 = W05.W05.objects.filter(status="1").latest("pk")
            start_valid_time = last_w05.start_valid_time.strftime("%d%m%Y")
            with requests.get(
                "http://django:8000/w05/pdf/" + str(last_w05.id_w05)
            ) as r:
                r.raise_for_status()
                email.attach("bollettinoMeteo_" + start_valid_time + ".pdf", r.content)
        email.send()
    except Exception as e:
        error = "send_bulletin_with_mail failed %s" % e
        send_mail(url, destinazione, error)
        raise TaskFailure(error)
    return "ok"


def send_mail(url, destinazione, body):
    print("========== send_mail")
    try:
        email = EmailMultiAlternatives(
            "Weboll error",
            body + " " + url + " " + destinazione,
            settings.DEFAULT_FROM_EMAIL,
            [a[1] for a in settings.ADMINS],
        )
        email.send()
    except Exception as e:
        error = "send_mail failed %s" % e
        print(error)


@celery_app.task
def auto_create_and_send():
    """Create and send all automatic bulletins, if they are not yet sent today"""
    to_send = 0
    time_now = datetime.datetime.now()
    log.info("create and send at {time_now}".format(time_now=time_now.time()))
    login_url = "http://django:8000/token/"
    password = getenv("AUTO_PASSWORD", default="auto")
    with requests.post(login_url, json={"username": "auto", "password": password}) as r:
        r.raise_for_status()
        token = r.json()["access"]
    headers = {"Authorization": "Bearer %s" % token}
    for bulletin in Bulletins.objects.filter(
        time__gte=(time_now - datetime.timedelta(minutes=5)).time(),
        time__lte=(time_now + datetime.timedelta(minutes=5)).time(),
    ).filter(auto=True):
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


@celery_app.task
def auto_send_last_one():
    """send all automatic destinations with last bulletin"""
    to_send = 0
    time_now = datetime.datetime.now().time()
    log.info("send last one at {time_now}".format(time_now=time_now))
    login_url = "http://django:8000/token/"
    password = getenv("AUTO_PASSWORD", default="auto")
    with requests.post(login_url, json={"username": "auto", "password": password}) as r:
        r.raise_for_status()
        token = r.json()["access"]
    headers = {"Authorization": "Bearer %s" % token}
    for destinazione in Destinazioni.objects.filter(enabled=True).filter(auto=True):
        table = destinazione.prodotto.tabella
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_{} FROM {} WHERE status = '1' order by last_update desc limit 1".format(
                    table, table
                ),
            )
            row = cursor.fetchone()
        id = row[0]
        log.info(
            "-- automatic send last one for {bulletin}".format(
                bulletin=destinazione.prodotto
            )
        )
        url_send = "http://django:8000/%s/bulletins/%s/send_auto/" % (
            table,
            id,
        )
        with requests.get(url_send, headers=headers) as r:
            r.raise_for_status()
        to_send += 1
    return to_send
