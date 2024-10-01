// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt

import Bulletin from '../../front/Bulletin.vue'

// assemble a fake Bulletin object to mimick the min2 functionalities
// that need to be accessible to the function to be tested
let MyBulletin = {
  firstguess: Bulletin.methods.firstguess,
  min2: Bulletin.methods.min2,
  arrayMin: Bulletin.methods.arrayMin,
  arrayMax: Bulletin.methods.arrayMax,
}

// 1: BIANCO
// 2: VERDE
// 3: GIALLO
// 4: ARANCIONE
// 5: ROSSO

describe('min2', () => {
  it('Oggi massime - giallo almeno un piemontino 6h e giallo il piemonte 12h allora giallo su Idrogeologico Oggi', () => {
    const result = MyBulletin.min2([3, 3])
    expect(result).toEqual(3)
  })
  it('Oggi massime - giallo almeno un piemontino 6h e Rosso il piemonte 12h allora giallo su Idrogeologico Oggi', () => {
    const result = MyBulletin.min2([3, 5])
    expect(result).toEqual(3)
  })
  it('Domani massime - giallo almeno un piemontino 6h e giallo il piemonte 12h allora giallo su Idrogeologico Domani', () => {
    const result = MyBulletin.min2([3, 3, 2])
    expect(result).toEqual(3)
  })
  it('Domani massime - giallo almeno un piemontino 6h e Rosso il piemonte 12h allora giallo su Idrogeologico Domani', () => {
    const result = MyBulletin.min2([3, 2, 5])
    expect(result).toEqual(3)
  })
  it('Domani massime - giallo almeno un piemonte 24h e Rosso il piemonte 12h allora giallo su Idrogeologico Domani', () => {
    const result = MyBulletin.min2([2, 5, 3])
    expect(result).toEqual(3)
  })
  it('Oggi medie - giallo almeno un piemontino 6h e giallo almeno un piemontino 12h con intervallo che comprende oggi allora giallo su Idraulico Oggi', () => {
    const result = MyBulletin.min2([3, 3, 2])
    expect(result).toEqual(3)
  })
  it('Oggi medie - giallo almeno un piemontino 6h e Rosso almeno un piemontino 12h con intervallo che comprende oggi allora giallo su Idraulico Oggi', () => {
    const result = MyBulletin.min2([3, 5, 2])
    expect(result).toEqual(3)
  })
  it('Domani medie - giallo almeno un piemontino 6h di oggi e giallo almeno un piemontino 12h con intervallo che comprende domani allora giallo su Idraulico domani', () => {
    const result = MyBulletin.min2([3, 3, 2])
    expect(result).toEqual(3)
  })
  it('[2, 2] -> 2', () => {
    const result = MyBulletin.min2([2, 2])
    expect(result).toEqual(2)
  })
  it('[2, 3] -> 2', () => {
    const result = MyBulletin.min2([2, 3])
    expect(result).toEqual(2)
  })
  it('[3, 3] -> 3', () => {
    const result = MyBulletin.min2([3, 3])
    expect(result).toEqual(3)
  })
  it('[2, 2, 3] -> 2', () => {
    const result = MyBulletin.min2([2, 2, 3])
    expect(result).toEqual(2)
  })
  it('[2, 3, 3] -> 3', () => {
    const result = MyBulletin.min2([2, 3, 3])
    expect(result).toEqual(3)
  })
  it('[3, 3, 3] -> 3', () => {
    const result = MyBulletin.min2([3, 3, 3])
    expect(result).toEqual(3)
  })
  it('[3, 4] -> 3', () => {
    const result = MyBulletin.min2([3, 4])
    expect(result).toEqual(3)
  })
  it('[4, 4] -> 4', () => {
    const result = MyBulletin.min2([4, 4])
    expect(result).toEqual(4)
  })
  it('[2, 2, 4] -> 2', () => {
    const result = MyBulletin.min2([2, 2, 4])
    expect(result).toEqual(2)
  })
  it('[2, 3, 4] -> 3', () => {
    const result = MyBulletin.min2([2, 3, 4])
    expect(result).toEqual(3)
  })
  it('[2, 4, 4] -> 4', () => {
    const result = MyBulletin.min2([2, 4, 4])
    expect(result).toEqual(4)
  })
  it('[3, 3, 4] -> 3', () => {
    const result = MyBulletin.min2([3, 3, 4])
    expect(result).toEqual(3)
  })
  it('[3, 4, 4] -> 4', () => {
    const result = MyBulletin.min2([3, 4, 4])
    expect(result).toEqual(4)
  })
  it('[2, 4, 5] -> 4', () => {
    const result = MyBulletin.min2([2, 4, 5])
    expect(result).toEqual(4)
  })
  it('[3, 4, 5] -> 4', () => {
    const result = MyBulletin.min2([3, 4, 5])
    expect(result).toEqual(4)
  })
  it('[4, 4, 5] -> 4', () => {
    const result = MyBulletin.min2([4, 4, 5])
    expect(result).toEqual(4)
  })
  it('[4, 5, 5] -> 4', () => {
    const result = MyBulletin.min2([4, 5, 5])
    expect(result).toEqual(5)
  })
})
