// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
export const configCaldo = {
    variabili: [
        {"label": "Tmax","parametro": "TERMA", "aggregazione": 328},
        {"label": "ATmax","parametro": "ATMAX", "aggregazione": 0},
        {"label": "Tmin","parametro": "TERMA", "aggregazione": 327},
        {"label": "ATmin","parametro": "ATMIN", "aggregazione": 0},
    ],
    percentili: [
        {"label": "ATmax75p","parametro": "ATMAX", "aggregazione": 940},
        {"label": "ATmin75p","parametro": "ATMIN", "aggregazione": 940},
        {"label": "ATmax90p","parametro": "ATMAX", "aggregazione": 941},
        {"label": "ATmin90p","parametro": "ATMIN", "aggregazione": 941},
        {"label": "ATmax95p","parametro": "ATMAX", "aggregazione": 942},
        {"label": "ATmin95p","parametro": "ATMIN", "aggregazione": 942}
    ],
    wda: [
        {"label": "WDA75p", "aggregazione": 940},
        {"label": "WDA90p", "aggregazione": 941},
        {"label": "WDA95p", "aggregazione": 942}
    ],
    temperature_torino: [
        {"parametro": "TERMA", "aggregazione": 328},
        {"parametro": "ATMAX", "aggregazione": 0},
        {"parametro": "TERMA", "aggregazione": 327},
        {"parametro": "ATMIN", "aggregazione": 0}
    ],
    param_equazione: [
        {"id": "D0", "label": "GG cons oggi", "parametro": "GGCONS", "aggregazione": 0},
        {"id": "D1", "label": "GG cons ieri", "parametro": "GGCONS", "aggregazione": 0},
        {"id": "D2", "label": "GG cons altroieri", "parametro": "GGCONS", "aggregazione": 0},
        {"id": "D0", "label": "ATmin oggi", "parametro": "ATMIN", "aggregazione": 0},
        {"id": "D1", "label": "ATmin ieri", "parametro": "ATMIN", "aggregazione": 0},
        {"id": "D2", "label": "ATmin altroieri", "parametro": "ATMIN", "aggregazione": 0},

    ]
}