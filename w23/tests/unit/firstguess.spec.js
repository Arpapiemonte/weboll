// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt

import Bulletin from '../../front/Bulletin.vue'

// assemble a fake Bulletin object to mimick the firstguess functionalities
// that need to be accessible to the function to be tested
let BulletinFirstGuess = {
  firstguess: Bulletin.methods.firstguess,
  min2: Bulletin.methods.min2,
  rischio_temporali: Bulletin.methods.rischio_temporali,
  rischio_valanghe: Bulletin.methods.rischio_temporali,
  arrayMin: Bulletin.methods.arrayMin,
  arrayMax: Bulletin.methods.arrayMax,
  vigilanza:{
    sintesi_meteo: "sintesi_meteo"
  },
  pericolo_da_indice: {
    1: {id_w23_pericolo: "BIANCO"},
    2: {id_w23_pericolo: "VERDE"},
    3: {id_w23_pericolo: "GIALLO"},
    4: {id_w23_pericolo: "ARANCIONE"},
    5: {id_w23_pericolo: "ROSSO"},
  },
  availability: {"risk_val_oggi":true,"risk_val_domani":true,"vigilanza":true,"psa":true,"pluvoss":true},
  allerta: {
    w23data_set: [
      {
        id_w23_zone: {
          nome_zona:"Piem-A"
        }
      },
    ]
  },
  piogge_massime:{
    125: {
      45: { "Piem-A": 0 },
      46: { "Piem-A": 0 },
      60: { "Piem-A": 0 },
      61: { "Piem-A": 0 },
      62: { "Piem-A": 0 },
      63: { "Piem-A": 0 },
      77: { "Piem-A": 0 },
      78: { "Piem-A": 0 },
      79: { "Piem-A": 0 },
      80: { "Piem-A": 0 },
    },
    126: {
      48: { "Piem-A": 0 },
      66: { "Piem-A": 0 },
    },
    127: {
      66: { "Piem-A": 0 },
    },
  },
  piogge_medie: {
    900: {
      45: { "Piem-A": 0 },
      46: { "Piem-A": 0 },
      60: { "Piem-A": 0 },
      61: { "Piem-A": 0 },
      62: { "Piem-A": 0 },
      63: { "Piem-A": 0 },
      77: { "Piem-A": 0 },
      78: { "Piem-A": 0 },
      79: { "Piem-A": 0 },
      80: { "Piem-A": 0 },
    },
    901: {
      1009: { "Piem-A": 0 },
      48: { "Piem-A": 0 },
      1011: { "Piem-A": 0 },
      64: { "Piem-A": 0 },
      1013: { "Piem-A": 0 },
      65: { "Piem-A": 0 },
      1015: { "Piem-A": 0 },
      81: { "Piem-A": 0 },
      1017: { "Piem-A": 0 },
      82: { "Piem-A": 0 },
    },
    902: {
      2006: { "Piem-A": 0 },
      49: { "Piem-A": 0 },
      2009: { "Piem-A": 0 },
      2010: { "Piem-A": 0 },
      2011: { "Piem-A": 0 },
      66: { "Piem-A": 0 },
      2014: { "Piem-A": 0 },
      2015: { "Piem-A": 0 },
      2016: { "Piem-A": 0 },
      83: { "Piem-A": 0 },
    },
    903: {
      3003: { "Piem-A": 0 },
      3004: { "Piem-A": 0 },
      3005: { "Piem-A": 0 },
      3006: { "Piem-A": 0 },
      3007: { "Piem-A": 0 },
      3008: { "Piem-A": 0 },
      3009: { "Piem-A": 0 },
      3010: { "Piem-A": 0 },
      3011: { "Piem-A": 0 },
      3012: { "Piem-A": 0 },
    }
  },
  setFirstGuess(zona, campo, indice) {
    const pericolo = this.pericolo_da_indice[indice]
    return [
      {"value_key":campo,"new_value": pericolo.id_w23_pericolo},
    ]
  },
  saveW23() { }, // dummy
  saveField() { } // dummy
}

