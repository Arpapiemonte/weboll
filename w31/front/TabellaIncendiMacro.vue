// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt


<template>
  <table class="table">
    <thead>
      <tr>
        <th scope="col">
          Macroarea
        </th>
        <th scope="col">
          Denominazione 
        </th>
        <th scope="col">
          Livello
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="(area, index) in area_data"
        :key="index"
      >
        <th
          scope="row"
        >
          {{ area.id_w31_macroaree.id_w31_macroaree }}
        </th>
        <td
          scope="row"
        >
          {{ area.id_w31_macroaree.nome }}
        </td>
        <td>
          <select
            class="form-select"
            aria-label="Default select example"
            :disabled="readonly"
            :value="area.id_w31_livelli"
            @change="setValue(area, $event.target.value)"
          >
            <option
              v-for="livello in livelli"
              :key="livello.id_w31_livelli"
              :value="livello.id_w31_livelli"
            >
              {{ livello.id_w31_livelli }}
            </option>
          </select>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'TabellaIncendiMacro',
  props: {
    data:  {
      type: Array,
      default: null
    },
    livelli: {
      type: Array,
      default: () => []
    },
    readonly: {
      type: Boolean,
      default: false
    },
  },
  emits: ['saveW31Data'],
  computed: {
    area_data() {
      let vd = { }
      this.data.forEach(element => {
        vd[element.id_w31_macroaree.id_w31_macroaree] = element
      })
      return vd
    }
  },
  methods: {
    setValue(area, value) {
      // console.log(`setValue(${area}, ${value})`)
      this.$emit('saveW31Data', area, value)
    },
  }
}
</script>