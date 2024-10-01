// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
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
          rowspan="3"
          class="align-middle"
        >
          Area
        </th>
        <th
          scope="col"
          :colspan="data[0] ? 12 : 6"
          class="text-center"
        >
          Precipitazioni e quota neve da PSA
        </th>
        <th
          v-if="timelayout === 48"
          scope="col"
          colspan="4"
          class="text-center"
        >
          Nevicate attese (cm) in 12 h
        </th>
        <th
          v-else
          scope="col"
          colspan="4"
          class="text-center"
        >
          Nevicate attese (cm) in 24 h
        </th>
        <th
          scope="col"
          rowspan="3"
          class="align-middle"
        >
          Intensità<br>neve
        </th>
      </tr>
      <tr>
        <th
          v-if="data[0]"
          scope="col"
          colspan="3"
          class="text-center"
        >
          scad06
        </th>
        <th
          v-if="data[1]"
          scope="col"
          colspan="3"
          class="text-center"
        >
          scad12
        </th>
        <th
          scope="col"
          colspan="3"
          class="text-center"
        >
          scad18
        </th>
        <th
          scope="col"
          colspan="3"
          class="text-center"
        >
          scad00
        </th>
        <th
          scope="col"
          rowspan="2"
          class="align-middle"
        >
          Pianura<br>0-400m
        </th>
        <th
          scope="col"
          rowspan="2"
          class="align-middle"
        >
          Collina<br>500-700m
        </th>
        <th
          scope="col"
          rowspan="2"
          class="align-middle"
        >
          Montagna<br>800-1300m
        </th>
        <th
          scope="col"
          rowspan="2"
          class="align-middle"
        >
          Montagna<br>1400-2000m
        </th>
      </tr>
      <tr>
        <th
          v-if="data[0]"
          scope="col"
        >
          med
        </th>
        <th
          v-if="data[0]"
          scope="col"
        >
          max
        </th>
        <th
          v-if="data[0]"
          scope="col"
        >
          Q.N.
        </th>
        <th
          v-if="data[1]"
          scope="col"
        >
          med
        </th>
        <th
          v-if="data[1]"
          scope="col"
        >
          max
        </th>
        <th
          v-if="data[1]"
          scope="col"
        >
          Q.N.
        </th>
        <th scope="col">
          med
        </th>
        <th scope="col">
          max
        </th>
        <th scope="col">
          Q.N.
        </th>
        <th scope="col">
          med
        </th>
        <th scope="col">
          max
        </th>
        <th scope="col">
          Q.N.
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
          v-for="(colonna, index) in colonne"
          :key="index"
          scope="col"
        >
          area_data[{{ colonna.index }}][{{ riga }}][{{ colonna.parametro }}]
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
          v-for="(colonna, index) in colonne"
          :key="index"
          scope="col"
          :class="{
            classPiogge1: (colonna.opzioni && Math.round(area_data[colonna.index][riga][colonna.parametro].numeric_value) === 1),
            classPiogge2: (colonna.opzioni && Math.round(area_data[colonna.index][riga][colonna.parametro].numeric_value) === 2),
            classPiogge3: (colonna.opzioni && Math.round(area_data[colonna.index][riga][colonna.parametro].numeric_value) === 3),
            classPiogge4: (colonna.opzioni && Math.round(area_data[colonna.index][riga][colonna.parametro].numeric_value) === 4),
            bggray: colonna.bggray,
          }"
        > 
          <template v-if="colonna.opzioni">
            <select
              :tabindex="tabcolonne[colonna.parametro+colonna.index]"
              class="form-select form-select-sm"
              :disabled="readonly"
              :value="Math.round(area_data[colonna.index][riga][colonna.parametro].numeric_value)"
              @change="setClasse(area_data[colonna.index][riga][colonna.parametro].id_w24_data, $event.target.value)"
            >
              <option
                v-for="(t, i) in colonna.opzioni"
                :key="i"
                :value="i"
              >
                {{ t }}
              </option>
            </select>
          </template>
          <template v-else-if="colonna.value">
            <template v-if="colonna.parametro === 'SNOW_LEV'">
              <TabQuoteInput
                :tabindex="tabcolonne[colonna.parametro+colonna.index]"
                :readonly="readonly"
                :measure="area_data[colonna.index][riga][colonna.parametro].numeric_value"
                :idw24data="area_data[colonna.index][riga][colonna.parametro].id_w24_data"
                :refresher="refresher"
                @set-neve="setNeve"
              />
            </template>
            <template v-else-if="colonna.zones && colonna.zones.find(z => z === riga)">
              <input
                :tabindex="tabcolonne[colonna.parametro+colonna.index]"
                class="form-control"
                :disabled="readonly"
                :value="Math.round(area_data[colonna.index][riga][colonna.parametro].numeric_value)"
                @change="setValue(area_data[colonna.index][riga][colonna.parametro].id_w24_data, $event.target.value)"
              >
            </template>
            <template v-else-if="!colonna.zones">
              <input
                :tabindex="tabcolonne[colonna.parametro+colonna.index]"
                class="form-control"
                style="padding: 6px 6px;"
                :disabled="readonly"
                :value="Math.round(area_data[colonna.index][riga][colonna.parametro].numeric_value)"
                @change="setClasse(area_data[colonna.index][riga][colonna.parametro].id_w24_data, $event.target.value)"
              >
            </template>
          </template>
          <template v-else>
            {{ area_data[colonna.index][riga][colonna.parametro].numeric_value === "9999.00" ? '-' : Math.round(area_data[colonna.index][riga][colonna.parametro].numeric_value) }}
          </template>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import TabQuoteInput from './TabQuoteInput.vue'

