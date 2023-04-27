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
      <h3>Zero Termico</h3>
      <div
        class="col-sm"
      >
        <MeteoText
          :id="'freezing_level_giornata_' + freezingLevelGiornata.id_time_layouts"
          :readonly="readonly"
          :data="freezingLevelGiornata"
          :history="history"
          @set-level="setLevel"
        />
      </div>
    </div>
    <div class="row my-3">
      <div
        v-if="freezingLevelMattino"
        class="col-sm"
      >
        <h5>Dalle 0 alle 12</h5>
        <p>
          Quota:
          <Level
            :readonly="readonly"
            :data="freezingLevelMattino"
            :history="history"
            :step="100"
            @set-level="setLevel"
          />
        </p>
        <ClassSelect
          :readonly="readonly"
          :data="classes0012"
          :classes-value="classDescription[classes0012.id_classes].classes_value"
          :history="history"
          @set-class="setClass"
        />
      </div>
      <div class="col-sm">
        <h5>Dalle 12 alle 24</h5>
        <p>
          Quota:
          <Level
            :readonly="readonly"
            :data="freezingLevelPomeriggio"
            :history="history"
            :step="100"
            @set-level="setLevel"
          />
        </p>
        <ClassSelect
          :readonly="readonly"
          :data="classes1224"
          :classes-value="classDescription[classes1224.id_classes].classes_value"
          :history="history"
          @set-class="setClass"
        />
      </div>
      <div
        v-if="classes0024"
        class="col-sm"
      >
        <h5>Dalle 00 alle 24</h5>
        <p>
          Quota:
          <Level
            :readonly="readonly"
            :data="freezingLevelGiornata"
            :history="history"
            :step="100"
            @set-level="setLevel"
          />
          <ClassSelect
            :readonly="readonly"
            :data="classes0024"
            :classes-value="classDescription[classes0024.id_classes].classes_value"
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
import Level from './Level.vue'

export default {
  name: 'ZeroTermico',
  components: {
    ClassSelect,
    MeteoText,
    Level,
  },
  props: {
    freezingLevelGiornata: {
      type: Object,
      default: () => {
        return {
          id_w05_data: null,
          text_value: null,
          numeric_value: null
        }
      }
    },
    freezingLevelMattino: {
      type: Object,
      default: () => {
        return {
          id_w05_data: null,
          numeric_value: null
        }
      }
    },
    freezingLevelPomeriggio: {
      type: Object,
      default: () => {
        return {
          id_w05_data: null,
          numeric_value: null
        }
      }
    },
    classes0024: {
      type: Object,
      default: () => null
    },
    classes0012: {
      type: Object,
      default: () => null
    },
    classes1224: {
      type: Object,
      default: () => null
    },
    classDescription: {
      type: Object,
      default: () => { return { 11: {}, 12: {}, 13: {} } }
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
