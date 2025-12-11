// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <Bulletins
    :primary-key-name="'id_w22'"
    :endpoint="'w22/bulletins'"
    :name="'Piene'"
    :detail-page="'w22'"
    :pdf-endpoint="'w22/pdf'"
    :date-field="'data_emissione'"
  >
    <template #th1="slotProps">
      <th
        scope="col"
        role="button"
        class="align-middle"
        width="100px"
        @click="slotProps.sort('numero_bollettino')"
      >
        Num {{ slotProps.currentSort === 'numero_bollettino' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
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
      <th
        scope="col"
        role="button"
        class="align-middle"
        width="100px"
        @click="slotProps.sort('ora_emissione')"
      >
        ora {{ slotProps.currentSort === 'ora_emissione' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
      <th
        scope="col"
        role="button"
        class="align-middle"
        width="100px"
        @click="slotProps.sort('pdf_ordinario')"
      >
        pdf ordinario {{ slotProps.currentSort === 'pdf_ordinario' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
    </template>
    <template #td1="slotProps">
      <td>{{ slotProps.bulletin['numero_bollettino'] }}</td>
      <td>
        {{ slotProps.bulletin['data_emissione'] }}
      </td>
      <td>{{ slotProps.bulletin['ora_emissione'] }}</td>
      <td>{{ slotProps.bulletin['pdf_ordinario'] }}</td>
    </template>
    <template #th2="slotProps">
      <th
        scope="col"
        role="button"
        class="align-middle"
        width="300px"
        @click="slotProps.sort('data_emissione')"
      >
        Data di validità {{ slotProps.currentSort === 'data_validita' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
      </th>
    </template>
    <template #td2="slotProps">
      <td>
        {{ slotProps.bulletin['data_validita'] }}
      </td>
    </template>
  </Bulletins>
</template>

<script>
// import api from '@/api'
import Bulletins from '@/components/Bulletins.vue'

export default {
  name: 'PieneBulletins',
  components: {
    Bulletins
  },
  methods: {
  }
}
</script>
