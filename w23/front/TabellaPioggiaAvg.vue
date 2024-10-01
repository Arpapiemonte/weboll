// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <h1>Precipitazioni medie<span v-if="debug"> (da w30 PLUV)</span></h1>
  <h2>
    Per periodi di 6 ore consecutive<span v-if="debug"> (id_aggregazione 900)</span>, mm:
  </h2>
  <div class="table-responsive">
    <TabellaMappe
      :debug="debug"
      :labels="labels"
      :soglie="soglie.h6"
      :tls="tls[900]"
      :values="pioggeMedie[900]"
      :classes="classes"
    />
  </div>
  <h2>
    Per periodi di 12 ore consecutive<span v-if="debug"> (id_aggregazione 901)</span>, mm:
  </h2>
  <div class="table-responsive">
    <TabellaMappe
      :debug="debug"
      :labels="labels"
      :soglie="soglie.h12"
      :tls="tls[901]"
      :values="pioggeMedie[901]"
      :classes="classes"
    />
  </div>
  <h2>
    Per periodi di 24 ore consecutive<span v-if="debug"> (id_aggregazione 902)</span>, mm:
  </h2>
  <div class="table-responsive">
    <TabellaMappe
      :debug="debug"
      :labels="labels"
      :soglie="soglie.h24"
      :tls="tls[902]"
      :values="pioggeMedie[902]"
      :classes="classes"
    />
  </div>
  <h2>
    Per periodi di 48 ore consecutive<span v-if="debug"> (id_aggregazione 903)</span>, mm:
  </h2>
  <div class="table-responsive">
    <TabellaMappe
      :debug="debug"
      :labels="labels"
      :soglie="soglie.h48"
      :tls="tls[903]"
      :values="pioggeMedie[903]"
      :classes="classes"
    />
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
      <tr>
        <th
          class="bg-success bg-opacity-25 p-3"
        >
          Scadenza (in parte) nel passato che comprende valori osservati
          <table class="mt-2">
            <tr>
              <th
                width="25%"
                class="bg-success"
              />
              <td class="px-2">
                Osservazioni
              </td>
            </tr>
            <tr>
              <th class="bg-danger" />
              <td class="px-2">
                Previsioni
              </td>
            </tr>
            <tr>
              <th class="bg-light" />
              <td class="px-2">
                Dati mancanti
              </td>
            </tr>
          </table>
        </th>
      </tr>
    </table>
  </div>
  <h2>
    Soglie
  </h2>
  <div class="table-responsive">
    <TabellaSoglie
      title="Soglia pioggia, medie areali (mm)"
      :soglie="soglie"
      :legend="['Presoglia', 'Soglia 1', 'Soglia 2']"
      :levels="[0, 1, 2]"
      :ranges="['h6', 'h12', 'h24', 'h48']"
      :classes="classes"
    />
  </div>
</template>

<script>
import TabellaMappe from './TabellaMappe.vue'
import TabellaSoglie from './TabellaSoglie.vue'

export default {
  name: 'TabellaPioggiaAvg',
  components: {
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
    pioggeMedie: {
      type: Object,
      default: () => { return {} }
    },
    tls: {
      type: Object,
      default: () => { return {} }
    },
  },
  data () {
    // non reactive properties
    this.classes = ['all_1', 'all_2', 'all_3']
    return {}
  },
}
</script>

