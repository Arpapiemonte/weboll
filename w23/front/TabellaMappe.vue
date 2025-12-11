// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <table
    class="table"
  >
    <tbody>
      <tr>
        <td
          v-for="tl in tls"
          :key="tl.id"
          :class="{'bg-success': tl.role < 0, 'bg-danger': tl.role > 0}"
          class="bg-opacity-25"
        >
          <MapPluv
            :soglie="soglie"
            :values="values[tl.id]"
            :classes="classes"
            :counts="tl.counts ? tl.counts : {}"
          />
        </td>
      </tr>
    </tbody>
    <thead>
      <tr>
        <th
          v-for="tl in tls"
          :key="tl.id"
          :class="{'bg-success': tl.role < 0, 'bg-danger': tl.role > 0}"
          class="bg-opacity-25"
        >
          Da: {{ labels[tl.id][0] }}<br>A: {{ labels[tl.id][1] }}<br><small
            v-if="debug"
            style="font-size: em;"
          >(id_time_layout: {{ tl.id }})</small>
        </th>
      </tr>
    </thead>
  </table>
</template>

<script>
import MapPluv from './MapPluv.vue'

export default {
  name: 'TabellaMappe',
  components: {
    MapPluv,
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
    tls: {
      type: Object,
      default: () => { return {} }
    },
    values: {
      type: Object,
      default: () => { return {} }
    },
    classes: {
      type: Array,
      default: () => []
    },
  },
}
</script>
