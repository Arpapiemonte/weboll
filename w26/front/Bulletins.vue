// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <W26Modal 
    :updatew26fetch="updatew26fetch"
    @create-w26="createW26"
  />
  <Bulletins
    :primary-key-name="'id_w26'"
    :endpoint="'w26/bulletins'"
    :name="'BIS'"
    :detail-page="'w26'"
    :pdf-endpoint="'w26/pdf'"
    :date-field="'data_emissione'"
    :id-field="'numero_bollettino'"
  > 
    <template #openW26modal>
      <button
        :disabled="creating"
        class="btn btn-sm btn-outline-primary"
        type="button"
        @click="openW26modal()"
      >
        <span v-if="creating">
          <span
            class="spinner-border spinner-border-sm"
            role="status"
            aria-hidden="true"
          />
          Sto creando il bollettino ...
        </span>
        <span v-else>Crea bollettino</span>
      </button>
    </template>
    <template #th1="slotProps">
      <th
        scope="col"
        role="button"
        width="100px"
        @click="slotProps.sort('numero_bollettino')"
      >
        Seq {{ slotProps.currentSort === 'numero_bollettino' ? slotProps.currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
      </th>
      <th
        scope="col"
        role="button"
        width="200px"
        @click="slotProps.sort('data_validita')"
      >
        Data Validità {{ slotProps.currentSort === 'data_validita' ? slotProps.currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
      </th>
      <th
        scope="col"
        role="button"
        width="200px"
        @click="slotProps.sort('data_emissione')"
      >
        Data di emissione {{ slotProps.currentSort === 'data_emissione' ? slotProps.currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
      </th>
    </template>
    <template #td1="slotProps">
      <td>{{ slotProps.bulletin['numero_bollettino'] }}</td>
      <td>{{ getDateFormatted(slotProps.bulletin['data_validita']) }}</td>
      <td>
        {{ getDateFormatted(slotProps.bulletin['data_emissione']) }}
      </td>
    </template>
  </Bulletins>
</template>

<script>
import { Modal } from 'bootstrap'

import 'vue-toast-notification/dist/theme-default.css'
import api from '@/api'
import store from '@/store'
import Bulletins from '@/components/Bulletins.vue'
import W26Modal from './W26Modal.vue'

export default {
  name: 'BisBulletins',
  components: {
    Bulletins,
    W26Modal,
  },
  data () {
    return {
      updatew26fetch: 0,
      w26Modal: {},
      creating: false,
      state: store.state,
    }
  },
  mounted() {
    let w26ModalElement = document.getElementById('w26Modal')
    this.w26Modal = new Modal(w26ModalElement)
  },
  methods: {
    getDateFormatted(rawString) {
      return api.getDateFormatted(rawString,false)
    },
    openW26modal(){
      this.updatew26fetch += 1
      this.w26Modal.show()
    },
    createW26(validita) {
      this.creating = true
      this.fetchBulletinNewW26(validita).then(async response => {
        this.creating = false
        if (response.ok) {
          this.$toast.open(
            {
              message: 'Bollettino creato',
              type: 'success',
              position: 'top-left'
            }
          )
          var tmp = await response.json()
          this.$router.push({ path: `/w26/${tmp['id_w26']}`})
        } else {
          this.$toast.open(
            {
              message: `Errore ${response.status} nella creazione del bollettino`,
              type: 'error',
              position: 'top-left'
            }
          )
          this.creating = false
          if (response.status === 401 || response.status === 403) {
            this.$refs.login.show()
            return null
          }
        }
      }).catch((error) => {
        this.creating = false
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    async fetchBulletinNewW26 (validita) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w26/bulletins/new/${validita}/`
      )
      return response
    },
  }
}
</script>
