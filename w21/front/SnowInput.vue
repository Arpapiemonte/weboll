// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <input
    type="number"
    class="form-control col"
    step="100"
    :value="roundedValue"
    :disabled="readonly"
    @change="setmeasure"
  >
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    measure: number | null | string,
    idW21Data: number,
    campo: string,
    refresher: number,
    readonly: boolean
}>()

const emit = defineEmits(['setmeasure'])

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
    emit('setmeasure', props.idW21Data, props.campo, value)
  }
}
</script>
