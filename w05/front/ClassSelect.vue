// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <select
    :name="String(data.id_w05_classes)"
    :value="data.id_classes_value"
    :disabled="readonly"
    class="form-select my-3"
    :class="{
      dirty: history.isDirty(data.id_w05_classes, 'id_w05_classes', 'id_classes_value'),
      'is-invalid': validity[data.id_w05_classes]
    }"
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
  <div
    v-if="debug"
    style="background-color: lightblue;"
  >
    <span>Value[{{ data.id_w05_classes }}]: {{ data.id_classes_value }}</span>
  </div>
  <span
    v-if="validity[data.id_w05_classes]"
    :class="'text-danger'"
  >
    Questa classe deve essere impostata
  </span>
</template>

<script setup lang="ts">

export interface Props {
  data: {
    id_classes_value: number,
    id_w05_classes: number
  },
  classesValue: {
    id_classes_value: number,
    description: string
  }[],
  readonly: boolean,
  history: {
    isDirty: (id: number, id_key: string, value_key: string) => boolean,
    cursor: number,
    snapshots: any[]
  },
  required?: boolean,
  validity: object
}

const props = withDefaults(defineProps<Props>(), {
  data: () => {
    return {
      id_classes_value: 81,
      id_w05_classes: 42
    }
  },
  classesValue: () => [{id_classes_value: 81, description: "-"}],
  readonly: false,
  history: () => { return { isDirty: () => true, cursor: -1, snapshots: [] } },
  required: true,
  validity: () => { return {} },
})

const debug = false

const emit = defineEmits<{
  setClass: [id_w05_classes: number, old_value: number, new_value: number]
}>()

/*
const { errorMessage, meta, validate } = useField(String(props.data.id_w05_classes), validateField, {
  validateOnMount: true
})
*/

function validateField() {
  // console.log(`validateField(${props.data.id_w05_classes}, ${props.data.id_classes_value})`)
  if (!props.required) {
    return true // field is optional
  } if (props.data.id_classes_value !== undefined && props.data.id_classes_value <= 80) {
    return true
  } else {
    return 'Questa classe deve essere impostata'
  }
}

function onChange(e: Event) {
  const target = e.target as HTMLInputElement
  const old_value = props.data.id_classes_value
  const new_value = parseInt(target.value)
  emit("setClass", props.data.id_w05_classes, old_value, new_value)
}
</script>
