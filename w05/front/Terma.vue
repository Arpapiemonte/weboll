// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <input
    style="width: 3em;"
    type="number"
    min="-30"
    max="50"
    :value="Number(data.numeric_value)"
    :disabled="readonly"
    :class="{dirty: history.isDirty(data.id_w05_data, 'id_w05_data', 'numeric_value')}"
    @change="$emit('setLevel', data.id_w05_data, data.numeric_value, Math.max(Math.min($event.target.value, 50), -30))"
  >
</template>

<script>
export default {
  name: 'TermaInput',
  props: {
    data: {
      type: Object,
      default: () => {
        return {
          numeric_value: "0.00",
          id_w05_data: null,
          id_trend:0
        }
      }
    },
    readonly: {
      type: Boolean,
      default: false
    },
    history: {
      type: Object,
      default: () => { return { cursor: -1, snapshots: [] } }
    }
  },
  emits: ['setLevel']
}
</script>
