// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <select
    :name="String(data.id_w12_data + campo)"
    :value="data[campo]"
    class="form-select"
    :style="validity ? 'border: #FF5C5C; border:3px solid #FF5C5C;' : ''"
    :disabled="readonly"
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
type W12Data = components['schemas']['W12Data']

export interface Props {
  data: W12Data,
  classesValue: {
    id_classes_value: number | null,
    description: string
  }[],
  campo: string,
  validity: boolean,
  readonly: boolean,
}

const props = withDefaults(defineProps<Props>(), {
  data: () => {
    return {
      id_w12_data: 0,
      cloud_amount: null,
      precipitation_class: null,
      cumulated_snow: null,
      freezing_level: null,
      snow_level: null,
      temperature_below_zero: false,
      risk_freezing_rain: false,
      vis_inf_1000: false,
      vis_inf_1000_reason: null,
      wind_class: null,
      id_w12: 0,
      id_venue: 0,
      id_time_layouts: 0,
      id_sky_condition: 0,
    }
  },
  classesValue: () => [{id_classes_value: 81, description: "-"}],
  campo: "",
  validity: false,
  readonly: true,
})


const emit = defineEmits<{
  (e: "setClass", id_w12_data: number, campo: string, new_value: number): void
}>()

function onChange(e: Event) {
  const target = e.target as HTMLInputElement
  const new_value = parseInt(target.value)
  emit("setClass", props.data.id_w12_data, props.campo, new_value)
}

</script>
