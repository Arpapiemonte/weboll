// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <td>
    <select
      :disabled="readonly"
      :value="idProbabilita"
      class="form-select my-1"
      @change="$emit('changeProbabilita', $event.target.value, area.id_w29_zone.id_w29_zone, campo)"
    >
      <option
        v-for="prob in probabilita"
        :key="prob.id_w29_probabilita"
        :value="prob.id_w29_probabilita"
      >
        {{ prob.id_w29_probabilita }}
      </option>
    </select>
  </td>
</template>

<script>
export default {
  name: 'CellProbabilita',
  props: {
    probabilita: {
      type: Array,
      default: () => { return [] }
    },
    area: {
      type: Object,
      default: () => { return { id_w29_probabilita: 'nessuna' } }
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
  emits: ['changeProbabilita'],
  computed: {
    idProbabilita () {
      return this.area[this.campo]
    }
  }
}
</script>
