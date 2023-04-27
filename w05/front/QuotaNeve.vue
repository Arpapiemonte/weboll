// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    v-if="classDescription"
    class="my-3"
  >
    <div
      v-if="data"
      class="row"
    >
      <h3>Quota neve</h3>
      <div class="col-sm">
        <h5>Valore di riferimento min</h5>
        <p>
          Quota:
          <Level
            :readonly="readonly"
            :data="data[1]"
            :history="history"
            :step="100"
            :nullable="true"
            @set-level="setLevel"
          />
        </p>
        <ClassSelect
          :readonly="readonly"
          :data="classes[0]"
          :classes-value="classDescription[classes[0].id_classes].classes_value"
          :history="history"
          :required="false"
          @set-class="setClass"
        />
      </div>
      <div class="col-sm">
        <h5>Valore di riferimento max</h5>
        <p>
          Quota:
          <Level
            :readonly="readonly"
            :data="data[0]"
            :history="history"
            :step="100"
            :nullable="true"
            @set-level="setLevel"
          />
        </p>
        <ClassSelect
          :readonly="readonly"
          :data="classes[1]"
          :classes-value="classDescription[classes[1].id_classes].classes_value"
          :history="history"
          :required="false"
          @set-class="setClass"
        />
      </div>
    </div>
  </div>
</template>

<script>
import ClassSelect from './ClassSelect.vue'
import Level from './Level.vue'

export default {
  name: 'QuotaNeve',
  components: {
    ClassSelect,
    Level,
  },
  props: {
    data: {
      type: Array,
      default: null
    },
    classes: {
      type: Array,
      default: () => []
    },
    classDescription: {
      type: Object,
      default: () => { return { 14: {}, 15: {} } }
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
  emits: ['setClass', 'setLevel'],
  methods: {
    setClass(id_w05_classes, old_value, new_value) {
      this.$emit('setClass', id_w05_classes, old_value, new_value)
    },
    setLevel(id_w05_data, old_value, new_value, value_key) {
      this.$emit('setLevel', id_w05_data, old_value, new_value, value_key)
    }
  }
}
</script>
