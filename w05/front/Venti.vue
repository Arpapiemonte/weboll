// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    v-if="classDescription"
    class="my-3"
  >
    <div class="row">
      <h3>Venti</h3>
      <div
        class="col-sm"
      >
        <MeteoText
          :id="'velocita_vento_' + velocitaVento.id_time_layouts"
          :readonly="readonly"
          :data="velocitaVento"
          :history="history"
          :validity="validity"
          @set-level="setLevel"
        />
      </div>
    </div>
    <div class="row">
      <div class="col-sm my-3">
        <h5>Dalle 0 alle 24</h5>
        <p
          v-for="(c, index) in classes"
          :key="index"
          class="my-3"
        >
          <span>{{ classDescription[c.id_classes].description }}:</span>
          <ClassSelect
            :readonly="readonly"
            :data="c"
            :classes-value="classDescription[c.id_classes].classes_value"
            :history="history"
            :validity="validity"
            @set-class="setClass"
          />
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import ClassSelect from './ClassSelect.vue'
import MeteoText from './MeteoText.vue'

export default {
  name: 'VentiForm',
  components: {
    ClassSelect,
    MeteoText,
  },
  props: {
    velocitaVento: {
      type: Object,
      default: () => {
        return {
          id_w05_data: null,
          text_value: null
        }
      }
    },
    classes: {
      type: Array,
      default: () => []
    },
    classDescription: {
      type: Object,
      default: () => { return { 16: {}, 17: {}, 18: {}, 19: {}, 20: {}, 21: {} } }
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
