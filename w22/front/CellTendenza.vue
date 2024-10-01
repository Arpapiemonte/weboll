// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <td>
    <select
      :disabled="readonly"
      :value="idTendenza"
      @change="$emit('changeTendenza', $event.target.value, area.id_w22_data, area.id_w22_zone.id_w22_zone, campo)"
    >
      <option
        v-for="tend in tendenza"
        :key="tend.id_w22_tendenza"
        :value="tend.descrizione"
      >
        {{ tend.descrizione }}
      </option>
    </select>
  </td>
</template>

<script>
export default {
  name: 'CellTendenza',
  props: {
    tendenza: {
      type: Array,
      default: () => { return [] }
    },
    area: {
      type: Object,
      default: () => { return { descrizione: 'stazionario' } }
    },
    campo: {
      type: String,
      default: ''
    },
    readonly: {
      type: Boolean,
      default: true,
    }
  },
  emits: ['changeTendenza'],
  computed: {
    idTendenza () {
      return this.area[this.campo]
    }
  }
}
</script>
