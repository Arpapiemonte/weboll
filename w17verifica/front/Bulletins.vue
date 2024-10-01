// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
/ Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <Bulletins
    :primary-key-name="'id_w17verifica'"
    :endpoint="'w17verifica/bulletins'"
    :name="'Verifica Meteo'"
    :detail-page="'w17verifica'"
    :pdf-endpoint="'w17verifica/pdf'"
    :date-field="'data_emissione'"
  >
    <template #th1="slotProps">
      <th
        scope="col"
        role="button"
        width="300px"
        @click="slotProps.sort('data_emissione')"
      >
        Data di emissione {{ slotProps.currentSort === 'data_emissione' ? slotProps.currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
      </th>
    </template>
    <template #td1="slotProps">
      <td>
        {{ getDateFormatted(slotProps.bulletin['data_emissione']) }}
      </td>
    </template>
    <template #th2="slotProps">
      <th
        scope="col"
        role="button"
        width="300px"
        @click="slotProps.sort('data_analysis')"
      >
        Data Analisi {{ slotProps.currentSort === 'data_analysis' ? slotProps.currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
      </th>
    </template>
    <template #td2="slotProps">
      <td>
        {{ getDateFormatted(slotProps.bulletin['data_analysis']) }}
      </td>
    </template>
  </Bulletins>
</template>

<script>
import api from '@/api'
import Bulletins from '@/components/Bulletins.vue'

export default{
  name: 'VerificaMeteoBulletins',
  components: {
    Bulletins
  },
  methods: {
    getDateFormatted(rawString) {
      return api.getDateFormatted(rawString, false)
    }
  }
}
</script>
