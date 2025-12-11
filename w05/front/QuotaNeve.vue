// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
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
        <h5>Valore di riferimento min dalle 00 alle 24</h5>
        <p>
          Quota:
          <Level
            :readonly="readonly"
            :style="validity_check(orderedData[1],orderedData[0]) ? 'border: #FFBF00; border:5px solid #FFBF00;' : ''"
            :data="orderedData[1]"
            :history="history"
            :step="100"
            :nullable="true"
            :validity="validity"
            @set-level="setLevel"
          />
        </p>
        <ClassSelect
          :readonly="true"
          :data="orderedClasses[1]"
          :classes-value="classDescription['14'].classes_value"
          :history="history"
          :required="false"
          :validity="validity"
          @set-class="setClass"
        />
      </div>
      <div class="col-sm">
        <h5>Valore di riferimento max dalle 00 alle 24 </h5>
        <p>
          Quota:
          <Level
            :readonly="readonly"
            :data="orderedData[0]"
            :history="history"
            :step="100"
            :nullable="true"
            :validity="validity"
            @set-level="setLevel"
          />
        </p>
        <ClassSelect
          :readonly="true"
          :data="orderedClasses[0]"
          :classes-value="classDescription['15'].classes_value"
          :history="history"
          :required="false"
          :validity="validity"
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
    },
    validity: {
      type: Object,
      default: () => { return {} }
    },
  },
  emits: ['setClass', 'setLevel'],
  computed: {
    orderedData(){
      // 0 => 909 => Massima
      // 1 => 910 => Minima
      const massima = this.data.find((element) => element.id_aggregazione == 909);
      const minima = this.data.find((element) => element.id_aggregazione == 910);
      return [massima,minima]
    },
    orderedClasses(){
      // 0 => 909 => Massima
      // 1 => 910 => Minima
      const massima = this.classes.find((element) => element.id_aggregazione == 909);
      const minima = this.classes.find((element) => element.id_aggregazione == 910);
      return [massima,minima]
    }
  },
  methods: {
    setClass(id_w05_classes, old_value, new_value) {
      this.$emit('setClass', id_w05_classes, old_value, new_value)
    },
    setLevel(id_w05_data, old_value, new_value, value_key) {
      this.$emit('setLevel', id_w05_data, old_value, new_value, value_key)
    },
    validity_check(min, max){
      //se min > max colora di arancione verifica che quota neve min non sia maggiore di quota neve max
      if(parseInt(min['numeric_value'])>parseInt(max['numeric_value']))  {
        return true
      } else {
        return false
      }
    }
  },
}
</script>
