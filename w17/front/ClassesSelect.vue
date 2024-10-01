// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <label
    class="form-label"
  >{{ title }}</label>
  <select
    :value="data.id_classes_value"
    :name="String(data.id_w17_classes)"
    :disabled="readonly"
    :style="validity ? 'border: #FF0000; border:3px solid #FF0000;' : ''"
    class="form-select"
    @change="onChange"
  >
    <option
      v-for="(d, j) in classesValue"
      :key="j"
      :value="d.id_classes_value"
    >
      {{ d.description }}
    </option>
  </select>
</template>

<script setup lang="ts">

import { components } from '../../src/types/weboll'
type W17Classes = components['schemas']['W17Classes']

export interface Props {
  data: W17Classes,
  classesValue: {
    id_classes_value: number,
    description: string
  }[],
  title: string,
  readonly: boolean,
  validity: boolean,
}

const props = withDefaults(defineProps<Props>(), {
  data: () => {
    return {
      id_w17_classes: 2,
      id_w17: 3408,
      id_parametro: "COP_TOT",
      id_classes_value: 3,
      id_classes: 1,
      id_time_layouts: 30
    }
  },
  classesValue: () => [{id_classes_value: 81, description: "-"}],
  title: "",
  readonly: true,
  validity: false,
})


const emit = defineEmits<{
  setClass: [id_parametro: string, id_time_layouts: number, id_classes: number, new_value: number]
}>()

function onChange(e: Event) {
  //console.log("onChange", e.target)
  const target = e.target as HTMLInputElement
  //const old_value = props.data.id_classes_value
  const new_value = parseInt(target.value)
  emit("setClass", props.data.id_parametro, props.data.id_time_layouts,  props.data.id_classes, new_value)
}

</script>
