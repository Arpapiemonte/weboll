// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <h1>Massime precipitazioni</h1>
  <h2>
    Per periodi di 6 ore consecutive<span v-if="debug"> (da w30 PLUV con id_aggregazione 125)</span>, mm:
  </h2>
  <div class="table-responsive">
    <TabellaMappe
      :debug="debug"
      :labels="labels"
      :soglie="soglie.h6"
      :tls="tl6"
      :values="pioggeMassime[125]"
      :classes="classes"
    />
  </div>

  <h2>
    Per periodi di 12 ore consecutive<span v-if="debug"> (da w30 PLUV con id_aggregazione 126)</span>, mm:
  </h2>
  <div class="table-responsive">
    <table class="table">
      <tbody>
        <tr>
          <td width="10%">
            <MapPluv
              :soglie="soglie.h12"
              :values="pioggeMassime[126][48]"
              :classes="classes"
            />
          </td>
          <td width="10%">
            <MapPluv
              :soglie="soglie.h12"
              :values="pioggeMassime[126][66]"
              :classes="classes"
            />
          </td>
          <td width="10%" />
          <td width="10%" />
          <td width="10%" />
          <td width="10%" />
          <td width="10%" />
          <td width="10%" />
          <td width="10%" />
        </tr>
      </tbody>
      <thead>
        <tr>
          <th>
            Da: {{ labels[48][0] }}<br>A: {{ labels[48][1] }}<br><small
              v-if="debug"
              style="font-size: em;"
            >(id_time_layout: 48)</small>
          </th>
          <th>
            Da: {{ labels[66][0] }}<br>A: {{ labels[66][1] }}<br><small
              v-if="debug"
              style="font-size: em;"
            >(id_time_layout: 66)</small>
          </th>
          <th />
          <th />
          <th />
          <th />
          <th />
          <th />
          <th />
          <th />
        </tr>
      </thead>
    </table>
  </div>

  <h2>
    Per periodi di 24 ore consecutive<span v-if="debug"> (da w30 PLUV con id_aggregazione 127)</span>, mm:
  </h2>
  <div class="table-responsive">
    <table class="table">
      <tbody>
        <tr>
          <td width="10%">
            <MapPluv
              :soglie="soglie.h24"
              :values="pioggeMassime[127][66]"
              :classes="classes"
            />
          </td>
          <td width="10%" />
          <td width="10%" />
          <td width="10%" />
          <td width="10%" />
          <td width="10%" />
          <td width="10%" />
          <td width="10%" />
          <td width="10%" />
        </tr>
      </tbody>
      <thead>
        <tr>
          <th>
            Da: {{ labels[66][0] }}<br>A: {{ labels[66][1] }}<br><small
              v-if="debug"
              style="font-size: em;"
            >(id_time_layout: 66)</small>
          </th>
        </tr>
      </thead>
    </table>
  </div>

  <h2>
    Legenda
  </h2>
  <div class="table-responsive">
    <table class="table">
      <tr>
        <th
          width="25%"
          class="bg-danger bg-opacity-25 p-3"
        >
          Scadenza nel futuro fuori dallo scopo temporale del bollettino
        </th>
        <td />
      </tr>
    </table>
  </div>

  <h2>
    Soglie
  </h2>
  <div class="table-responsive">
    <TabellaSoglie
      title="Soglia pioggia, massime puntuali (mm)"
      :soglie="soglie"
      :legend="['Presoglia', 'Soglia 1', 'Soglia 2', 'Soglia 3']"
      :levels="[0, 1, 2, 3]"
      :ranges="['h6', 'h12', 'h24']"
      :classes="classes"
    />
  </div>
</template>

<script>
import MapPluv from './MapPluv.vue'
import TabellaMappe from './TabellaMappe.vue'
import TabellaSoglie from './TabellaSoglie.vue'

export default {
  name: 'TabellaPioggiaMax',
  components: {
    MapPluv,
    TabellaMappe,
    TabellaSoglie,
  },
  props: {
    debug: {
      type: Boolean,
      default: false
    },
    labels: {
      type: Object,
      default: () => { return {} }
    },
    soglie: {
      type: Object,
      default: () => { return {} }
    },
    pioggeMassime: {
      type: Object,
      default: () => { return {} }
    },
  },
  data () {
    // non reactive properties
    this.tl6 = [{id:45, role:0}, {id:46, role:0}, {id:60, role:0}, {id:61, role:0}, {id:62, role:0}, {id:63, role:0}, {id:77, role:1}, {id:78, role:1}, {id:79, role:1}, {id:80, role:1}]
    this.classes = ['pre_all', 'all_1', 'all_2', 'all_3']
    return {}
  },
}
</script>
