// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <textarea
    :id="id"
    :name="id"
    :value="data[valueKey]"
    class="form-control"
    rows="2"
    :readonly="readonly"
    :class="{
      dirty: history.isDirty(data[idKey], idKey, valueKey),
      'is-invalid': meta && meta.validated ? !meta.valid : false
    }"
    @change="onChange"
  />
  <div
    v-if="debug"
    style="background-color: lightblue;"
  >
    <span>Value[{{ id }}]: {{ data[valueKey] }}</span>
    <br>
    <code>
      {{ meta }}
    </code>
  </div>
  <span
    v-if="meta.validated && !meta.valid"
    :class="'text-danger'"
  >
    Campo non compilato
  </span>
</template>

<script setup lang="ts">
import { useField } from 'vee-validate'
import { watch } from "vue"

export interface Props {
  data: {
    note: string,
    text_value: string,
    id_w16_data: number,
    id_w16: number,
  },
  readonly: boolean,
  history: {
    isDirty: (id: number, id_key: string, value_key: string) => boolean,
    cursor: number,
    snapshots: any[]
  },
  id: string,
  valueKey: string,
  idKey: string,
}

const props = withDefaults(defineProps<Props>(), {
  data: () => {
    return {
      note: "",
      text_value: "",
      id_w16_data: 0,
      id_w16: 0
    }
  },
  readonly: false,
  history: () => { return { isDirty: () => true, cursor: -1, snapshots: [] } },
  id: "",
  valueKey: "text_value",
  idKey: "id_w05_data"
})

const debug = false

const emit = defineEmits<{
  (e: "setNote", id_w16: number, old_value: string, new_value: string): void
}>()

const { errorMessage, meta, validate } = useField(String(props.id), validateField, {
  validateOnMount: true
})

function validateField() {
  let value = props.data[props.valueKey]
  // console.log(`validateField(props.data[${props.valueKey}]) = ${value}`)
  if (value && value.trim()) {
    return true
  } else {
    return 'Questo campo è richiesto'
  }
}

function onChange(e: Event) {
  const target = e.target as HTMLInputElement
  const new_value = target.value
  emit('setNote', props.data[props.idKey], props.data[props.valueKey], new_value)
}

watch(props, () => {
  validate()
}, { immediate: true, deep: true });
</script>