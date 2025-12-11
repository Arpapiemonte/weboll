// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <td
    :style="`background-color: ${coloreHtml};`"
  >
    <select
      v-bind="field"
      :value="idPericolombacini"
      class="form-select my-1"
      :disabled="readonly"
      @change="$emit('changePericolombacini', $event.target.value, area.id_w32_mbacini.id_w32_mbacini, campo.slice(0, -8));"
    >
      <option
        v-for="per in pericolombacini"
        :key="per.id_w32_pericolombacini"
        :value="per.id_w32_pericolombacini"
      >
        {{ per.id_w32_pericolombacini }}
      </option>
    </select>
  </td>
</template>

<script language="JavaScript">

export default {
  name: 'CellPericoloMbacini',
  props: {
    pericolombacini: {
      type: Array,
      default: () => { return [] }
    },
    area: {
      type: Object,
      default: () => { return { colore_html: 'white', id_w32_pericolombacini: 'np' } }
    },
    field: {
      type: String,
      default: ''
    },
    campo: {
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
  emits: ['changePericolombacini'],
  computed: {
    coloreHtml () {
      var colore = 'red'
      if (this.area[this.campo.slice(0, -8)] == 'np')
        colore = '#FFFFFF'
      else if (this.area[this.campo.slice(0, -8)] == '-')
        colore = '#A6A6A6'
      else if (this.area[this.campo.slice(0, -8)] == 'S')
        colore = '#4999CE'
      return colore
    },
    idPericolombacini () {
      return this.area[this.campo.slice(0, -8)]
    }
  },
}
</script>
