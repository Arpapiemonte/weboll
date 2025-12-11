// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div>
    <div class="row">
      <div class="col-md-8 mb-3">
        <span><b>{{ getWeekDay }}</b> {{ (getDateFormatted(coperturaNuvolosa.start_valid_time)).slice(0, 9) }} {{ giorno === 1 ? 'pomeriggio' : '' }}</span>
      </div>
      <div class="col-md-4 mb-3">
        <b>Attendibilità: </b>
        <Level
          :readonly="readonly"
          :data="previsioniMeteo"
          :history="history"
          :max="100"
          :step="5"
          :width="3"
          :value-key="'text_value'"
          @set-level="setLevel"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Level from './Level.vue'
import api from '@/api'

export default {
  name: 'ValidTime',
  components: {
    Level,
  },
  props: {
    coperturaNuvolosa: {
      type: Object,
      default: () => {
        return {
          start_valid_time: null,
          end_valid_time: null
        }
      }
    },
    previsioniMeteo: {
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
    },
      giorno: {
      type: Number,
      default: () => 0
    }
  },
  emits: ['setLevel'],
  computed: {
    getWeekDay(){
      let weekDays = ["Domenica", "Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato"]
      return weekDays[(new Date(this.coperturaNuvolosa.start_valid_time)).getDay()]
    }
  },
  methods: {
    setLevel(id_w05_data, old_value, new_value, value_key) {
      this.$emit('setLevel', id_w05_data, old_value, new_value, value_key)
    },
    getDateFormatted(rawString) {
      return api.getDateFormatted(rawString)
    }
  }
}
</script>
