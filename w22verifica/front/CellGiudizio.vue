// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt// ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
<template>
  <td :style="`background-color: ${coloreHtml};`">
    <select
      :disabled="readonly"
      :value="idGiudizio"
      @change="$emit('changeGiudizio', $event.target.value, w22verifica.id_w22verifica, 'id_w22giudizio')"
    >
      <option
        v-for="prob in giudizio"
        :key="prob.id_w22giudizio"
        :value="prob.id_w22giudizio"
      >
        {{ prob.descrizione }}-{{ prob.id_w22giudizio }}
      </option>
    </select>
  </td>
</template>

<script>
export default {
  name: 'CellGiudizio',
  props: {
    w22verifica: {
      type: Array,
      default: () => { return [] }
    },
    area: {
      type: Object,
      default: () => { return { id_w22giudizio: '1' } }
    },
    campo: {
      type: String,
      default: ''
    },
    giudizio: {
      type: Array,
      default: () => { return [] }
    },
    giudizioRe: {
      type: Object,
      default: () => { return {} }
    },
    readonly: {
      type: Boolean,
      default: true,
    }
  },
  emits: ['changeGiudizio'],
  computed: {
    idGiudizio () {
      return this.area[this.campo]
    },
    coloreHtml () {
      return this.giudizioRe[this.area[this.campo]]
    }
  },
  watch: {
    	giudizio: function() {
          Object.keys(this.giudizio).forEach(id => {
            this.giudizioRe[this.giudizio[id].id_w22giudizio] = this.giudizio[id].colore_html
          })
      }
  }
}
</script>
