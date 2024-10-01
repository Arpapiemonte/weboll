// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <Bulletins
    :primary-key-name="'id_w37'"
    :endpoint="'w37/bulletins'"
    :name="'Aggiornamento Allerta'"
    :detail-page="'w37'"
    :pdf-endpoint="'w37/pdf'"
    :date-field="'data_emissione'"
  >
    <template #th1="slotProps">
      <th
        scope="col"
        role="button"
        width="100px"
        @click="slotProps.sort('numero_bollettino')"
      >
        numero bollettino {{ slotProps.currentSort === 'numero_bollettino' ? slotProps.currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
      </th>
      <th
        scope="col"
        role="button"
        width="300px"
        @click="slotProps.sort('data_emissione')"
      >
        Data di emissione {{ slotProps.currentSort === 'data_emissione' ? slotProps.currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
      </th>
      <th
        scope="col"
        role="button"
        width="300px"
        @click="slotProps.sort('ora_emissione')"
      >
        Ora di emissione {{ slotProps.currentSort === 'ora_emissione' ? slotProps.currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
      </th>
    </template>
    <template #td1="slotProps">
      <td>{{ slotProps.bulletin['numero_bollettino'] }}</td>
      <td>
        {{ getDateFormatted(slotProps.bulletin['data_emissione']) }}
      </td>
      <td>{{ slotProps.bulletin['ora_emissione'] }}</td>
    </template>
  </Bulletins>
</template>

<script>
import api from '@/api'
import Bulletins from '@/components/Bulletins.vue'

export default {
  name: 'PrevisioneBulletins',
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
