// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <td
    :style="`background-color: ${coloreHtml()};`"
  >
    <select
      :name="String(area.id_w29_data + '_' + campo)"
      :value="area[campo]"
      class="form-select my-1"
      :class="{
        'is-invalid': !validity[area.id_w29_data][campo]
      }"
      :disabled="readonly"
      @change="onChange"
    >
      <option
        v-for="per in pericolo"
        :key="per.id_w29_pericolo"
        :value="per.id_w29_pericolo"
      >
        {{ per.id_w29_pericolo }}
      </option>
    </select>
    <div
      v-if="debug"
      style="background-color: lightblue;"
    >
      <span>Value[{{ area[campo] }}]: {{ }}</span>
      <br>
      <span
        v-if="!validity[area.id_w29_data][campo]"
        :class="'text-danger'"
      >
        Questo campo è richiesto
      </span>
    </div>    
  </td>
</template>

<script setup lang="ts">
import { watch } from "vue";

export interface Props {
  pericolo: {"id_w29_pericolo": string,"descrizione": string}[],
  area: {
    id_w29_data: number,
    id_w29_zone: {
      id_w29_zone: number,
      descrizione: string
    },
    livello_criticita_oss: string,
    probabilita_criticita_oss: string,
    livello_criticita_prev_oggi: string,
    probabilita_criticita_prev_oggi: string,
    livello_criticita_prev_domani: string,
    probabilita_criticita_prev_domani: string,
    id_w29: number
  },
  campo: string,
  readonly: boolean,
  required: boolean,
  validity: object
}

const props = withDefaults(defineProps<Props>(), {
  area: () => {
    return {
      id_w29_data: -1,
      id_w29_zone: {
        id_w29_zone: -1,
        descrizione: "np"
      },
      livello_criticita_oss: "np",
      probabilita_criticita_oss: "nessuna",
      livello_criticita_prev_oggi: "np",
      probabilita_criticita_prev_oggi: "nessuna",
      livello_criticita_prev_domani: "np",
      probabilita_criticita_prev_domani: "nessuna",
      id_w29: -1
    }
  },
  readonly: true,
  required: true,
  validity: () => { return {}}
})

function coloreHtml() {
  var colore = 'red'
  if (props.area[props.campo] == 'np')
    colore = 'black'
  else if (props.area[props.campo] == '-')
    colore = '#A6A6A6'
  else if (props.area[props.campo] == '1')
    colore = '#99CCFF'
  else if (props.area[props.campo] == '2')
    colore = '#9999FF'
  else if (props.area[props.campo] == '3')
    colore = '#9900FF'
  return colore
}

const debug = false

const emit = defineEmits<{
  changePericolo: [new_value: string, id_29_zone: number, campo: string]
}>()

/*
const { errorMessage, meta, validate } = useField(String(props.area.id_w29_data + '_' + props.campo), validateField, {
  validateOnMount: true
})
*/

function validateField() {
  if (debug) console.log(`validateField(${props.required}, ${props.area[props.campo]})`)
  if (!props.required) {
    return true // field is optional
  } if (props.area[props.campo] !== 'np') {
    return true
  } else {
    return false
  }
}

function onChange(e: Event) {
  const target = e.target as HTMLInputElement
  const new_value = target.value
  if (debug) console.log(`changePericolo(${new_value}, ${props.area.id_w29_zone.id_w29_zone}, ${props.campo})`)
  emit("changePericolo", new_value, props.area.id_w29_zone.id_w29_zone, props.campo)
}

/*
watch(props, () => {
  validate()
}, { immediate: true, deep: true });
*/
</script>
