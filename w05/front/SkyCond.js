// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
export default {
  data() {
    // non reactive properties
    this.nome_periodo = ['Mattino', 'Pomeriggio']
    return {}
  },
  computed: {
    venueSelection() {
      return Object.keys(this.selectedVenues).filter(venue => { return this.selectedVenues[venue] })
    },
    venue_data() {
      let vd = { }
      this.rearrange_sky_condit(this.cieli[0], vd, 'SKY_CONDIT')
      this.rearrange_terma(this.cieli[1], this.cieli[2], vd, 'TERMA')
      this.rearrange_terma(this.cieli[1], this.cieli[2], vd, 'TERMA_700')
      this.rearrange_terma(this.cieli[1], this.cieli[2], vd, 'TERMA_1500')
      this.rearrange_terma(this.cieli[1], this.cieli[2], vd, 'TERMA_2000')
      return vd
    }
  },
  methods: {
    rearrange1(cielo, vd, parametro) {
      cielo[parametro].forEach(element => {
        if (!(element.id_venue in vd)) {
          vd[element.id_venue] = { }
        }
        vd[element.id_venue][parametro] = [
          {
            numeric_value: element.numeric_value,
            id_w05_data: element.id_w05_data,
            id_trend: element.id_trend
          }
        ]
      })
    },
    rearrange2(cielo1, cielo2, vd, parametro) {
      this.rearrange1(cielo1, vd, parametro)
      cielo2[parametro].forEach(element => {
        if (!(element.id_venue in vd)) {
          vd[element.id_venue] = { }
          vd[element.id_venue][parametro] = []
        }
        vd[element.id_venue][parametro].push({
          numeric_value: element.numeric_value,
          id_w05_data: element.id_w05_data,
          id_trend: element.id_trend
        })
      })
    },
    setLevel(id_w05_data, old_value, new_value) {
      let data = {
        id_key: 'id_w05_data',
        id: id_w05_data,
        value_key: 'numeric_value',
        old_value: old_value,
        new_value: new_value
      }
      // console.log(data)
      this.$emit('transformed', data)
    },
    setAll(status) {
      Object.keys(this.selectedVenues).forEach(venue => { this.selectedVenues[venue] = status})
    },
    setAlpi(status) {
      var alpi = [87, 88, 89, 90]
      Object.keys(this.selectedVenues).filter(d => alpi.includes(Number(d))).forEach(venue => { this.selectedVenues[venue]  = status})
    },
    setPianure(status) {
      var pianure = [1, 9, 11, 28, 33, 59, 63, 64, 92, 93]
      //Object.keys(this.selectedVenues).filter(function(d) { return (d >= 1 && d <= 64) || d == 92 || d == 93; }).forEach(venue => { this.selectedVenues[venue]  = status})
      Object.keys(this.selectedVenues).filter(d => pianure.includes(Number(d))).forEach(venue => { this.selectedVenues[venue]  = status})
    },
    termaStep(id, step) {
      if (this.venueSelection.length > 0) {
        this.cieli[1 + id].TERMA.forEach(element => {
          if (this.venueSelection.includes(element.id_venue.toString())) {
            let new_value = Number(element.numeric_value) + step
            this.setLevel(element.id_w05_data, element.numeric_value, new_value)
          }
        })
      }
    }
  }
}
