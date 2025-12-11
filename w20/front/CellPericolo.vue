// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <td
    :style="`background-color: ${coloreHtml()};`"
  >
    <select
      :name="String(area.id_w20_data + '_' + campo)"
      :value="area[campo]"
      class="form-select my-1"
      :disabled="readonly"
      @change="onChange"
    >
      <option
        v-for="per in pericolo"
        :key="per.id_w20_pericolo"
        :value="per.id_w20_pericolo"
      >
        {{ per.id_w20_pericolo }}
      </option>
    </select>
    <div
      v-if="debug"
      style="background-color: lightblue;"
    >
      <span>Value[{{ area[campo] }}]: {{ }}</span>
    </div>    
  </td>
</template>

<script setup lang="ts">

export interface Props {
  pericolo: {"id_w20_pericolo": string,"descrizione": string}[],
  area: {
    id_w20_data: number,
    if_perc: string,
    comune: string,
    provincia: string,
    id_w20: number
  },
  campo: string,
  readonly: boolean,
  required: boolean,
}

const props = withDefaults(defineProps<Props>(), {
  area: () => {
    return {
      id_w20_data: -1,
      if_perc: "A",
      comune: "np",
      provincia: "np",
      id_w20: -1
    }
  },
  readonly: true,
  required: true,
})

function coloreHtml() {
  var colore = 'red'
  if (props.area[props.campo] == 'A')
    colore = '#A6A6A6'
  else if (props.area[props.campo] == 'B')
    colore = '#9999FF'
  else if (props.area[props.campo] == 'E')
    colore = '#9900FF'
  return colore
}

const debug = false

const emit = defineEmits<{
  (e: "changePericolo", new_value: string, comune: string, campo: string): void
}>()

function onChange(e: Event) {
  const target = e.target as HTMLInputElement
  const new_value = target.value
  if (debug) console.log(`changePericolo(${new_value}, ${props.area.comune}, ${props.campo})`)
  emit("changePericolo", new_value, props.area.comune, props.campo)
}
</script>
