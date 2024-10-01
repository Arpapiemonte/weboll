// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <td>
    <select
      :value="Number(data.numeric_value)"
      :disabled="readonly"
      class="form-control form-control-sm"
      :class="{
        dirty: history.isDirty(data.id_w05_data, 'id_w05_data', 'numeric_value'),
        'is-invalid': validity[data.id_w05_data]
      }"
      @change="$emit('setLevel', data.id_w05_data, data.numeric_value, $event.target.value)"
    >
      <option
        v-for="icon in icons"
        :key="icon.id_sky_condition"
        :value="icon.id_sky_condition"
      >
        {{ icon.description_ita }}
      </option>
    </select>
  </td>
</template>

<script>
export default {
  name: 'CellSelect',
  props: {
    data: {
      type: Object,
      default: () => { return { numeric_value: "0.00", id_w05_data: null, "id_trend": null } }
    },
    icons: {
      type: Array,
      default: () => { return [] }
    },
    readonly: {
      type: Boolean,
      default: false
    },
    history: {
      type: Object,
      default: () => { return { cursor: -1, snapshots: [] } }
    },
    validity: {
      type: Object,
      default: () => { return {} }
    },
  },
  emits: ['setLevel']
}
</script>
