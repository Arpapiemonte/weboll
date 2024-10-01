// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <Bulletins
    :primary-key-name="'id_w28'"
    :endpoint="'w28/bulletins'"
    :name="'A33'"
    :detail-page="'w28'"
    :pdf-endpoint="'w28/pdf'"
    :date-field="'start_valid_time'"
  >
    <template #th1="slotProps">
      <th
        scope="col"
        role="button"
        width="100px"
        @click="slotProps.sort('seq_num')"
      >
        Seq {{ slotProps.currentSort === 'seq_num' ? slotProps.currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
      </th>
      <th
        scope="col"
        role="button"
        width="300px"
        @click="slotProps.sort('start_valid_time')"
      >
        Data di emissione {{ slotProps.currentSort === 'start_valid_time' ? slotProps.currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
      </th>
    </template>
    <template #td1="slotProps">
      <td>{{ slotProps.bulletin['seq_num'] }}</td>
      <td>
        {{ getDateFormatted(slotProps.bulletin['start_valid_time']) }}
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
    }
  }
}
</script>