describe('firstguess', () => {
  it('defaults to green', () => {
    let Green = {
      ...BulletinFirstGuess,
      rischio_neve(parametro, time_layout, area) {
        // parametro = SNOW_400, SNOW_700, SNOW_1000
        // time_layout = 48, 1009
        // area = Piem-A, Piem-B, ...
        // return value: 1, 2, 3, 4 or 5
        return 2
      },
      rischio_pioggia_max(aggregazione, time_layout, area) {
        // aggregazione = 125, 126, 127
        // time_layout = 45, 46 ...
        // area = Piem-A, Piem-B, ...
        // return value: 1, 2, 3, 4 or 5
        return 2
      },
      rischio_pioggia_avg(aggregazione, time_layout, area) {
        // aggregazione = 900, 901, 902, 903
        // time_layout = 45, 46 ...
        // area = Piem-A, Piem-B, ...
        // return value: 1, 2, 3, 4 or 5
        return 2
      },
      risk_storm_oggi: {"Piem-A": 2},
      risk_storm_domani: {"Piem-A": 2},
      risk_val_oggi: {"Piem-A":{ valore_originale :"2.000"}},
      risk_val_domani: {"Piem-A":{ valore_originale :"2.000"}}
    }
    const stack = Green.firstguess()
    const values = Bulletin.methods.rearrange(stack, 'value_key', arr => arr[0].new_value)
    expect(values.neve_oggi).toEqual('VERDE')
    expect(values.neve_domani).toEqual('VERDE')
    expect(values.idrogeologico_oggi).toEqual('VERDE')
    expect(values.idrogeologico_domani).toEqual('VERDE')
    expect(values.idraulico_oggi).toEqual('VERDE')
    expect(values.idraulico_domani).toEqual('VERDE')
    expect(values.temporali_oggi).toEqual('VERDE')
    expect(values.temporali_domani).toEqual('VERDE')
    expect(values.valanghe_oggi).toEqual('VERDE')
    expect(values.valanghe_domani).toEqual('VERDE')
  }),
  it('turns into yellow', () => {
    let Yellow = {
      ...BulletinFirstGuess,
      rischio_neve(parametro, time_layout, area) {
        // parametro = SNOW_400, SNOW_700, SNOW_1000
        // time_layout = 48, 1009
        // area = Piem-A, Piem-B, ...
        // return value: 1, 2, 3, 4 or 5
        return 3
      },
      rischio_pioggia_max(aggregazione, time_layout, area) {
        // aggregazione = 125, 126, 127
        // time_layout = 45, 46 ...
        // area = Piem-A, Piem-B, ...
        // return value: 1, 2, 3, 4 or 5
        return 3
      },
      rischio_pioggia_avg(aggregazione, time_layout, area) {
        // aggregazione = 900, 901, 902, 903
        // time_layout = 45, 46 ...
        // area = Piem-A, Piem-B, ...
        // return value: 1, 2, 3, 4 or 5
        return 3
      },
      risk_storm_oggi: {"Piem-A": 3},
      risk_storm_domani: {"Piem-A": 3},
      risk_val_oggi: {"Piem-A":{ valore_originale :"3.000"}},
      risk_val_domani: {"Piem-A":{ valore_originale :"3.000"}}
    }
    const stack = Yellow.firstguess()
    const values = Bulletin.methods.rearrange(stack, 'value_key', arr => arr[0].new_value)
    expect(values.neve_oggi).toEqual('GIALLO')
    expect(values.neve_domani).toEqual('GIALLO')
    expect(values.idrogeologico_oggi).toEqual('GIALLO')
    expect(values.idrogeologico_domani).toEqual('GIALLO')
    expect(values.idraulico_oggi).toEqual('GIALLO')
    expect(values.idraulico_domani).toEqual('GIALLO')
    expect(values.temporali_oggi).toEqual('GIALLO')
    expect(values.temporali_domani).toEqual('GIALLO')
    expect(values.valanghe_oggi).toEqual('GIALLO')
    expect(values.valanghe_domani).toEqual('GIALLO')
  }),
  it('turns into orange', () => {
    let Orange = {
      ...BulletinFirstGuess,
      rischio_neve(parametro, time_layout, area) {
        // parametro = SNOW_400, SNOW_700, SNOW_1000
        // time_layout = 48, 1009
        // area = Piem-A, Piem-B, ...
        // return value: 1, 2, 3, 4 or 5
        return 4
      },
      rischio_pioggia_max(aggregazione, time_layout, area) {
        // aggregazione = 125, 126, 127
        // time_layout = 45, 46 ...
        // area = Piem-A, Piem-B, ...
        // return value: 1, 2, 3, 4 or 5
        return 4
      },
      rischio_pioggia_avg(aggregazione, time_layout, area) {
        // aggregazione = 900, 901, 902, 903
        // time_layout = 45, 46 ...
        // area = Piem-A, Piem-B, ...
        // return value: 1, 2, 3, 4 or 5
        return 4
      },
      risk_storm_oggi: {"Piem-A": 4},
      risk_storm_domani: {"Piem-A": 4},
      risk_val_oggi: {"Piem-A":{ valore_originale :"4.000"}},
      risk_val_domani: {"Piem-A":{ valore_originale :"4.000"}}
    }
    const stack = Orange.firstguess()
    const values = Bulletin.methods.rearrange(stack, 'value_key', arr => arr[0].new_value)
    expect(values.neve_oggi).toEqual('ARANCIONE')
    expect(values.neve_domani).toEqual('ARANCIONE')
    expect(values.idrogeologico_oggi).toEqual('ARANCIONE')
    expect(values.idrogeologico_domani).toEqual('ARANCIONE')
    expect(values.idraulico_oggi).toEqual('ARANCIONE')
    expect(values.idraulico_domani).toEqual('ARANCIONE')
    expect(values.temporali_oggi).toEqual('ARANCIONE')
    expect(values.temporali_domani).toEqual('ARANCIONE')
    expect(values.valanghe_oggi).toEqual('ARANCIONE')
    expect(values.valanghe_domani).toEqual('ARANCIONE')
  }),
  it('turns into red', () => {
    let Red = {
      ...BulletinFirstGuess,
      rischio_neve(parametro, time_layout, area) {
        // parametro = SNOW_400, SNOW_700, SNOW_1000
        // time_layout = 48, 1009
        // area = Piem-A, Piem-B, ...
        // return value: 1, 2, 3, 4 or 5
        return 5
      },
      rischio_pioggia_max(aggregazione, time_layout, area) {
        // aggregazione = 125, 126, 127
        // time_layout = 45, 46 ...
        // area = Piem-A, Piem-B, ...
        // return value: 1, 2, 3, 4 or 5
        return 5
      },
      rischio_pioggia_avg(aggregazione, time_layout, area) {
        // aggregazione = 900, 901, 902, 903
        // time_layout = 45, 46 ...
        // area = Piem-A, Piem-B, ...
        // return value: 1, 2, 3, 4 or 5
        return 5
      },
      risk_storm_oggi: {"Piem-A": 4},
      risk_storm_domani: {"Piem-A": 4},
      risk_val_oggi: {"Piem-A":{ valore_originale :"4.000"}},
      risk_val_domani: {"Piem-A":{ valore_originale :"4.000"}}
    }
    const stack = Red.firstguess()
    const values = Bulletin.methods.rearrange(stack, 'value_key', arr => arr[0].new_value)
    expect(values.neve_oggi).toEqual('ROSSO')
    expect(values.neve_domani).toEqual('ROSSO')
    expect(values.idrogeologico_oggi).toEqual('ROSSO')
    expect(values.idrogeologico_domani).toEqual('ROSSO')
    expect(values.idraulico_oggi).toEqual('ROSSO')
    expect(values.idraulico_domani).toEqual('ROSSO')
    expect(values.temporali_oggi).toEqual('ARANCIONE')
    expect(values.temporali_domani).toEqual('ARANCIONE')
    expect(values.valanghe_oggi).toEqual('ARANCIONE')
    expect(values.valanghe_domani).toEqual('ARANCIONE')
  })
})
