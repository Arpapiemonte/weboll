// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    v-if="classDescription"
    class="my-3"
  >
    <div class="row">
      <h3>Precipitazioni</h3>
      <div
        class="col-sm"
      >
        <MeteoText
          :id="'livello_pioggia_' + livelloPioggia.id_time_layouts"
          :readonly="readonly"
          :data="livelloPioggia"
          :history="history"
          @set-level="setLevel"
        />
      </div>
    </div>
    <div class="row my-3">
      <div
        v-if="classes0012"
        class="col-sm"
      >
        <h5>Dalle 0 alle 12</h5>
        <p
          v-for="(c, index) in classes0012"
          :key="index"
          class="my-3"
        >
          <span>{{ classDescription[c.id_classes].description }}:</span>
          <ClassSelect
            :readonly="readonly"
            :data="c"
            :classes-value="classDescription[c.id_classes].classes_value"
            :history="history"
            @set-class="setClass"
          />
        </p>
      </div>
      <div class="col-sm">
        <h5>Dalle 12 alle 24</h5>
        <p
          v-for="(c, index) in classes1224"
          :key="index"
          class="my-3"
        >
          <span>{{ classDescription[c.id_classes].description }}:</span>
          <ClassSelect
            :readonly="readonly"
            :data="c"
            :classes-value="classDescription[c.id_classes].classes_value"
            :history="history"
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
  name: 'PrecipitazioniForm',
  components: {
    ClassSelect,
    MeteoText,
  },
  props: {
    livelloPioggia: {
      type: Object,
      default: () => {
        return {
          id_w05_data: null,
          text_value: null
        }
      }
    },
    classes0012: {
      type: Array,
      default: () => []
    },
    classes1224: {
      type: Array,
      default: () => []
    },
    classDescription: {
      type: Object,
      default: () => { return { 5: {}, 6: {}, 7: {}, 8: {} } }
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
