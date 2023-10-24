// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <ModaleLivelli
    :selected-shape="selected_shape"
    :selected-denominazione="selected_denominazione"
    :livelli="livelli"
    @save-level="saveLevel"
  />
  <div
    v-if="ready"
    class="container-fluid my-3 py-1"
  >
    <div
      class="row justify-content-end sticky-top py-1"
      style="background-color: #f8f9fa;"
    >
      <div
        class="btn-group w-auto mt-1 pt-1"
        role="group"
      >
        <div class="form-check form-switch">
          <input
            id="flexSwitchCheckDefault"
            v-model="switch_map"
            class="form-check-input"
            type="checkbox"
          >
          <label
            v-if="switch_map"
            class="form-check-label"
            for="flexSwitchCheckDefault"
          >Micro Aree</label>
          <label
            v-else
            class="form-check-label"
            for="flexSwitchCheckDefault"
          >Macro Aree</label>
        </div>
      </div>
      <div
        class="btn-group w-auto"
        role="group"
      >
        <div class="btn-group">
          <a
            class="btn btn-outline-primary"
            :href="'/api/w31/pdf/' + incendi.id_w31"
            target="_blank"
            role="button"
          >
            <img
              src="~bootstrap-icons/icons/file-earmark-pdf-fill.svg"
              alt="PDF icon"
              width="18"
              height="18"
            > PDF
          </a>
          <button
            v-if="incendi.status === '1' && state.username"
            type="button"
            class="btn btn-outline-warning"
            @click="execute('reopen', true, 'Bollettino riaperto')"
          >
            <span v-if="reopening">
              <span
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              />
              Sto riaprendo il bollettino ...
            </span>
            <span v-else>
              <img
                src="~bootstrap-icons/icons/unlock-fill.svg"
                alt="unlock icon"
                width="18"
                height="18"
              > Riapri
            </span>
          </button>
          <button
            v-if="incendi.status === '0' && state.username"
            type="button"
            class="btn btn-outline-success"
            @click="execute('send', false, 'Bollettino inviato')"
          >
            <span v-if="sending">
              <span
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              />
              Sto inviando il bollettino ...
            </span>
            <span v-else>
              <img
                src="~bootstrap-icons/icons/emoji-laughing.svg"
                alt="unlock icon"
                width="18"
                height="18"
              > Invia
            </span>
          </button>
          <button
            v-if="incendi.status === '0' && state.username"
            type="button"
            class="btn btn-outline-danger"
            @click="remove()"
          >
            <img
              src="~bootstrap-icons/icons/trash-fill.svg"
              alt="unlock icon"
              width="18"
              height="18"
            > Elimina
          </button>
        </div>
      </div>
    </div> <!-- row -->
    <div class="row mb-3">
      <h1>Bollettino Incendi {{ incendi.seq_num }}</h1>
    </div> <!-- row -->
    <div
      v-if="incendi.username ==='auto'"
      class="alert alert-danger"
    >
      Emissione effettuata con sistemi automatici
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="incendi.status == 1">
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Inviato"
            >
          </span>
          <span v-else-if="incendi.status == 2">
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Riaperto"
            >
          </span>
          <span v-else>
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Bozza"
            >
          </span>
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="dataEmissione">Data emissione
          <input
            id="dataEmissione"
            disabled
            class="form-control"
            type="text"
            :value="(new Date(incendi.start_valid_time)).toLocaleString()"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="dataAggiornamento">Ultima modifica
          <input
            id="dataAggiornamento"
            disabled
            class="form-control"
            type="text"
            :value="(new Date(incendi.last_update)).toLocaleString()"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="username">Autore
          <input
            id="username"
            disabled
            class="form-control"
            name="username"
            type="text"
            :value="incendi.username"
          >
        </label>
      </div>
    </div> <!-- row -->
    <div class="row mt-3">
      <div class="col-xl-8 col-md-12 mb-3">
        <ul
          class="nav nav-tabs nav-justified sticky-top"
          role="tablist"
        >
          <li
            v-for="(dataGiorno, index) in giorniBulletin"
            :key="index"
            class="nav-item"
            role="presentation"
          >
            <a
              class="nav-link"
              :class="{ active: current_day === index }"
              @click="current_day = index"
            >
              {{ dataGiorno }}
            </a>
          </li>
        </ul>
        <div v-if="switch_map">
          <TabellaIncendiMicro
            :data="incendi.micro[time_layouts[current_day]]"
          />
        </div>
        <div v-else>
          <TabellaIncendiMacro
            :data="incendi.macro[time_layouts[current_day]]"
            :livelli="livelli"
            :readonly="readonly"
            @save-w31-data="saveW31Data"
          />
        </div>
      </div>
      <div class="col-xl-4 col-md-12 mb-3">
        <div
          class="sticky-top"
          style="z-index: 0;"
        >
          <div v-if="switch_map">
            <MapIncendiMicro
              :venue-data="venue_data_micro"
            />
          </div>
          <div v-else>
            <MapIncendiMacro
              :readonly="readonly"
              :venue-data="venue_data_macro"
              @open-modal="openModal"
            />
          </div>
        </div>
      </div> <!-- end col-xl-5 -->
    </div> <!-- row -->
    <div class="row">
      <div class="col-md-12 mb-3">
        <table>
          <tbody>
            <tr>
              <td>
                <label for="annotazione">Campo note</label><br>
                <textarea
                  id="annotazione"
                  v-model="incendi.annotazione"
                  class="form-control"
                  name="annotazione"
                  rows="4"
                  cols="200"
                  :readonly="readonly"
                  @change="saveW31(incendi.annotazione, incendi.id_w31, 'annotazione')"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <img
      :src="`/api/static/images/loghi_progetti.png`"
      class="img-fluid rounded mx-auto d-block"
      :alt="`Loghi progetti`"
    >
  </div> <!-- end container-fluid -->
