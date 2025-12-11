// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <select
    :value="data.id_trend"
    :name="String(data.id_trend)"
    :disabled="readonly"
    class="form-select"
    @change="onChange"
  >
    <option
      v-for="(d, j) in trend"
      :key="j"
      :value="d.id_trend"
    >
      {{ d.desc_ita }}
    </option>
  </select>
</template>

<script setup lang="ts">

import { components } from '../../src/types/weboll'
type W17Data = components['schemas']['W17Data']
type Trend = components["schemas"]["Trend"]

export interface Props {
  data: W17Data,
  trend: Trend[],
  readonly: boolean,
}

const props = withDefaults(defineProps<Props>(), {
  data: () => {
    return {
      id_w17_data: 0,
      numeric_value: null,
      id_trend: 0 ,
      text_value: "",
      id_w17: 0,
      id_venue: 0,
      id_time_layouts: 0,
      id_parametro: "",
      id_aggregazione: 0,
      cod_staz_meteo: null,
    }
  },
  trend: () => [{
    desc_eng: "",
    desc_ita: "",
    id_trend: 0,
    id_web: 0,
    last_update: "2006-11-13T12:58:20",
    username: "weboll",
    title: "",
  }],
  readonly: true,
})


const emit = defineEmits<{
  setTrend: [id_parametro: string, id_time_layouts: number, id_classes: number, id_aggregazione: number, new_value: number]
}>()

function onChange(e: Event) {
  //console.log("onChange", e.target)
  const target = e.target as HTMLInputElement
  // const old_value = props.data.id_trend
  const new_value = parseInt(target.value)
  console.log("new_value", new_value)
  emit("setTrend",  props.data.id_parametro, props.data.id_time_layouts, props.data.id_venue, props.data.id_aggregazione, new_value)
}

</script>
