// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <Bulletins
    :primary-key-name="'id_w33'"
    :endpoint="'w33/bulletins'"
    :name="'Metaprodotto'"
    :detail-page="'w33'"
    :pdf-endpoint="'w33/pdf'"
    :date-field="'data_emissione'"
  >
    <template #th1="slotProps">
      <th
        scope="col"
        role="button"
        class="align-middle"
        width="100px"
        @click="slotProps.sort('seq_num')"
      >
        Seq {{ slotProps.currentSort === 'seq_num' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
      <th
        scope="col"
        role="button"
        class="align-middle"
        width="300px"
        @click="slotProps.sort('data_emissione')"
      >
        Data di emissione {{ slotProps.currentSort === 'data_emissione' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
    </template>
    <template #td1="slotProps">
      <td>{{ slotProps.bulletin['seq_num'] }}</td>
      <td>
        {{ getDateFormatted_eng(slotProps.bulletin['data_emissione']) }}
      </td>
    </template>
  </Bulletins>
</template>

<script>
import api from '@/api'
import Bulletins from '@/components/Bulletins.vue'

export default {
  name: 'MetaprodottoBulletins',
  components: {
    Bulletins
  },
  methods: {
    getDateFormatted(rawString) {
      return api.getDateFormatted(rawString)
    },
    getDateFormatted_eng(rawString) {
      return api.getDateFormatted_eng(rawString, false)
    }
  }
}
</script>
