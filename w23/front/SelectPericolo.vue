// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <td :style="`background-color: ${coloreHtml};`">
    <select
      :value="idPericolo"
      @change="$emit('changePericolo', $event.target.value, area.id_w23_zone.id_w23_zone, campo)"
    >
      <option
        v-for="pericolo in pericoli"
        :key="pericolo.id_w23_pericolo"
        :value="pericolo.id_w23_pericolo"
      >
        {{ pericolo.id_w23_pericolo }}
      </option>
    </select>
  </td>
</template>

<script>
export default {
  name: 'SelectPericolo',
  props: {
    pericoli: {
      type: Array,
      default: () => { return [] }
    },
    area: {
      type: Object,
      default: () => { return { colore_html: 'white', id_w23_pericolo: 'BIANCO' } }
    },
    campo: {
      type: String,
      default: ''
    }
  },
  emits: ['changePericolo'],
  computed: {
    coloreHtml () { return this.area[this.campo].colore_html },
    idPericolo () { return this.area[this.campo].id_w23_pericolo }
  }
}
</script>
