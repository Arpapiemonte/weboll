// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <table class="table table-striped">
    <thead>
      <tr>
        <th scope="col">
          Venue
        </th>
        <th scope="col">
          SkyCondition
        </th>
        <th scope="col">
          Neve<br>Cumulata<br>(cm)
        </th>
        <th scope="col">
          Quota<br>Neve<br>(m)
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="tratto in values"
        :key="tratto.id_w33_data"
      >
        <th scope="row">
          <span
            class="badge"
            :style="'font-size: large;background-color:' + autostradeColors[venueNames[tratto.id_venue].substring(0,3).trim().toLowerCase()] + ';'"
          >
            {{ venueNames[tratto.id_venue].substring(0,3) }}
          </span>
          {{ venueNames[tratto.id_venue].substring(3,venueNames[tratto.id_venue].length) }} ({{ heights[tratto.id_venue].min }}-{{ heights[tratto.id_venue].max }} m)
        </th>
        <th scope="row">
          <select
            :value="tratto.id_sky_condition"
            :disabled="readonly"
            style="width: 12em;"
            class="form-select col"
            :style="skycondValidity[tratto.id_venue] ? 'border: 3px solid #FFA500' : ''"
            @change="setMeasure(tratto.id_venue, 'id_sky_condition')"
          >
            <option
              v-for="(d, j) in icons"
              :key="j"
              :value="d.id_sky_condition"
            >
              {{ d.description_ita }}
            </option>
          </select>
        </th>
        <td>
          <input
            v-model="tratto.cumulated_snow"
            type="Number"
            class="form-control col"
            style="width: 4em;"
            :style="cumulatedSnowValidity[tratto.id_venue] ? 'border: #FFA500; border:3px solid #FFA500;' : ''"
            title="Neve cumulata"
            :disabled="readonly"
            @change="setMeasure(tratto.id_venue, 'cumulated_snow')"
          >
        </td>
        <td>
          <SnowLevelInput 
            :measure="tratto.snow_level"
            :idvenue="tratto.id_venue"
            :readonly="readonly"
            :refresher="refresher"
            :snow-level-info="snowLevelInfo[tratto.id_venue]"
            :tabmode="true"
            @setmeasure="setSnowLevel"
          />
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script lang="ts">
import SnowLevelInput from './SnowLevelInput.vue'

export default {
  name: 'NeveMap',
  components: {
    SnowLevelInput,
  }
}
</script>

<script setup lang="ts">
import { ref, computed } from 'vue'

import { components } from '../../src/types/weboll'
import type { Icons } from "../types"

type W33Data = components['schemas']['W33Data']

const props = defineProps<{
    readonly: Boolean,
    datatab: Array<W33Data>,
    autostradeColors: Object,
    cumulatedSnowValidity: Object,
    snowLevelInfo: Object,
    skycondValidity: Object,
    heights: Object,
    venueNames: Object,
    icons: Icons,
}>()

let refresher = ref(0)

const venueOrder = [
  105, 
  104, 
  103, 
  102, 
  101, 
  100, 
  99,
  94,
  95,
  96,
  97, 
  47, 
  25, 
  19, 
  41,
  66,
  106,
  49,
  107,
  24,
  108, 
  187, 
  188, 
  189
]

const emit = defineEmits<{
  saveW33Data: [id_venue: string, campo: string, new_value: number],
  setNeve: [id_venue: number, campo: string, new_value: number]
}>()

const values = computed(() => {
    let values : Array<W33Data> = []
    let tmpvalues = props.datatab
    venueOrder.forEach(e => {
      let tratto = tmpvalues.find(v => v.id_venue === e)
      if(tratto){
        values.push(tratto)
      }
    })
    return values
})

function forceUpdate(){
  refresher.value += 1
}

function setSnowLevel(id_venue, new_value){
  emit('setNeve', parseInt(id_venue), 'snow_level', new_value)
  forceUpdate()
}

function setMeasure(id_venue, campo){
    if(window.event && window.event.target !== null){
        console.log(parseInt((window.event.target as HTMLInputElement).value))
        emit('saveW33Data', id_venue, campo, parseInt((window.event.target as HTMLInputElement).value))
    }
}

</script>