export default {
  name: 'TabellaNeve',
  components: {
    TabQuoteInput
  },
  props: {
    data: {
      type: Array,
      default: () => { return [] }
    },
    readonly: {
      type: Boolean,
      default: true
    },
    timelayout: {
      type: Number,
      default: 0
    },
  },
  emits: ['saveW24Data', 'saveW24Value'],
  data () {
    // non reactive properties
    return {
      // reactive properties
      debug: false,
      refresher: 0
    }
  },
  computed: {
    colonne() {
      var cs = []
      if (this.data[0]) {
        cs = cs.concat([
          {
            index: 0,
            parametro: "PLUV",
            value: true,
          },
          {
            index: 0,
            parametro: "PLUV1",
            value: true,
          },
          {
            index: 0,
            parametro: "SNOW_LEV",
            value: true,
          },
          {
            index: 1,
            parametro: "PLUV",
            value: true,
            bggray: true,
          },
          {
            index: 1,
            parametro: "PLUV1",
            value: true,
            bggray: true,
          },
          {
            index: 1,
            parametro: "SNOW_LEV",
            value: true,
            bggray: true,
          }
        ])
      }
      cs = cs.concat([
        {
          index: 2,
          parametro: "PLUV",
          value: true,
        },
        {
          index: 2,
          parametro: "PLUV1",
          value: true,
        },
        {
          index: 2,
          parametro: "SNOW_LEV",
          value: true,
        },
        {
          index: 3,
          parametro: "PLUV",
          value: true,
          bggray: true,
        },
        {
          index: 3,
          parametro: "PLUV1",
          value: true,
          bggray: true,
        },
        {
          index: 3,
          parametro: "SNOW_LEV",
          value: true,
          bggray: true,
        },
        {
          index: 4,
          parametro: "SNOW_400",
          value: true,
          zones: ["Piem-A", "Piem-F", "Piem-G", "Piem-H", "Piem-I", "Piem-L", "Piem-M"]
        },
        {
          index: 4,
          parametro: "SNOW_700",
          value: true,
          zones: ["Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F", "Piem-G", "Piem-H", "Piem-M"]
        },
        {
          index: 4,
          parametro: "SNOW_1000",
          value: true,
          zones: ["Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F"]
        },
        {
          index: 4,
          parametro: "SNOW_2000",
          value: true,
          zones: ["Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F"]
        },
        {
          index: 4,
          parametro: "SNOW",
          opzioni: ["assente", "debole", "moderata", "forte"]
        }
      ])
      return cs
    },
    tabcolonne () {
      let tabcolonne = {}
      let i = 20
      this.colonne.forEach(colonna => {
        tabcolonne[colonna.parametro+colonna.index] = i + colonna.index
        i += 1
      })
      return tabcolonne
    },
    righe () {
      return [ "Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F", "Piem-G", "Piem-H", "Piem-I", "Piem-L", "Piem-M"]
    },
    area_data() {
      let vd = [ ]
      this.data.forEach(tl => {
        let vvd = { }
        if (tl) {
          Object.keys(tl).forEach(parametro => {
            this.rearrange(tl, vvd, parametro)
          })
        }
        vd.push(vvd)
      })
      // console.log("area_data",vd)
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
    setNeve(id_w24_data, value){
      this.forceUpdate()
      this.setClasse(id_w24_data, value)
    },
    forceUpdate(){
      this.refresher += 1
    },
    setClasse(id_w24_data, value) {
      // console.log(`TabellaNeve.setClasse(${id_w24_data}, ${value})`)
      this.$emit('saveW24Data', id_w24_data, Number(value).toFixed(2))
    },
    setValue(id_w24_data, value) {
      // console.log(`TabellaNeve.setValue(${id_w24_data}, ${value})`)
      this.$emit('saveW24Value', id_w24_data, Number(value).toFixed(2))
    },
  }
}
</script>

<style>
  .bggray {background-color: rgba(211, 211, 211, 0.4) !important;;}
  input[type="Number"] {
    appearance: textfield;
  }
</style>