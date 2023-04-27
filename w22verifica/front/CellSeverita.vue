// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt// ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
<template>
  <td :style="`background-color: ${coloreHtml};`">
    <select
      :disabled="readonly"
      :value="idSeverita"
      @change="$emit('changeSeverita', $event.target.value, area.id_w22verifica_data, area.id_w22_zone.id_w22_zone, campo)"
    >
      <option
        v-for="prob in severita"
        :key="prob.id_w22severita"
        :value="prob.id_w22severita"
      >
        {{ prob.sigla }} - {{ prob.id_w22severita }}
      </option>
    </select>
  </td>
</template>

<script>
export default {
  name: 'CellSeverita',
  props: {
    severita: {
      type: Array,
      default: () => { return [] }
    },
    severitaRe: {
      type: Object,
      default: () => { return {} }
    },
    area: {
      type: Object,
      default: () => { return { id_w22severita: '1' } }
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
  emits: ['changeSeverita'],
  computed: {
    idSeverita () {
      return this.area[this.campo]
    },
    coloreHtml () {
      return this.severitaRe[this.area[this.campo]]
    }
  },
  beforeMount() {
    Object.keys(this.severita).forEach(id => {
      this.severitaRe[this.severita[id].id_w22severita] = this.severita[id].colore_html
    })
  },
}
</script>
