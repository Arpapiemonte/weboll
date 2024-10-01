// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <input
    type="number"
    class="form-control col"
    step="100"
    min="0" 
    max="6000"
    :value="roundedValue"
    :disabled="readonly"
    :style="tabFieldValidity ? '':'border:2px solid red;'"
    @change="setmeasure"
  >
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    measure: number | null,
    idW35Data: number,
    zona: string,
    campo: string,
    field: string,
    readonly: boolean,
    refresher: number,
    tabFieldValidity: boolean
}>()

const emit = defineEmits<{
  setmeasure: [idW35Data: number, campo: string, zona: string, field: string, value: number]
}>()

const roundedValue = computed(() => {
  let value = props.measure
  if(value === null){
    value === null
  }else if(value % 100 >= 50){
    value = 100 * Math.ceil(value / 100);
  }else{
    value = 100 * Math.floor(value / 100);
  }
  return value
})

function setmeasure() {
  if(window.event && window.event.target !== null){
    let value = parseInt((window.event.target as HTMLTextAreaElement).value)
    if(value % 100 >= 50){
        value = 100 * Math.ceil(value / 100);
    }else{
        value = 100 * Math.floor(value / 100);
    }
    emit('setmeasure', props.idW35Data, props.campo, props.zona, props.field, value)
  }
}
</script>
