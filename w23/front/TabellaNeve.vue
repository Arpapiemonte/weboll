// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <h1>Neve<span v-if="debug"> da w24</span></h1>
  <h2 v-if="debug">
    estremi <code>SNOW_LEV</code> + cumulate <code>SNOW_{400,700,1000}</code>
  </h2>
  <div class="table-responsive">
    <table
      v-if="neve"
      class="table text-center"
    >
      <thead>
        <tr>
          <th
            scope="col"
            rowspan="3"
            class="align-middle"
          >
            Zone di<br>allerta
          </th>
          <th
            scope="col"
            colspan="8"
            class="align-middle"
          >
            Quota neve, m.s.l.d.m.
          </th>
          <th
            scope="col"
            colspan="9"
            class="align-middle"
          >
            Precipitazioni nevose, cm
          </th>
        </tr>
        <tr>
          <th
            scope="col"
            colspan="2"
          />
          <th
            scope="col"
            colspan="2"
            class="align-middle"
          >
            Oggi
          </th>
          <th
            scope="col"
            colspan="4"
            class="align-middle"
          >
            Domani
          </th>
          <th
            scope="col"
            colspan="3"
            class="align-middle"
          >
            Fino a 400 m<br>(pianura)
          </th>
          <th
            scope="col"
            colspan="3"
            class="align-middle"
          >
            Da 400 m a 700 m<br>(collina)
          </th>
          <th
            scope="col"
            colspan="3"
            class="align-middle"
          >
            Da 700 m a 1000 m<br>(montagna)
          </th>
        </tr>
        <tr>
          <th
            v-for="(colonna, index) in colonne"
            :key="index"
            scope="col"
            v-html="colonna.titolo"
          />
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
            neve[{{ colonna.parametro }}][{{ colonna.time_layout }}][{{ riga }}]
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
            :class="classes(riga, colonna)"
          >
            <template v-if="colonna.zones">
              <span v-if="colonna.zones.find(z => z === riga)">
                {{ neve[colonna.parametro][colonna.time_layout][riga] }}
              </span>
              <span v-else />
            </template>
            <template v-else>
              <span v-if="'formato' in colonna">
                {{ clip(neve[colonna.parametro][colonna.time_layout][riga]) }}
              </span>
              <span v-else>
                {{ neve[colonna.parametro][colonna.time_layout][riga] }}
              </span>
            </template>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="table-responsive">
    <table
      v-if="soglie"
      class="table text-center"
    >
      <thead>
        <tr>
          <th
            scope="col"
            rowspan="3"
            class="align-middle"
          >
            Zone di<br>allerta
          </th>
          <th
            scope="col"
            colspan="9"
            class="align-middle"
          >
            Soglia neve (cm)
          </th>
        </tr>
        <tr>
          <th
            scope="col"
            colspan="3"
            class="align-middle"
          >
            Pianura
          </th>
          <th
            scope="col"
            colspan="3"
            class="align-middle"
          >
            Collina
          </th>
          <th
            scope="col"
            colspan="3"
            class="align-middle"
          >
            Montagna
          </th>
        </tr>
        <tr>
          <th
            scope="col"
            class="align-middler"
          >
            Presoglia
          </th>
          <th
            scope="col"
            class="align-middle"
          >
            Soglia 1
          </th>
          <th
            scope="col"
            class="align-middle"
          >
            Soglia 2
          </th>
          <th
            scope="col"
            class="align-middle"
          >
            Presoglia
          </th>
          <th
            scope="col"
            class="align-middle"
          >
            Soglia 1
          </th>
          <th
            scope="col"
            class="align-middle"
          >
            Soglia 2
          </th>
          <th
            scope="col"
            class="align-middle"
          >
            Presoglia
          </th>
          <th
            scope="col"
            class="align-middle"
          >
            Soglia 1
          </th>
          <th
            scope="col"
            class="align-middle"
          >
            Soglia 2
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="riga in righe"
          :key="riga"
        >
          <th scope="row">
            {{ riga }}
          </th>
          <template
            v-for="ambito in ['pianura', 'collina', 'montagna ']"
            :key="ambito"
          >
            <td :class="{all_1: soglie[ambito][riga].soglia_cod1 < 999}">
              <span v-if="soglie[ambito][riga].soglia_cod1 < 999">{{ parseInt(soglie[ambito][riga].soglia_cod1) }}</span>
              <span v-else>-</span>
            </td>
            <td :class="{all_2: soglie[ambito][riga].soglia_cod1 < 999}">
              <span v-if="soglie[ambito][riga].soglia_cod2 < 999">{{ parseInt(soglie[ambito][riga].soglia_cod2) }}</span>
              <span v-else>-</span>
            </td>
            <td :class="{all_3: soglie[ambito][riga].soglia_cod1 < 999}">
              <span v-if="soglie[ambito][riga].soglia_cod3 < 999">{{ parseInt(soglie[ambito][riga].soglia_cod3) }}</span>
              <span v-else>-</span>
            </td>
          </template>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'TabellaNeve',
  props: {
    debug: {
      type: Boolean,
      default: false
    },
    soglie: {
      type: Object,
      default: () => { return {} }
    },
    neve: {
      type: Object,
      default: () => { return {} }
    },
  },
  data () {
    // non reactive properties
    this.colonne = [
      {
        parametro: "SNOW_LEV_MIN",
        time_layout: 1009,
        titolo: "Min<br>36 h"
      },
      {
        parametro: "SNOW_LEV_MAX",
        time_layout: 1009,
        titolo: "Max<br>36 h"
      },
      {
        parametro: "SNOW_LEV",
        time_layout: 45,
        titolo: "D0<br>12-18",
        formato: "clip"
      },
      {
        parametro: "SNOW_LEV",
        time_layout: 46,
        titolo: "D0<br>18-24",
        formato: "clip"
      },
      {
        parametro: "SNOW_LEV",
        time_layout: 60,
        titolo: "D1<br>0-6",
        formato: "clip"
      },
      {
        parametro: "SNOW_LEV",
        time_layout: 61,
        titolo: "D1<br>6-12",
        formato: "clip"
      },
      {
        parametro: "SNOW_LEV",
        time_layout: 62,
        titolo: "D1<br>12-18",
        formato: "clip"
      },
      {
        parametro: "SNOW_LEV",
        time_layout: 63,
        titolo: "D1<br>18-24",
        formato: "clip"
      },
      {
        parametro: "SNOW_400",
        time_layout: 1009,
        titolo: "In 36 h",
        ambito: "pianura",
        zones: ["Piem-A", "Piem-F", "Piem-G", "Piem-H", "Piem-I", "Piem-L", "Piem-M"]
      },
      {
        parametro: "SNOW_400",
        time_layout: 48,
        titolo: "Oggi",
        ambito: "pianura",
        zones: ["Piem-A", "Piem-F", "Piem-G", "Piem-H", "Piem-I", "Piem-L", "Piem-M"]
      },
      {
        parametro: "SNOW_400",
        time_layout: 66,
        titolo: "Domani",
        ambito: "pianura",
        zones: ["Piem-A", "Piem-F", "Piem-G", "Piem-H", "Piem-I", "Piem-L", "Piem-M"]
      },
      {
        parametro: "SNOW_700",
        time_layout: 1009,
        titolo: "In 36 h",
        ambito: "collina",
        zones: ["Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F", "Piem-G", "Piem-H", "Piem-M"],
      },
      {
        parametro: "SNOW_700",
        time_layout: 48,
        titolo: "Oggi",
        ambito: "collina",
        zones: ["Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F", "Piem-G", "Piem-H", "Piem-M"],
      },
      {
        parametro: "SNOW_700",
        time_layout: 66,
        titolo: "Domani",
        ambito: "collina",
        zones: ["Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F", "Piem-G", "Piem-H", "Piem-M"],
      },
      {
        parametro: "SNOW_1000",
        time_layout: 1009,
        titolo: "In 36 h",
        ambito:"montagna ",
        zones: ["Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F"],
      },
      {
        parametro: "SNOW_1000",
        time_layout: 48,
        titolo: "Oggi",
        ambito:"montagna ",
        zones: ["Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F"],
      },
      {
        parametro: "SNOW_1000",
        time_layout: 66,
        titolo: "Domani",
        ambito:"montagna ",
        zones: ["Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F"],
      }
    ]
    this.righe = ["Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F", "Piem-G", "Piem-H", "Piem-I", "Piem-L", "Piem-M"]
    return {
      // reactive properties
    }
  },
  methods: {
    classes(riga, colonna) {
      const factor = 1.0  // colonna.time_layout === 1009 ? 1.5 : 1.0
      if ('ambito' in colonna) {
        const value = this.neve[colonna.parametro][colonna.time_layout][riga]
        const soglia = this.soglie[colonna.ambito][riga]
        return {
          all_1: value >= soglia.soglia_cod1 * factor,
          all_2: value >= soglia.soglia_cod2 * factor,
          all_3: value >= soglia.soglia_cod3 * factor
        }
      } else {
        return {}
      }
    },
    clip(value) {
      return value < 9990 && value > 0 ? value : null
    }
  }
}
</script>

<style scoped>
  .all_0 {background-color: #6EBB00;}
  .all_1 {background-color: #FFFF00;}
  .all_2 {background-color: #FFA500;}
  .all_3 {background-color: #FF0000;}
  .all_4 {background-color: #ffffff;}
</style>
