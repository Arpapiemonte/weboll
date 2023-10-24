// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <input
    type="number"
    data-bs-toggle="tooltip"
    data-bs-placement="top"
    :class="tabmode ? 'form-control col': ''"
    step="100"
    :value="roundedValue"
    :disabled="readonly"
    :style="tabmode ? snowLevelInfo ? 'width: 4em; border: #4169E1; border:2px solid #4169E1;' : 'width: 4em;' : snowLevelInfo ? 
      'height: 1.5em; width: 2.8em; font-size: 12px; background-color: white; border: #4169E1; border:2px solid #4169E1;' : 'height: 1.5em; width: 2.8em; font-size: 12px; background-color: white; color: #000000; border: #000000; border:1px solid #000000;'"
    @change="setmeasure"
  >
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    measure: number | null,
    idvenue: number | string,
    refresher: number,
    readonly: boolean,
    tabmode: boolean,
    snowLevelInfo: Boolean,
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
    emit('setmeasure', props.idvenue, value)
  }
}
</script>
