// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <Bulletins
    :primary-key-name="'id_w23'"
    :endpoint="'w23/bulletins'"
    :name="'Allerta'"
    :detail-page="'w23'"
    :pdf-endpoint="'w23/pdf'"
    :date-field="'data_emissione'"
  >
    <template #th1="slotProps">
      <th
        scope="col"
        class="cursor-pointer align-middle"
        role="button"
        width="100px"
        @click="slotProps.sort('numero_bollettino')"
      >
        Seq {{ slotProps.currentSort === 'numero_bollettino' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
      <th
        scope="col"
        class="cursor-pointer align-middle"
        role="button"
        width="300px"
        @click="slotProps.sort('data_emissione')"
      >
        Data di emissione {{ slotProps.currentSort === 'data_emissione' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
    </template>
    <template #td1="slotProps">
      <td>{{ slotProps.bulletin['numero_bollettino'] }}</td>
      <td>
        {{ getDateFormattedNoTime_eng(slotProps.bulletin['data_emissione']) }}
      </td>
    </template>
    <template #th2="slotProps">
      <th
        scope="col"
        class="cursor-pointer align-middle"
        role="button"
        width="300px"
        @click="slotProps.sort('last_update_annotazione')"
      >
        Data ultima modifica annotazione {{ slotProps.currentSort === 'last_update_annotazione' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
    </template>
    <template #td2="slotProps">
      <td>{{ getDateFormatted_eng(slotProps.bulletin['last_update_annotazione']) }}</td>
    </template>
  </Bulletins>
</template>

<script>
import api from '@/api'
import Bulletins from '@/components/Bulletins.vue'

export default {
  name: 'AllertaBulletins',
  components: {
    Bulletins
  },
  methods: {
    getDateFormatted(rawString) {
      return api.getDateFormatted(rawString)
    },
    getDateFormattedNoTime(rawString) {
      return api.getDateFormatted(rawString, false)
    },
    getDateFormatted_eng(rawString) {
      return api.getDateFormatted_eng(rawString)
    },
    getDateFormattedNoTime_eng(rawString) {
      return api.getDateFormatted_eng(rawString, false)
    },
  }
}
</script>
