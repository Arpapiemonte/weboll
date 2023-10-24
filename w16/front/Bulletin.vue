// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <LoginModal ref="login" />
  <VeeForm>
    <div class="container-fluid">
      <LevelModal
        :selected-venue="selected_venue"
        :levels="levels"
        @set-selected-level="setSelectedLevel"
      />
      <MeteoModal />

      <div
        class="row justify-content-end sticky-top py-1"
        style="background-color: #f8f9fa;"
      >
        <div
          class="btn-group w-auto"
          role="group"
        >
          <a
            class="btn btn-outline-primary"
            :href="'/api/w16/pdf/' + ozono.id_w16"
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
            v-if="ozono.last_seq_num === ozono.seq_num && state.username"
            :disabled="copying || reopening || sending"
            type="button"
            class="btn btn-outline-dark"
            @click="execute('copy', true, 'Bollettino copiato')"
          >
            <span v-if="copying">
              <span
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              />
              Sto copiando il bollettino ...
            </span>
            <span v-else>
              <img
                src="~bootstrap-icons/icons/plus-circle-fill.svg"
                alt="plus icon"
                width="18"
                height="18"
              > Copia
            </span>
          </button>
          <button
            v-if="ozono.status === '1' && state.username"
            :disabled="copying || reopening || sending"
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
            v-if="ozono.status === '0' && state.username"
            :disabled="history.canUndo || reopening || sending"
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
            v-if="ozono.status === '0' && state.username"
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
        <div
          v-if="!readonly"
          class="btn-group w-auto"
          role="group"
        >
          <button
            type="button"
            class="btn btn-success"
            :disabled="!history.canUndo"
            @click="undo()"
          >
            <img
              src="~bootstrap-icons/icons/arrow-counterclockwise.svg"
              alt="undo icon"
              width="18"
              height="18"
            > Undo
          </button>
          <button
            type="button"
            class="btn btn-info"
            :disabled="!history.canRedo"
            @click="redo()"
          >
            <img
              src="~bootstrap-icons/icons/arrow-clockwise.svg"
              alt="redo icon"
              width="18"
              height="18"
            > Redo
          </button>
          <button
            type="button"
            class="btn btn-danger"
            :disabled="!history.canUndo"
            @click="save()"
          >
            <img
              src="~bootstrap-icons/icons/save.svg"
              alt="save icon"
              width="18"
              height="18"
            > Save
          </button>
        </div>
      </div>

      <div class="row mb-3">
        <h1>Bollettino Ozono {{ ozono.seq_num }}</h1>
      </div>

      <div class="row">
        <div class="col-md-2 mb-3">
          <label for="stato">Stato</label>
          <span v-if="ozono.status == 1">
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Inviato"
            >
          </span>
          <span v-else-if="ozono.status == 2">
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
        </div>
        <div class="col-md-2 mb-3">
          <label for="dataEmissione">Data emissione</label>
          <input
            id="dataEmissione"
            disabled
            type="text"
            class="form-control"
            :value="(new Date(ozono.start_valid_time)).toLocaleString()"
          >
        </div>
        <div class="col-md-2 mb-3">
          <label for="dataAggiornamento">Ultima modifica</label>
          <input
            id="dataAggiornamento"
            disabled
            type="text"
            class="form-control"
            :value="(new Date(ozono.last_update)).toLocaleString()"
          >
        </div>
        <div class="col-md-2 mb-3">
          <label for="versione">Versione</label>
          <input
            id="versione"
            disabled
            class="form-control"
            name="versione"
            type="text"
            :value="ozono.version"
          >
        </div>
        <div class="col-md-2 mb-3">
          <label for="username">Autore</label>
          <input
            id="username"
            disabled
            class="form-control"
            name="username"
            type="text"
            :value="ozono.username"
          >
        </div>
      </div> <!-- end row -->
      <div class="row">
        <div class="col-md-12 mb-3">
          <label for="note">Note</label>
          <OzonoText
            :id="'note'"
            :readonly="readonly"
            :data="ozono"
            :history="history"
            :value-key="'note'"
            :id-key="'id_w16'"
            @set-note="setNote"
          />
        </div>
      </div>
      <div class="row mt-3">
        <div class="col-xl-7 col-md-12 mb-3">
          <ul class="nav nav-tabs nav-justified sticky-top">
            <li
              v-for="(dataGiorno, index) in giorniBulletin"
              :key="index"
              class="nav-item"
            >
              <a
                class="nav-link"
                :class="{ active: current_day === index }"
                @click="current_day = index"
              >{{ dataGiorno }}</a>
            </li>
          </ul>
          <div
            v-for="(value, venue) in venue_values[current_day]"
            :key="venue"
          >
            <AreaOzono
              v-if="'w16_data' in ozono"
              :value="value"
              :venue="venue"
              :readonly="readonly"
              :history="history"
              :levels="levels"
              @set-level="setLevel"
            />
          </div>
        </div>
        <div class="col-xl-5 col-md-12 mb-3">
          <div
            class="sticky-top pt-5"
            style="z-index: 0;"
          >
            <MapOzono
              v-if="'w16_data' in ozono"
              :orography="orography"
              :rivers="rivers"
              :provinces="provinces"
              :capitals="capitals"
              :layer="layer"
              :levels="levels"
              :venues="ozono.w16_data[current_day]"
              :readonly="readonly"
              :selected-venue="selected_venue"
              :venue-data="venue_data"
              :ozono-status="ozono.status"
              :ozono-date="ozono.start_valid_time"
              @open-modal="openModal"
              @open-meteo-modal="openMeteoModal"
            />
            <img
              src="/images/ozono/BollOzo_legenda.png"
              class="img-fluid"
              alt="test"
            >
          </div>
        </div> <!-- end col-xl-5 -->
      </div> <!-- end row -->
    </div> <!-- end container-fluid -->
  </VeeForm>
