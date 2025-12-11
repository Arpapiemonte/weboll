// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <Bulletins
    :primary-key-name="'id_w06'"
    :endpoint="'w06/bulletins'"
    :name="'A6'"
    :detail-page="'w06'"
    :pdf-endpoint="'w06/pdf'"
    :date-field="'start_valid_time'"
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
        @click="slotProps.sort('start_valid_time')"
      >
        Data di emissione {{ slotProps.currentSort === 'start_valid_time' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
    </template>
    <template #td1="slotProps">
      <td>{{ slotProps.bulletin['seq_num'] }}</td>
      <td>
        {{ getDateFormatted_eng(slotProps.bulletin['start_valid_time']) }}
      </td>
    </template>
  </Bulletins>
</template>

<script>
import api from '@/api'
import Bulletins from '@/components/Bulletins.vue'

export default {
  name: 'A6Bulletins',
  components: {
    Bulletins
  },
  methods: {
    getDateFormatted(rawString) {
      return api.getDateFormatted(rawString)
    },
    getDateFormatted_eng(rawString) {
      return api.getDateFormatted_eng(rawString)
    }
  }
}
</script>