</template>

<script>
import Modal from 'bootstrap/js/dist/modal'
import api from '@/api'
import store from '@/store'
import TabellaIncendiMicro from './TabellaIncendiMicro.vue'
import TabellaIncendiMacro from './TabellaIncendiMacro.vue'
import MapIncendiMicro from './MapIncendiMicro.vue'
import MapIncendiMacro from './MapIncendiMacro.vue'
import ModaleLivelli from './ModaleLivelli.vue'

export default {
  name: 'IncendiBulletin',
  components: {
    MapIncendiMicro,
    MapIncendiMacro,
    TabellaIncendiMicro,
    TabellaIncendiMacro,
    ModaleLivelli
  },
  data () {
    // non reactive properties
    this.modaleLivelli = null
    this.time_layouts = ["49", "66", "83", "100", "117", "134", "151", "168", "185", "202", "219"]
    return {
      // reactive properties
      current_day: 0,
      incendi: {},
      livelli: [],
      readonly: true,
      ready: false,
      reopening: false,
      selected_denominazione: null,
      selected_shape: null,
      sending: false,
      state: store.state,
      switch_map: false
    }
  },
  computed: {
    today() {
      // returns today in 2021-04-22 format
      let d = new Date()
      return d.toISOString().substring(0, 10)
    },
    giorniBulletin() {
      const days = 9
      var bulletinDays = []
      var stringBulletinDays = Array(days).fill('')
      if ('start_valid_time' in this.incendi){
        var currentFullDate = new Date(this.incendi.start_valid_time)
        const startDay = currentFullDate.getDate()
        for(let i = 0; i < days ; i++){
          currentFullDate = new Date(this.incendi.start_valid_time)
          currentFullDate.setDate(startDay+i)
          bulletinDays[i] = new Date(currentFullDate.getTime())
          stringBulletinDays[i] = bulletinDays[i].getDate() + "/" + (bulletinDays[i].getMonth()+1)  + "/" +  bulletinDays[i].getFullYear()
        } 
      }
      return stringBulletinDays
    },
    venue_data_micro() {
      let vd = { }	
      this.incendi.micro[this.time_layouts[this.current_day]].forEach(element => {
        vd[element.id_w31_microaree.id_w31_microaree] = {
          color: this.livelli[element.id_w31_livelli - 1].colore,
          id_w31_livelli: element.id_w31_livelli,
        }
      })
      return vd
    },
    venue_data_macro() {
      let vdm = { }	
      this.incendi.macro[this.time_layouts[this.current_day]].forEach(element => {
        vdm[element.id_w31_macroaree.id_w31_macroaree] = {
          color: this.livelli[element.id_w31_livelli - 1].colore,
          id_w31_livelli: element.id_w31_livelli,
          denominazione: element.id_w31_macroaree.nome
        }
      })
      return vdm
    }
  },
  created() {
    // https://v3.vuejs.org/guide/composition-api-lifecycle-hooks.html#lifecycle-hooks
    this.ready = false
    this.getTest()
  },
  mounted: function () {
    this.$nextTick(() => {
      let modaleLivelliElement = document.getElementById('ModaleLivelli')
      this.modaleLivelli = new Modal(modaleLivelliElement)
      modaleLivelliElement.addEventListener('hidden.bs.modal', () => {
        this.selected_shape = 0
      })
    })
  },
  methods: {
    getTest() {
      this.incendi_id = this.$route.params.id
      if (typeof this.incendi_id === 'undefined') {
        return
      }
      this.fetchData()
    },
    fetchData () {
      this.fetchLevels().then(response => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero dei livelli`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json()
      }).then(data => {
        this.livelli = data
        this.fetchIncendi().then(response => {
          if (!response.ok) {
            this.$toast.open(
              {
                message: `Errore ${response.status} nel recupero del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
          }
          return response.json()
        }).then(data => {
          // console.log(`received data = ${JSON.stringify(data)}`)
          data.micro = { }
          if ('w31datamicroareelivelli_set' in data) {
            data.w31datamicroareelivelli_set.forEach((element) => {
              if (!(element.id_time_layouts in data.micro)) {
                data.micro[element.id_time_layouts] = []
              }
              data.micro[element.id_time_layouts].push(element)
            })
            delete data.w31datamicroareelivelli_set
          }
          data.macro = { }
          if ('w31datamacroareelivelli_set' in data) {
            data.w31datamacroareelivelli_set.forEach((element) => {
              if (!(element.id_time_layouts in data.macro)) {
                data.macro[element.id_time_layouts] = []
              }
              data.macro[element.id_time_layouts].push(element)
            })
            delete data.w31datamacroareelivelli_set
          }
          this.incendi = data
          this.readonly = (data.status === '1' || !this.state.username)
          this.ready = true
        }).catch(error => {
          this.$toast.open(
            {
              message: error,
              type: 'error',
              position: 'top-left'
            }
          )
        })
      }).catch(error => {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    fetchLevels () {
      const response = fetch('/api/w31/levels/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    fetchIncendi () {
      const response = fetch('/api/w31/bulletins/' + this.incendi_id + '/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    async bulkUpdateW31(payload) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w31/bulletins/bulk_update/`,
        {
          method: 'POST',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    async fetchPatch(id, endpoint, payload) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w31/${endpoint}/${id}/`,
        {
          method: 'PATCH',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    getDateFormatted(rawString) {
      return api.getDateFormatted(rawString)
    },
    saveW31(newValue, id_w31, campo) {
      const payload = { }
      if (campo) {
        payload[campo] = newValue
      }
      payload['id_w31'] = id_w31
      payload['username'] = store.state.username
      this.bulkUpdateW31(payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio bulk',
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json()
      }).then(data => {
        this.$toast.open(
          {
            message: 'Dato salvato',
            type: 'success',
            position: 'top-left'
          }
        )
        this.incendi.last_update = data.last_update
        this.incendi.username = store.state.username
      }).catch((error) => {
        this.$toast.open(
          {
            message: `Errore di comunicazione: ${error}`,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    updateW31(id_w31) {
      const payload = { }
      payload['id_w31'] = id_w31
      payload['username'] = store.state.username
      payload['version'] = this.incendi.version + 1
      this.bulkUpdateW31(payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio',
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json()
      }).then(data => {
        this.$toast.open(
          {
            message: 'Dato salvato',
            type: 'success',
            position: 'top-left'
          }
        )
        this.incendi.last_update = data.last_update
        this.incendi.username = store.state.username
        this.incendi.version = this.incendi.version + 1
      }).catch((error) => {
        this.$toast.open(
          {
            message: `Errore di comunicazione: ${error}`,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    saveLevel(value) {
      let area = this.incendi.macro[this.time_layouts[this.current_day]][this.selected_shape - 1]
      this.saveW31Data(area, value)
      this.modaleLivelli.hide()
    },
    saveW31Data(area, value) {
      const payload = { }
      let campo = 'id_w31_livelli' 
      if (value === 'N' || value === 'S') {
        campo = 'wind'
      }
      payload[campo] = value
      this.fetchPatch(area.id_w31_data_macroaree_livelli, 'data', payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio',
              type: 'error',
              position: 'top-left'
            }
          )
        } else {
          area[campo] = value
          this.updateW31(this.incendi.id_w31)
        }
        }).catch((error) => {
        this.$toast.open(
          {
            message: `Errore di comunicazione: ${error}`,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    async fetchAction(action) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w31/bulletins/${this.incendi.id_w31}/${action}/`
      )
      return response
    },
    execute(action, reroute, message) {
      this[action + 'ing'] = true
      this.fetchAction(action).then(response => {
        this[action + 'ing'] = false
        if (response.ok) {
          return response.json()
        } else {
          this.$toast.open(
            {
              message: `Errore ${response.status} nell'esecuzione del comando ${action}`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
      }).then(data => {
        this.$toast.open(
          {
            message: message,
            type: 'success',
            position: 'top-left'
          }
        )
        if (reroute) {
          this.$router.push({ path: `/w31/${data.id_w31}`})
          this.incendi_id = data.id_w31
          this.fetchData()
        } else {
          this.fetchData()
        }
      }).catch((error) => {
        this[action + 'ing'] = false
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    remove() {
      if (
        confirm('Vuoi davvero cancellare questo bollettino?')
      ) {
        api.fetchBulletinDelete(this.incendi.id_w31, 'w31/bulletins', store).then(response => {
          if (response.ok) {
            this.$toast.open(
              {
                message: 'Bollettino cancellato',
                type: 'success',
                position: 'top-left'
              }
            )
            this.bozza_presente = false
            this.$router.push({ path: `/w31`})
          } else {
            this.$toast.open(
              {
                message: `Errore ${response.status} nella cancellazione del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
          }
        }).catch((error) => {
          this.$toast.open(
            {
              message: error,
              type: 'error',
              position: 'top-left'
            }
          )
        })
      }
    },
    openModal(value) {
      this.selected_shape = value
      this.selected_denominazione = this.incendi.macro[this.time_layouts[this.current_day]][this.selected_shape - 1].id_w31_macroaree.nome
      this.modaleLivelli.show()
    },
  }
}
</script>
