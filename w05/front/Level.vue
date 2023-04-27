// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <input
    :style="'width: ' + width +'em;'"
    type="number"
    min="0"
    :max="max"
    :value="nullable && (data[valueKey] === '' || data[valueKey] == null) ? '' : Number(data[valueKey])"
    :disabled="readonly"
    :class="{dirty: history.isDirty(data.id_w05_data, 'id_w05_data', valueKey)}"
    @change="$emit('setLevel', data.id_w05_data, data[valueKey], nullable && $event.target.value === '' ? null : Math.max(Math.min($event.target.value, max), 0).toString(), valueKey)"
  >
</template>

<script>
export default {
  name: 'LevelInput',
  props: {
    data: {
      type: Object,
      default: () => {
        let d = { id_w05_data: null }
        d[this.valueKey] = null
        return d
      }
    },
    readonly: {
      type: Boolean,
      default: false
    },
    history: {
      type: Object,
      default: () => { return { cursor: -1, snapshots: [] } }
    },
    max: {
      type: Number,
      default: 6000
    },
    width: {
      type: Number,
      default: 5
    },
    valueKey: {
      type: String,
      default: "numeric_value"
    },
    nullable: {
      type: Boolean,
      default: false
    }
  },
  emits: ['setLevel']
}
</script>
