// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <input
    style="width: 4em;"
    type="number"
    min="-30"
    max="50"
    :value="value"
    :disabled="readonly"
    :class="{dirty: history.isDirty(data.id_w05_data, 'id_w05_data', 'numeric_value')}"
    :style="validity[data.id_w05_data] ? 'border:2px solid red;':''"
    @change="$emit('setLevel', data.id_w05_data, data.numeric_value, $event.target.value)"
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
    },
    validity: {
      type: Object,
      default: () => { return {} }
    },
  },
  emits: ['setLevel'],
  computed: {
    value (){
      let index = this.history.snapshots.findIndex(
        element => element.id === this.data.id_w05_data
        && element.id_key === 'id_w05_data' 
        && element.value_key === 'numeric_value')
      if (index < 0){
        if (!(this.data.numeric_value === null)){
          if (this.data.numeric_value === ''){
            return null
          }else{
            return Number(this.data.numeric_value)
          }
        }
        return this.data.numeric_value
      }else{
        if (!(this.history.snapshots[index].new_value === null)){
          if (this.history.snapshots[index].new_value === ''){
            return null
          }else{
            return Number(this.history.snapshots[index].new_value)
          }
        }
        return this.history.snapshots[index].new_value
      }
    }
  }
}
</script>
