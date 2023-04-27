// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt


<template>
  <table class="table">
    <thead>
      <tr>
        <th scope="col">
          Microarea
        </th>
        <th scope="col">
          Livello
        </th>
        <th scope="col">
          Parametri
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
          {{ area.id_w31_microaree.id_w31_microaree }}
        </th>
        <td>
          {{ area.id_w31_livelli }}
        </td>
        <td>
          <table class="table">
            <thead>
              <tr>
                <th
                  v-for="(set) in area.w31datamicroareeparametri_set" 
                  :key="set"
                  scope="col"
                >
                  {{ set.id_parametro }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td
                  v-for="(set) in area.w31datamicroareeparametri_set"
                  :key="set"
                >
                  {{ set.numeric_value.toFixed(3) }}
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'TabellaIncendiMicro',
  props: {
    data:  {
      type: Array,
      default: null
    }
  },
  computed: {
    area_data() {
      let vd = { }
      this.data.forEach(element => {
        vd[element.id_w31_microaree.id_w31_microaree] = element
      })
      return vd
    }
  }
}
</script>
