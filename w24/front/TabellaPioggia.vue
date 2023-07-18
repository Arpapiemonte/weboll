// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <table
    v-if="data"
    class="table"
  >
    <thead>
      <tr>
        <th
          scope="col"
          rowspan="2"
          class="align-middle"
        >
          Area
        </th>
        <th
          scope="col"
          colspan="2"
          class="text-center"
        >
          Temporali
        </th>
        <th
          scope="col"
          colspan="2"
          class="text-center"
        >
          Precipitazioni
        </th>
        <th
          v-if="!(timelayout === 48 && tipoanomaliat === 'F')"
          scope="col"
          :colspan="'TERMA' in data && !(data.TERMA[0].id_time_layouts === 48 && tipoanomaliat === 'F') ? 4 : 1"
          class="text-center"
        >
          Anomalia termica
        </th>
        <th
          scope="col"
          colspan="2"
          class="text-center"
        >
          Vento
        </th>
        <th
          scope="col"
          rowspan="2"
          class="align-middle"
        >
          Nebbia
        </th>
        <th
          scope="col"
          rowspan="2"
          class="align-middle"
        >
          Gelate
        </th>
      </tr>
      <tr>
        <th scope="col">
          Intensità
        </th>
        <th scope="col">
          max/<br>6h
        </th>
        <th
          v-if="timelayout === 48"
          scope="col"
        >
          mm/<br>12h
        </th>
        <th
          v-else
          scope="col"
        >
          mm/<br>24h
        </th>
        <th scope="col">
          Intensità
        </th>
        <template v-if="'TERMA' in data && !(data.TERMA[0].id_time_layouts === 48 && tipoanomaliat === 'F')">
          <th scope="col">
            T
          </th>
          <th scope="col">
            Soglia<br>1
          </th>
          <th scope="col">
            Soglia<br>2
          </th>
        </template>
        <th 
          v-if="!(timelayout === 48 && tipoanomaliat === 'F')" 
          scope="col"
        >
          Classe
        </th>
        <th scope="col">
          Media<br>raf.
        </th>
        <th scope="col">
          Intensità
        </th>
      </tr>
    </thead>
    <tbody v-if="debug">
      <tr
        v-for="riga in righe"
        :key="riga"
      >
        <th scope="row">
          {{ riga }}
        </th>
        <td
          v-for="(type, colonna) in colonne"
          :key="colonna"
          scope="col"
        >
          area_data[{{ riga }}][{{ colonna }}]
        </td>
      </tr>
    </tbody>
    <tbody v-else>
      <tr
        v-for="riga in righe"
        :key="riga"
      >
        <th scope="row">
          {{ riga }}
        </th>
        <td
          v-for="(type, colonna) in colonne"
          :key="colonna"
          scope="col"
          :class="{
            classTemporali1: (colonna === 'RISK_STORM' && type && Math.round(area_data[riga][colonna].numeric_value) === 1),
            classTemporali2: (colonna === 'RISK_STORM' && type && Math.round(area_data[riga][colonna].numeric_value) === 2),
            classTemporali3: (colonna === 'RISK_STORM' && type && Math.round(area_data[riga][colonna].numeric_value) === 3),
            classTemporali4: (colonna === 'RISK_STORM' && type && Math.round(area_data[riga][colonna].numeric_value) === 4),
            classTermiche1: ((colonna === 'RISK_THOT' || colonna === 'RISK_TCOLD') && type && Math.round(area_data[riga][colonna].numeric_value) === 1),
            classTermiche2: ((colonna === 'RISK_THOT' || colonna === 'RISK_TCOLD') && type && Math.round(area_data[riga][colonna].numeric_value) === 2),
            classPiogge1: (colonna === 'RISK_RAIN' && type && Math.round(area_data[riga][colonna].numeric_value) === 1),
            classPiogge2: (colonna === 'RISK_RAIN' && type && Math.round(area_data[riga][colonna].numeric_value) === 2),
            classPiogge3: (colonna === 'RISK_RAIN' && type && Math.round(area_data[riga][colonna].numeric_value) === 3),
            classPiogge4: (colonna === 'RISK_RAIN' && type && Math.round(area_data[riga][colonna].numeric_value) === 4),
            class1: ((colonna === 'RISK_WIND' || colonna === 'RISK_FOG' || colonna === 'RISK_FROST') && type && Math.round(area_data[riga][colonna].numeric_value) === 1),
            class2: ((colonna === 'RISK_WIND' || colonna === 'RISK_FOG' || colonna === 'RISK_FROST') && type && Math.round(area_data[riga][colonna].numeric_value) === 2),
            class3: ((colonna === 'RISK_WIND' || colonna === 'RISK_FOG' || colonna === 'RISK_FROST') && type && Math.round(area_data[riga][colonna].numeric_value) === 3),
            class4: ((colonna === 'RISK_WIND' || colonna === 'RISK_FOG' || colonna === 'RISK_FROST') && type && Math.round(area_data[riga][colonna].numeric_value) === 4)
          }"
        >
          <template v-if="!type">
            <template v-if="colonna === 'TERMA' || colonna === 'TERMA1' || colonna === 'TERMA2'">
              {{ area_data[riga][colonna].numeric_value.slice(0,area_data[riga][colonna].numeric_value.length-1) }}
            </template>
            <template v-else>
              {{ Math.round(area_data[riga][colonna].numeric_value) }} 
            </template>
          </template>
          <template v-else>
            <template v-if="colonna === 'RISK_WIND'">
              <select
                :tabindex="tabcolonne[colonna]"
                class="form-control form-control-sm"
                :disabled="readonly"
                :value="Math.round(area_data[riga][colonna].numeric_value)"
                @change="setValue(area_data[riga][colonna].id_w24_data, $event.target.value)"
              >
                <option
                  v-for="(t, i) in type"
                  :key="i"
                  :value="i"
                >
                  {{ t.text }} {{ parseInt(soglievento[riga][t.intensita].soglia1) }} - {{ parseInt(soglievento[riga][t.intensita].soglia2) }}
                </option>
              </select>
            </template>
            <template v-else>
              <select
                :tabindex="tabcolonne[colonna]"
                class="form-control form-control-sm"
                :disabled="readonly"
                :value="Math.round(area_data[riga][colonna].numeric_value)"
                @change="setValue(area_data[riga][colonna].id_w24_data, $event.target.value)"
              >
                <option
                  v-for="(t, i) in type"
                  :key="i"
                  :value="i"
                >
                  {{ t }} 
                </option>
              </select>
            </template>
          </template>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'TabellaPioggia',
  props: {
    data: {
      type: Object,
      default: () => null
    },
    readonly: {
      type: Boolean,
      default: true
    },
    soglievento: {
      type: Object,
      default: () => { return {} }
    },
    tipoanomaliat: {
      type: String,
      default: ''
    },
    timelayout: {
      type: Number,
      default: 0
    },
  },
  emits: ['saveW24Data'],
  data () {
    // non reactive properties
    return {
      // reactive properties
      debug: false
    }
  },
  computed: {
    righe () {
      return [ "Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F", "Piem-G", "Piem-H", "Piem-I", "Piem-L", "Piem-M"]
    },
    colonne () {
      const colonne1 = {
        "RISK_STORM": ["assente", "rovesci", "temporali", "temporali forti", "temporali forti e persistenti"],
        "CUM_PLUV": null,
        "PLUV": null,
        "RISK_RAIN": ["assente", "debole", "moderata", "forte", "molto forte"]
      }
      let colonne2 = { }
      if ('TERMA' in this.data) {
        colonne2 = {
          "TERMA": null,
          "TERMA1": null,
          "TERMA2": null,
        }
      }
      const colonne3 = {
        "RISK_THOT": ["assente", "calda", "molto calda"],
        "RISK_TCOLD": ["assente", "fredda", "molto fredda"],
        "VELV": null,
        "RISK_WIND": [{"text": "calmo/debole:", "intensita": 0}, {"text": "moderato:", "intensita": 1}, {"text": "forte:", "intensita": 2}],
        "RISK_FOG": ["assenti", "locali", "diffuse"],
        "RISK_FROST": ["assenti", "sparse", "diffuse"]
      }
      if(this.tipoanomaliat === "C"){
        delete colonne3.RISK_TCOLD
      }else if(this.tipoanomaliat === "F"){
        delete colonne3.RISK_THOT
        if(this.timelayout === 48){
          delete colonne3.RISK_TCOLD
          return {...colonne1, ...colonne3}
        }
      }
      return {...colonne1, ...colonne2, ...colonne3}
    },
    tabcolonne () {
      let tabcolonne = {}
      let i = 1
      for(const colonna in this.colonne){
        tabcolonne[colonna] = i
        i += 1
      }
      return tabcolonne
    },
    area_data() {
      let vd = { }
      Object.keys(this.data).forEach(parametro => {
        this.rearrange(this.data, vd, parametro)
      })
      return vd
    }
  },
  methods: {
    rearrange(data, vd, parametro) {
      data[parametro].forEach(element => {
        if (!(element.id_allertamento in vd)) {
          vd[element.id_allertamento] = { }
        }
        vd[element.id_allertamento][parametro] = element
      })
    },
    setValue(id_w24_data, value) {
      console.log(`TabellaPioggia.setValue(${id_w24_data}, ${value})`)
      this.$emit('saveW24Data', id_w24_data, Number(value).toFixed(2))
    },
  }
}
</script>

<style>
.classTemporali1 {background-color: #7CFC00 !important;; }
.classTemporali2 {background-color: #228B22 !important;; }
.classTemporali3 {background-color: #FFFF00 !important;; }
.classTemporali4 {background-color: #FF7F50 !important;; }
.classTermiche1 {background-color: #ff69b4 !important;; }
.classTermiche2 {background-color: #C71585 !important;; }
.classPiogge1 {background-color: #99ffff !important;; }
.classPiogge2 {background-color: #66b3ff !important;; }
.classPiogge3 {background-color: #0554ad !important;; }
.classPiogge4 {background-color: black !important;; }
.class1 {background-color: #FAE6FA !important;; }
.class2 {background-color: #E0B0FF !important;; }
.class3 {background-color: #DF00FF !important;; }
</style>