</template>

<script>
import Modal from 'bootstrap/js/dist/modal'
// @ is an alias to /src
import MapOzono from './MapOzono.vue'
import AreaOzono from './AreaOzono.vue'
import HistoryStack from '@/components/History.js'
import api from '@/api'
import store from '@/store'
import apply from '@/components/apply'
import LevelModal from './LevelModal.vue'
import MeteoModal from './MeteoModal.vue'
import OzonoText from './OzonoText.vue'
import LoginModal from '@/components/LoginModal.vue'
import { Form as VeeForm } from 'vee-validate'

export default {
  name: 'OzonoBulletin',
  components: {
    MapOzono,
    AreaOzono,
    LevelModal,
    MeteoModal,
    OzonoText,
    LoginModal,
    VeeForm,
  },
  data () {
    // non reactive properties
    this.levelModal = null
    this.meteoModal = null
    return {
      // reactive properties
      levels: [],
      orography: false,
      rivers: false,
      provinces: false,
      capitals: false,
      layer: true,
      current_day: 0,
      ozono_id: null,
      ozono: {},
      error: '',
      readonly: true,
      history: new HistoryStack(),
      reopening: false,
      copying: false,
      sending: false,
      selected_venue: null,
      selected_id_w16_data: null,
      state: store.state
    }
  },
  computed: {
    today() {
      // returns today in 2021-04-22 format
      let d = new Date()
      return d.toISOString().substring(0, 10)
    },
    venue_values() {
      let vs = {
        0: {},
        1: {},
        2: {},
        3: {}
      }
      // we can get this data structure from DB if we want
      let ozono_aggregazione = {
        1: {aggregazione_temporale: "mx8", aggregazione_spaziale: "90p"},
        2: {aggregazione_temporale: "mx8", aggregazione_spaziale: "75p"},
        3: {aggregazione_temporale: "mx8", aggregazione_spaziale: "50p"},
        4: {aggregazione_temporale: "mx8", aggregazione_spaziale: "med"},
        5: {aggregazione_temporale: "mx8", aggregazione_spaziale: "max"},
        6: {aggregazione_temporale: "mxd", aggregazione_spaziale: "90p"},
        7: {aggregazione_temporale: "mxd", aggregazione_spaziale: "75p"},
        8: {aggregazione_temporale: "mxd", aggregazione_spaziale: "50p"},
        9: {aggregazione_temporale: "mxd", aggregazione_spaziale: "med"},
        10: {aggregazione_temporale: "mxd", aggregazione_spaziale: "max"}
      }
      if ('w16_data' in this.ozono) {
        Object.keys(this.ozono.w16_data).forEach(day => {
          this.ozono.w16_data[day].forEach(element => {
            let w16data1 = {
                mx8: {},
                mxd: {}
            }
            element.w16data1_set.forEach(element1 => {
              if (element1.id_ozono_aggregazione <= 10) {
                let ozono_aggregazione_element1 = ozono_aggregazione[element1.id_ozono_aggregazione]
                let aggregazione_temporale = ozono_aggregazione_element1.aggregazione_temporale
                let aggregazione_spaziale = ozono_aggregazione_element1.aggregazione_spaziale
                w16data1[aggregazione_temporale][aggregazione_spaziale] = element1.valore_num
              }
            })
            vs[day][element.id_ozono_zone] = {
              level: element.id_ozono_livelli,
              id_w16_data: element.id_w16_data,
              w16data1: w16data1
            }
          })
        })
      }
      return vs
    },
    giorniBulletin() {
      var bulletinDays = []
      var stringBulletinDays = ['', '', '', '']
      if ('start_valid_time' in this.ozono){
        var currentFullDate = new Date(this.ozono.start_valid_time)
        const startDay = currentFullDate.getDate()
        const yesterday = new Date(new Date(this.ozono.start_valid_time).setDate(new Date(this.ozono.start_valid_time).getDate()-1))
        for(let i = 0; i <= 3 ; i++){
          if (i == 0) {
            bulletinDays[i] = new Date(yesterday.getTime())
            stringBulletinDays[i] = bulletinDays[i].getDate() + "/" + (bulletinDays[i].getMonth()+1)  + "/" +  bulletinDays[i].getFullYear()
          }
          else {
            bulletinDays[i] = new Date(currentFullDate.getTime())
            currentFullDate = new Date(this.ozono.start_valid_time)
            currentFullDate.setDate(startDay+i)
            stringBulletinDays[i] = bulletinDays[i].getDate() + "/" + (bulletinDays[i].getMonth()+1)  + "/" +  bulletinDays[i].getFullYear()
          }
        }
      }
      return stringBulletinDays
    },
    venue_data() {
      let vd = { }
      this.ozono.w16_data[this.current_day].forEach(element => {
        vd[element.id_ozono_zone] = {
          color: this.levels[Math.max(0, element.id_ozono_livelli - 1)].color,
          id_ozono_livelli: element.id_ozono_livelli,
          id_w16_data: element.id_w16_data
        }
      })
      return vd
    }
  },
  watch: {
    '$route': 'fetchData'
  },
  created() {
    this.fetchData()
  },
  mounted: function () {
    this.$nextTick(() => {
      let levelModalElement = document.getElementById('levelModal')
      this.levelModal = new Modal(levelModalElement)
      levelModalElement.addEventListener('hidden.bs.modal', () => {
        this.selected_venue = 0
      })
      let meteoModalElement = document.getElementById('meteoModal')
      this.meteoModal = new Modal(meteoModalElement)
    })
    window.addEventListener('keypress', (event) => {
      if (event.ctrlKey) {
        if (event.key === 'z') {
          this.undo()
        } else if (event.key === 'Z') {
          this.redo()
        }
      }
    })
  },
  methods: {
    async fetchOzono () {
      const response = await fetch('/api/w16/bulletins/' + this.ozono_id + '/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    async fetchLevels () {
      const response = await fetch('/api/w16/levels/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    setLevel(venue, id_w16_data, old_value, new_value) {
      let data = {
        id_key: 'id_w16_data',
        id: id_w16_data,
        value_key: 'id_ozono_livelli',
        old_value: old_value,
        new_value: new_value
      }
      this.onTransformed(data)
    },
    setSelectedLevel(level) {
      let data = {
        id_key: 'id_w16_data',
        id: this.selected_id_w16_data,
        value_key: 'id_ozono_livelli',
        old_value: this.venue_data[this.selected_venue].id_ozono_livelli,
        new_value: level
      }
      this.onTransformed(data)
      this.levelModal.hide()
    },
    setNote(id_w16, old_value, new_value) {
      let data = {
        id: id_w16,
        id_key: 'id_w16',
        value_key: 'note',
        old_value: old_value,
        new_value: new_value
      }
      this.onTransformed(data)
    },
    humanize(aggregazione_spaziale) {
      switch(aggregazione_spaziale) {
        case '90p':
          return '90 percentile'
        case '75p':
          return '75 percentile'
        case '50p':
          return '50 percentile'
        case 'med':
          return 'media'
        case 'max':
          return 'massimo'
      }
    },
    // this handler is triggered to modify a single w16_data record
    onTransformed(snapshot) {
      apply(this.ozono, snapshot);
      this.history.record(snapshot)
    },
    undo() {
      if (!this.readonly && this.history.canUndo) {
        let snapshot = this.history.undo()
        let found = apply(this.ozono, snapshot, true)
        this.$toast.open(
            {
              message: 'Undo: livello nella zona ' + found.id_ozono_zone + ' con scadenza ' + found.data_scadenza +' a ' + snapshot.old_value,
              type: 'success',
              position: 'top-left'
            }
          )
      }
    },
    redo() {
      if (!this.readonly && this.history.canRedo) {
        let snapshot = this.history.redo()
        let found = apply(this.ozono, snapshot);
        this.$toast.open(
            {
              message: 'Redo: livello nella zona ' + found.id_ozono_zone + ' con scadenza ' + found.data_scadenza +' a ' + snapshot.new_value,
              type: 'info',
              position: 'top-left'
            }
          )
      }
    },
    remove() {
      if (
        confirm('Vuoi davvero cancellare questo bollettino?')
      ) {
        api.fetchBulletinDelete(this.ozono_id, 'w16/bulletins', store).then(response => {
          if (response.ok) {
            this.$toast.open(
              {
                message: 'Bollettino cancellato',
                type: 'success',
                position: 'top-left'
              }
            )
            this.$router.back()
          } else {
            this.$toast.open(
              {
                message: `Errore ${response.status} nella cancellazione del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
          }
        }).catch(error => {
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
    async fetchOzonoAction (action) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w16/bulletins/${this.ozono_id}/${action}/`
      )
      return response
    },
    execute(action, reroute, message) {
      if (action === 'resend' && !confirm('Vuoi davvero ripetere l\'invio di questo bollettino?')) {
        return
      } else {
        this.really_execute(action, reroute, message)
      }
    },
    really_execute(action, reroute, message) {
      this[action + 'ing'] = true
      this.fetchOzonoAction(action).then(response => {
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
          if (response.status === 401 || response.status === 403) {
            this.$refs.login.show()
            return null
          }
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
          this.$router.push({ path: `/w16/${data.id_w16}`})
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
    async bulkUpdateW16data(snapshots) {
      let payload = snapshots
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w16/data/bulk_update/`,
        {
          method: 'POST',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    save() {
      this.history.shake()
      let discarded = this.history.splice()
      let original_length = discarded.length
      const original_discarded = [...discarded];
      // add username and version
      discarded.push({
        id_key: "id_w16",
        id: this.ozono.id_w16,
        value_key: "version",
        old_value: this.ozono.version,
        new_value: this.ozono.version + 1
      })
      discarded.push({
        id_key: "id_w16",
        id: this.ozono.id_w16,
        value_key: "username",
        old_value: this.ozono.username,
        new_value: this.state.username
      })

      // console.log(discarded)
      this.bulkUpdateW16data(discarded).then((response) => {
        if (!response.ok) {
          this.history.restore(original_discarded)
          this.$toast.open(
            {
              message: 'Errore nel salvataggio',
              type: 'error',
              position: 'top-left'
            }
          )
          if (response.status === 401 || response.status === 403) {
            this.$refs.login.show()
            return null
          }
        }
        return response.json()
      }).then(data => {
        // console.log('data:', data)
        this.ozono.version += 1
        this.ozono.username = this.state.username
        this.ozono.last_update = data.last_update

        if (data.updated >= discarded.length) {
          this.$toast.open(
              {
                message: `Salvate ${original_length} modifiche`,
                type: 'success',
                position: 'top-left'
              }
            )
        } else {
          this.$toast.open(
              {
                message: `Salvate solo ${data.updated} modifiche su ${discarded.length}`,
                type: 'warning',
                position: 'top-left'
              }
            )
        }
        //Controllo tra snapshots e bollettini salvati nel db
        let snapshotUnsaved = []
        discarded.forEach((snapshot) => {
          if(snapshot.id_key === "id_w16"){
            if (snapshot.new_value !== data.bulletin[snapshot.value_key])
                snapshotUnsaved.push(snapshot)
          }else if (snapshot.id_key === "id_w16_data"){
            let element = data.bulletin.w16data_set.find(element => element.id_w16_data === snapshot.id)
            if(Number(snapshot.new_value) !== element[snapshot.value_key])
                snapshotUnsaved.push(snapshot)
          }
        })

        if(snapshotUnsaved.length > 0){
          let snapshotString = ""
          let n = 1

          snapshotUnsaved.forEach((s) => {
              snapshotString = `${snapshotString}Snapshot #${n} id: ${s.id} id_key: "${s.id_key}" value_key: "${s.value_key}" old_value: ${s.old_value} new_value: ${s.new_value}\n`
              n++
            })
          const repo_home = import.meta.env.VITE_REPO_HOME || 'https://github.com/Arpapiemonte/weboll'
          alert(`ATTENZIONE! perdita di dati durante il salvataggio si prega di segnalare agli sviluppatori qui: \n${repo_home} indicando:

          - pagina: https://production.example.com/w05/${this.ozono.id_w05}
          - ${api.getDateFormatted(new Date())}
          - snapshot non salvati:\n\n${snapshotString}`)

        }
      }).catch((error) => {
        this.history.restore(discarded.splice(0, original_length))
        this.$toast.open(
            {
              message: `Errore di comunicazione: ${error}`,
              type: 'error',
              position: 'top-left'
            }
          )
      })
    },
    rgbToHex(r, g, b) {
     return "#" + ((1 << 24) + (Number(r) << 16) + (Number(g) << 8) + Number(b)).toString(16).slice(1);
    },
    fetchData() {
      this.ozono_id = this.$route.params.id
      if (typeof this.ozono_id === 'undefined') {
        return
      }
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
        let levels = data
        levels.forEach((level) => {
          let rgb = level.rgb.replaceAll('.', ':').split(':')
          // console.log(rgb)
          level.color = this.rgbToHex(rgb[0], rgb[1], rgb[2])
          return level
        })
        // console.log(levels)
        this.levels = levels
      }).catch((error) => {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
      this.fetchOzono().then(response => {
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
        let ozono = data
        ozono.w16_data = {
          0: [],
          1: [],
          2: [],
          3: []
        }
        if ('w16data_set' in ozono) {
          ozono.w16data_set.forEach((element) => {
            if (element.id_scadenza >= 0 && element.id_scadenza <= 3) {
            ozono.w16_data[element.id_scadenza].push(element)
            }
          })
          delete ozono.w16data_set
        }
        this.readonly = (ozono.status !== '0' || !this.state.username)
        this.ozono = ozono
      }).catch((error) => {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    openModal(venue, id_w16_data) {
      this.selected_venue = venue
      this.selected_id_w16_data = id_w16_data
      this.levelModal.show()
    },
    openMeteoModal() {
      // console.log('openMeteoModal')
      this.meteoModal.show()
    }
  }
}
</script>

<style>
.dirty {
  border: 3px solid #0dcaf0;
}
</style>
