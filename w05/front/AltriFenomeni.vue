// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="my-3">
    <div class="row">
      <h3>Altri Fenomeni</h3>
      <div
        class="col-sm"
      >
        <MeteoText
          :id="'altri_fenomeni_' + altriFenomeni.id_time_layouts"
          :readonly="readonly"
          :data="altriFenomeni"
          :history="history"
          @set-level="setLevel"
        />
      </div>
    </div>
  </div>
</template>

<script>
import MeteoText from './MeteoText.vue'

export default {
  name: 'AltriFenomeni',
  components: {
    MeteoText,
  },
  props: {
    altriFenomeni: {
      type: Object,
      default: () => {
        return {
          id_w05_data: null,
          text_value: null
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
  emits: ['setLevel'],
  methods: {
    setLevel(id_w05_data, old_value, new_value, value_key) {
      this.$emit('setLevel', id_w05_data, old_value, new_value, value_key)
    }
  }
}
</script>
