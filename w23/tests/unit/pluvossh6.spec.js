// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt

import Bulletin from '../../front/Bulletin.vue'

// assemble a fake Bulletin object to mimick the pluvossh6 functionalities
// that need to be accessible to the function to be tested
let BulletinFirstGuess = {
  rearrange: Bulletin.methods.rearrange,
  add: Bulletin.methods.add,
  subtractHours: Bulletin.methods.subtractHours,
  pluvoss: Bulletin.methods.pluvoss,
  pluvoss_available: Bulletin.methods.pluvoss_available,
  allerta: {
    data_emissione: "2023-01-26",
  },
}

describe('pluvossh6', () => {
  it('defaults to empty', () => {
    let Empty = {
      ...BulletinFirstGuess,
      pluvossh6_from_db: [
        {
          "data": "2023-01-24",
          "ora": "18:00:00",
          "area": "Piem-A",
          "valore": "0"
        },      
      ]
    }
    expect(Empty.pluvoss(Empty.pluvossh6_from_db)).toEqual({ 'Piem-A': { null: '0' } })
    expect(Empty.pluvoss_available(Empty.pluvoss(Empty.pluvossh6_from_db))).toEqual(false)
  })
})

describe('pluvossh6', () => {
  it('match tl 12', () => {
    let Empty = {
      ...BulletinFirstGuess,
      pluvossh6_from_db: [
        {
          "data": "2023-01-25",
          "ora": "00:00:00",
          "area": "Piem-A",
          "valore": "100"
        },      
      ]
    }
    expect(Empty.pluvoss(Empty.pluvossh6_from_db)).toEqual({ 'Piem-A': { "12": "100" } })
    expect(Empty.pluvoss_available(Empty.pluvoss(Empty.pluvossh6_from_db))).toEqual(true)
  })
})

describe('pluvossh6', () => {
  it('match tl 26', () => {
    let Empty = {
      ...BulletinFirstGuess,
      pluvossh6_from_db: [
        {
          "data": "2023-01-25",
          "ora": "06:00:00",
          "area": "Piem-A",
          "valore": "200"
        },      
      ]
    }
    expect(Empty.pluvoss(Empty.pluvossh6_from_db)).toEqual({ 'Piem-A': { "26": "200" } })
    expect(Empty.pluvoss_available(Empty.pluvoss(Empty.pluvossh6_from_db))).toEqual(true)
  })
})

describe('pluvossh6', () => {
  it('match tl 27', () => {
    let Empty = {
      ...BulletinFirstGuess,
      pluvossh6_from_db: [
        {
          "data": "2023-01-25",
          "ora": "12:00:00",
          "area": "Piem-A",
          "valore": "300"
        },      
      ]
    }
    expect(Empty.pluvoss(Empty.pluvossh6_from_db)).toEqual({ 'Piem-A': { "27": "300" } })
    expect(Empty.pluvoss_available(Empty.pluvoss(Empty.pluvossh6_from_db))).toEqual(true)
  })
})

describe('pluvossh6', () => {
  it('match tl 28', () => {
    let Empty = {
      ...BulletinFirstGuess,
      pluvossh6_from_db: [
        {
          "data": "2023-01-25",
          "ora": "18:00:00",
          "area": "Piem-A",
          "valore": "400"
        },      
      ]
    }
    expect(Empty.pluvoss(Empty.pluvossh6_from_db)).toEqual({ 'Piem-A': { "28": "400" } })
    expect(Empty.pluvoss_available(Empty.pluvoss(Empty.pluvossh6_from_db))).toEqual(true)
  })
})

describe('pluvossh6', () => {
  it('match tl 29', () => {
    let Empty = {
      ...BulletinFirstGuess,
      pluvossh6_from_db: [
        {
          "data": "2023-01-26",
          "ora": "00:00:00",
          "area": "Piem-A",
          "valore": "500"
        },      
      ]
    }
    expect(Empty.pluvoss(Empty.pluvossh6_from_db)).toEqual({ 'Piem-A': { "29": "500" } })
    expect(Empty.pluvoss_available(Empty.pluvoss(Empty.pluvossh6_from_db))).toEqual(true)
  })
})

describe('pluvossh6', () => {
  it('match tl 43', () => {
    let Empty = {
      ...BulletinFirstGuess,
      pluvossh6_from_db: [
        {
          "data": "2023-01-26",
          "ora": "06:00:00",
          "area": "Piem-A",
          "valore": "600"
        },      
      ]
    }
    expect(Empty.pluvoss(Empty.pluvossh6_from_db)).toEqual({ 'Piem-A': { "43": "600" } })
    expect(Empty.pluvoss_available(Empty.pluvoss(Empty.pluvossh6_from_db))).toEqual(true)
  })
})

describe('pluvossh6', () => {
  it('match tl 44, 45 and 46', () => {
    let Empty = {
      ...BulletinFirstGuess,
      pluvossh6_from_db: [
        {
          "data": "2023-01-26",
          "ora": "12:00:00",
          "area": "Piem-A",
          "valore": "700"
        },
        {
          "data": "2023-01-26",
          "ora": "18:00:00",
          "area": "Piem-A",
          "valore": "800"
        },
        {
          "data": "2023-01-27",
          "ora": "00:00:00",
          "area": "Piem-A",
          "valore": "900"
        },
      ]
    }
    expect(Empty.pluvoss(Empty.pluvossh6_from_db)).toEqual({ 'Piem-A': { "44": "700", "45": "800", "46": "900" } })
    expect(Empty.pluvoss_available(Empty.pluvoss(Empty.pluvossh6_from_db))).toEqual(true)
  })
})
