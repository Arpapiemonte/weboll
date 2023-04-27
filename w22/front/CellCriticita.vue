// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <td :style="`background-color: ${coloreHtml};`">
    <select
      :disabled="readonly"
      :value="idCriticita"
      @change="$emit('changeCriticita', $event.target.value, area.id_w22_data, area.id_w22_zone.id_w22_zone, campo)"
    >
      <option
        v-for="tend in criticita"
        :key="tend.id_w22_criticita"
        :value="tend.id_w22_criticita"
      >
        {{ tend.id_w22_criticita }}
      </option>
    </select>
  </td>
</template>

<script>
export default {
  name: 'CellCriticita',
  props: {
    criticita: {
      type: Array,
      default: () => { return [] }
    },
    area: {
      type: Object,
      default: () => { return { id_w22_criticita: 'A' } }
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
  emits: ['changeCriticita'],
  computed: {
    idCriticita () {
      return this.area[this.campo]
    },
    coloreHtml () {
      return this.criticitaRe[this.area[this.campo]]
    },
    criticitaRe() {
      let cr = {}
      Object.keys(this.criticita).forEach(id => {
        cr[this.criticita[id].id_w22_criticita] = this.criticita[id].colore_html
      })
      return cr
    }
  },
}
</script>
