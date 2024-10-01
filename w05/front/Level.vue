// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <input
    type="number"
    min="0"
    :max="max"
    :value="value"
    :disabled="readonly"
    :class="{dirty: history.isDirty(data.id_w05_data, 'id_w05_data', valueKey)}"
    :style="validity[data.id_w05_data] ? 'width: ' + width +'em;border:2px solid red;':'width: ' + width +'em;'"
    @change="$emit('setLevel', data.id_w05_data, data[valueKey], $event.target.value, valueKey)"
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
    },
    validity: {
      type: Object,
      default: () => { return {} }
    }
  },
  emits: ['setLevel'],
  computed: {
    value (){
      let index = this.history.snapshots.findIndex(
        element => element.id === this.data.id_w05_data
        && element.id_key === 'id_w05_data' 
        && element.value_key === this.valueKey)
      if (index < 0){
        if (!(this.data[this.valueKey] === null)){
          if (this.data[this.valueKey] === ''){
            return null
          }else{
            return Number(this.data[this.valueKey])
          }
        }
        return this.data[this.valueKey]
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
