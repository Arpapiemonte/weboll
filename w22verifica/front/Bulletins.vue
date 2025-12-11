// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <Bulletins
    :primary-key-name="'id_w22verifica'"
    :endpoint="'w22verifica/bulletins'"
    :name="'PieneVerifica'"
    :detail-page="'w22verifica'"
    :pdf-endpoint="'w22verifica/pdf'"
    :date-field="'data_emissione'"
    :id-field="'id_w22verifica'"
  >
    <template #th1="slotProps">
      <th
        scope="col"
        role="button"
        class="align-middle"
        width="100px"
        @click="slotProps.sort('id_numero_bollettino')"
      >
        Num Piene {{ slotProps.currentSort === 'id_numero_bollettino' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
      <th
        scope="col"
        role="button"
        class="align-middle"
        width="300px"
        @click="slotProps.sort('data_emissione')"
      >
        Data di emissione Piene {{ slotProps.currentSort === 'data_emissione' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
      <th
        scope="col"
        role="button"
        class="align-middle"
        width="300px"
        @click="slotProps.sort('data_analisi')"
      >
        Data di verifica Piene {{ slotProps.currentSort === 'data_analisi' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
      <th
        scope="col"
        role="button"
        class="align-middle"
        width="300px"
        @click="slotProps.sort('id_w22giudizio')"
      >
        Giudizio {{ slotProps.currentSort === 'id_w22giudizio' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
    </template>
    <template #td1="slotProps">
      <td>{{ slotProps.bulletin['id_numero_bollettino'] }}</td>
      <td>
        {{ getDateFormatted_eng(slotProps.bulletin['data_emissione']) }}
      </td>
      <td>
        {{ getDateFormatted_eng(slotProps.bulletin['data_analisi']) }}
      </td>
      <td>{{ slotProps.bulletin['id_w22giudizio'] }}</td>
    </template>
  </Bulletins>
</template>

<script>
import api from '@/api'
import Bulletins from '@/components/Bulletins.vue'

export default {
  name: 'VerificaPieneBulletins',
  components: {
    Bulletins
  },
  methods: {
    getDateFormatted(rawString) {
      return api.getDateFormatted(rawString,false)
    },
    getDateFormatted_eng(rawString) {
      return api.getDateFormatted_eng(rawString, false)
    }
  }
}
</script>
