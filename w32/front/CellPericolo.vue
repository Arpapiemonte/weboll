// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <td
    :style="`background-color: ${coloreHtml};`"
  >
    <select
      v-bind="field"
      :value="idPericolo"
      class="form-select my-1"
      :disabled="readonly"
      @change="$emit('changePericolo', $event.target.value, area.id_w32_zone.id_w32_zone, campo);"
    >
      <option
        v-for="per in pericolo"
        :key="per.id_w32_pericolo"
        :value="per.id_w32_pericolo"
      >
        {{ per.id_w32_pericolo }}
      </option>
    </select>
  </td>
</template>

<script>

export default {
  name: 'CellPericolo',
  props: {
    pericolo: {
      type: Array,
      default: () => { return [] }
    },
    area: {
      type: Object,
      default: () => { return { colore_html: 'white', id_w32_pericolo: 'np' } }
    },
    campo: {
      type: String,
      default: ''
    },
    field: {
      type: String,
      default: ''
    },
    readonly: {
      type: Boolean,
      default: true,
    },
    required: {
      type: Boolean,
      default: true
    }
  },
  emits: ['changePericolo'],
  computed: {
    coloreHtml () {
      var colore = 'red'
      if (this.area[this.campo] == 'np')
        colore = '#FFFFFF'
      else if (this.area[this.campo] == 'A')
        colore = '#A6A6A6'
      else if (this.area[this.campo] == 'I')
        colore = '#99CCFF'
      else if (this.area[this.campo] == 'P')
        colore = '#9999FF'
      else if (this.area[this.campo] == 'D')
        colore = '#9900FF'
      return colore
    },
    idPericolo () {
      return this.area[this.campo]
    }
  }
}
</script>
