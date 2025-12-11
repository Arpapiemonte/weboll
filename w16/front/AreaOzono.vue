// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="border p-4 m-3">
    <div class="row my-3">
      <div class="col-md-6">
        <h4>Area {{ String.fromCharCode(64 + Number(venue)) }}</h4>
      </div>
      <div class="col-md-6 my-auto">
        Livello:
        <select
          v-if="!readonly"
          :value="value.level"
          :class="{ dirty: history.isDirty(value.id_w16_data, 'id_w16_data', 'id_ozono_livelli') }"
          @change="$emit('setLevel', venue, value.id_w16_data, value.level, $event.target.value)"
        >
          <option
            v-for="level in levels"
            :key="level.id"
            :value="level.id_ozono_livelli"
          >
            {{ level.livelli }}
          </option>
        </select>
        <span v-else>{{ value.level }}</span>
      </div>
    </div>
    <table
      v-if="Object.keys(value.w16data1.mx8).length > 0"
      class="table container table-striped p-3"
    >
      <thead>
        <tr class="row">
          <th
            scope="col"
            class="col text-center"
          >
            Aggregazione spaziale
          </th>
          <th
            scope="col"
            class="col text-center"
          >
            Max nel giorno della media mobile su 8h
          </th>
          <th
            scope="col"
            class="col text-center"
          >
            Max nel giorno
          </th>
          <th
            scope="col"
            class="col text-center"
          >
            Livello proposto
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(forValue, aggregazione_spaziale) in value.w16data1.mx8"
          :key="aggregazione_spaziale"
          class="row"
        >
          <td class="col">
            {{ humanize(aggregazione_spaziale) }}
          </td>
          <td class="col">
            {{ forValue }}
          </td>
          <td class="col">
            {{ value.w16data1.mxd[aggregazione_spaziale] }}
          </td>
          <td class="col">
            {{ Math.max(livello_proposto_mx8(forValue), livello_proposto_mxd(value.w16data1.mxd[aggregazione_spaziale])) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: Object,
      default: () => { return { level: 0, id_w16_data: 0, w16data1: {} } }
    },
    venue: {
      type: String,
      default: ""
    },
    readonly: {
      type: Boolean,
    },
    history: {
      type: Object,
      default: () => { return { cursor: -1, snapshots: [] } }
    },
    levels: {
      type: Array,
      default: () => { return [] }
    },
  },
  emits: ['setLevel'],
  methods: {
    humanize(aggregazione_spaziale) {
      switch (aggregazione_spaziale) {
        case "90p":
          return "90 percentile";
        case "75p":
          return "75 percentile";
        case "50p":
          return "50 percentile";
        case "med":
          return "media";
        case "max":
          return "massimo";
      }
    },
    livello_proposto_mxd(value) {
      let compare = this.levels.map(level => { return value > level.soglia_inferiore_mxd }).filter(condition => condition)
      return Math.max(0, compare.length - 1)
    },
    livello_proposto_mx8(value) {
      let compare = this.levels.map(level => { return value > level.soglia_inferiore_mx8 }).filter(condition => condition)
      return Math.max(0, compare.length - 1)
    }
  }
};
</script>