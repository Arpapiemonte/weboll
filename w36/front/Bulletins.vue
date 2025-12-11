// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <Bulletins
    :primary-key-name="'id_w36'"
    :endpoint="'w36/bulletins'"
    :name="'Caldo'"
    :detail-page="'w36'"
    :pdf-endpoint="'w36/pdf'"
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
        Num {{ slotProps.currentSort === 'seq_num' ? slotProps.currentSortDir === '' ? '▲' : '▼' : ' ' }}
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
        {{ slotProps.bulletin['data_emissione'] }}
      </td>
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
  name: 'CaldoBulletins',
  components: {
    Bulletins
  },
  methods: {
  }
}
</script>
