import datetime
import json

import pytest

from website.core.models import W05

pytestmark = pytest.mark.django_db


def test_timesensitive(freeze):
    FAKE_TIME = datetime.datetime(2021, 7, 21, 12, 00, 00)
    freeze.freeze(FAKE_TIME)
    assert datetime.datetime.now() == FAKE_TIME


class TestBullettinsEndpoints:

    endpoint = "/w05/bulletins/"
    endpoint_new = "/w05/bulletins/new/"

    def test_list(self, api_client):

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    def test_full_new_bulletin_authorized(self, api_client, freeze):

        c = api_client()

        # numero bolletino esistenti

        tot = W05.objects.all().count()

        # login

        c.login(username="aliccoop", password="mypass")

        # creazione bolletino

        response = c.get(self.endpoint_new)

        assert response.status_code == 200

        data = json.loads(response.content)

        assert len(data) == 1

        # confronto numero di bolletini

        assert W05.objects.all().count() == tot + 1

        # rimozione nuovo bolletino

        url = f'{self.endpoint}{data["id_w05"]}/'

        response = c.delete(url)

        assert response.status_code == 204

        # confronto numero di bolletini

        assert W05.objects.all().count() == tot

    def test_new_bulletin_unauthorized(self, api_client):

        c = api_client()

        response = c.get(self.endpoint_new)

        assert response.status_code == 403

    def test_delete_new_bulletin_unauthorized(self, api_client, freeze):

        c = api_client()

        # login

        c.login(username="aliccoop", password="mypass")

        # new bulletin

        response = c.get(self.endpoint_new)

        data = json.loads(response.content)

        # logout

        c.logout()

        # rimozione nuovo bolletino in bozza da utente non autentificato

        url = f'{self.endpoint}{data["id_w05"]}/'

        response = c.delete(url)

        assert response.status_code == 403

        # login e per cancellare il bolletino in bozza

        c.login(username="aliccoop", password="mypass")

        url = f'{self.endpoint}{data["id_w05"]}/'

        response = c.delete(url)

        assert response.status_code == 204

    def test_delete_sent_bulletin_unauthorized(self, api_client):

        c = api_client()

        # estrazione del più recente bolletino inviato (status=1)

        var = W05.objects.filter(status=1)
        my_sent_bulletin = var[0].id_w05

        url = f"{self.endpoint}{my_sent_bulletin}/"

        response = c.delete(url)

        assert response.status_code == 403

    """

    # ASPETTARE CHE VENGA CORRETTO IL CODICE
    def test_delete_sent_bulletin(self, api_client):

        c = api_client()

        #login

        c.login(username='aliccoop', password='mypass')

        #estrazione del più recente bolletino inviato (status=1)

        var = W05.objects.filter(status = 1)
        my_sent_bulletin = var[0].id_w05

        url = f'{self.endpoint}{my_sent_bulletin}/'

        response = c.delete(url)

        assert response.status_code == 403
    """
