// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    v-if="ready"
    class="container-fluid my-3 py-1"
  >
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
          :href="'/api/w24/pdf/' + vigilanza.id_w24"
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
          v-if="vigilanza.status === '1' && state.username && vigilanza.data_emissione.substring(0, 10) === today" 
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
          v-if="vigilanza.status === '0' && state.username"
          type="button"
          class="btn btn-outline-success"
          :disabled="vigilanza.sintesi_meteo === '' || vigilanza.sintesi_meteo.startsWith('|||InputDataIsMissing|||')"
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
          v-if="vigilanza.status === '0' && state.username"
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
      </div> <!-- btn-group -->
    </div> <!-- row -->

    <div class="row mb-3">
      <h1>Bollettino Vigilanza {{ vigilanza.numero_bollettino }}</h1>
      <div
        v-if="dataismissing"
        class="alert alert-danger"
      >
        Attenzione alcuni dati di input sono mancanti!
      </div>
    </div> <!-- row -->
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="vigilanza.status == 1">
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Inviato"
            >
          </span>
          <span v-else-if="vigilanza.status == 2">
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
        <label for="data_emissione">Data emissione
          <input
            id="data_emissione"
            disabled
            class="form-control"
            name="data_emissione"
            type="text"
            :value="getDateFormatted(vigilanza.data_emissione)"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="last_update">Ultima modifica
          <input
            id="last_update"
            disabled
            class="form-control"
            name="last_update"
            type="text"
            :value="getDateFormatted(vigilanza.last_update)"
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
            :value="vigilanza.username"
          >
        </label>
      </div>
    </div> <!-- row -->
    <div class="row">
      <div class="col-md-12 mb-3">
        <label for="sintesi">Sintesi meteorologica</label>
        <textarea
          id="sintesi"
          class="form-control"
          rows="5"
          :readonly="readonly"
          :value="vigilanza.sintesi_meteo"
          @change="saveSintesiMeteo($event.target.value)"
        />
      </div> <!-- col -->
    </div> <!-- row -->
    <div class="row">
      <div class="col-xl-12 col-md-12 mb-3">
        <ul
          class="nav nav-tabs nav-justified sticky-top bg-light"
          style="top: 46px;"
          role="tablist"
        >
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-d0-tab"
              class="nav-link active"
              data-bs-toggle="pill"
              data-bs-target="#pills-d0"
              type="button"
              role="tab"
              aria-controls="pills-d0"
              aria-selected="true"
            >
              {{ days[0] }} Pomeriggio
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-d1-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-d1"
              type="button"
              role="tab"
              aria-controls="pills-d1"
              aria-selected="false"
            >
              {{ days[1] }}
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-d2-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-d2"
              type="button"
              role="tab"
              aria-controls="pills-d2"
              aria-selected="false"
            >
              {{ days[2] }}
            </button>
          </li>
        </ul>
        <div
          class="tab-content"
        >
          <TabVigilanza
            :id="'d0'"
            :data="vigilanza.w24_data"
            :time-layouts="[48, null, null, 45, 46]"
            :active="true"
            :readonly="readonly"
            :tipoanomaliat="vigilanza.tipo_anomalia_termica"
            :soglievento="soglievento"
            @save-w24-data="saveW24Data"
            @save-w24-value="saveW24Value"
          />
          <TabVigilanza
            :id="'d1'"
            :data="vigilanza.w24_data"
            :time-layouts="[66, 60, 61, 62, 63]"
            :readonly="readonly"
            :tipoanomaliat="vigilanza.tipo_anomalia_termica"
            :soglievento="soglievento"
            @save-w24-data="saveW24Data"
            @save-w24-value="saveW24Value"
          />
          <TabVigilanza
            :id="'d2'"
            :data="vigilanza.w24_data"
            :time-layouts="[83, 77, 78, 79, 80]"
            :readonly="readonly"
            :tipoanomaliat="vigilanza.tipo_anomalia_termica"
            :soglievento="soglievento"
            @save-w24-data="saveW24Data"
            @save-w24-value="saveW24Value"
          />
        </div>
      </div> <!-- col -->
    </div> <!-- row -->
  </div>
</template>
<script>
import api from '@/api'
import store from '@/store'
import TabVigilanza from './TabVigilanza.vue'

export default {
  name: 'VigilanzaBulletin',
  components: {
    TabVigilanza
  },
  data () {
    // non reactive properties
    return {
      // reactive properties
      vigilanza: {
        numero_bollettino: "aaaaaaaa"
      },
      ready: false,
      readonly: true,
      state: store.state,
      sending: false,
      reopening: false,
      countfetch: 0,
      soglievento: {},
      soglieneve: {},
    }
  },
  computed: {
    days() {
      var bulletinDays = []
      var stringBulletinDays = ['', '', '']
      if ('data_emissione' in this.vigilanza){
        var currentFullDate = new Date(this.vigilanza.data_emissione)
        const startDay = currentFullDate.getDate()
        for(let i = 0; i <= 2 ; i++){
          bulletinDays[i] = new Date(currentFullDate.getTime())
          currentFullDate = new Date(this.vigilanza.data_emissione)
          currentFullDate.setDate(startDay+i+1)
          stringBulletinDays[i] = bulletinDays[i].getDate() + "/" + (bulletinDays[i].getMonth()+1)  + "/" +  bulletinDays[i].getFullYear()
        }
      }
      return stringBulletinDays
    },
    today() {
      // returns today in 2021-04-22 format
      let d = new Date()
      return d.toISOString().substring(0, 10)
    },
    dataismissing() {
      if(this.vigilanza.sintesi_meteo.startsWith("|||InputDataIsMissing|||")){
        return true
      }
      return false
    },
  },
   watch: {
    countfetch: {
      handler () {
        if (this.countfetch >= 2) {
          this.ready = true
        }
      }
    },
  },
  created() {
    // https://v3.vuejs.org/guide/composition-api-lifecycle-hooks.html#lifecycle-hooks
    this.getVigilanza()
  },
  methods: {
    getVigilanza() {
      this.vigilanza_id = this.$route.params.id
      if (typeof this.vigilanza_id === 'undefined') {
        return
      }
      this.fetchData()
    },
    fetchData () {
      this.countfetch = 0
      this.ready = false     
      console.log(`fetch data for ${this.vigilanza_id}!`)
      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
      this.fetchVigilanza().then(response => {
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
        console.log(`received data = ${JSON.stringify(data)}`)
        data.w24_data = { }
        if ('w24data_set' in data) {
          data.w24data_set.forEach((element) => {
            if (!(element.id_time_layouts in data.w24_data)) {
              data.w24_data[element.id_time_layouts] = { }
            }
            if (element.id_parametro in data.w24_data[element.id_time_layouts]) {
              data.w24_data[element.id_time_layouts][element.id_parametro].push(element)
            } else {
              data.w24_data[element.id_time_layouts][element.id_parametro] = [element]
            }
          })
        }
        this.vigilanza = data
        this.readonly = (data.status === '1' || !this.state.username)
        this.countfetch += 1
      }).catch(error => {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
      this.fetchSoglie().then(response => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero delle soglie`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json()
      }).then(data => {
        const aree = [
            "Piem-A",
            "Piem-B",
            "Piem-C",
            "Piem-D",
            "Piem-E",
            "Piem-F",
            "Piem-G",
            "Piem-H",
            "Piem-I",
            "Piem-L",
            "Piem-M"
        ]
        
        aree.forEach(area => {
          this.soglievento[area] = []
          this.soglieneve[area] = {"901": [], "902": []}
        });

        console.log(data)
        for(const soglia in data){
          if(data[soglia].id_parametro === "VELV"){
            this.soglievento[data[soglia].id_allertamento].push(data[soglia])
          }
          if(data[soglia].id_parametro === "SNOW"){
            if(data[soglia].id_aggregazione === 901){
              this.soglieneve[data[soglia].id_allertamento]["901"].push(data[soglia])
            }
            if(data[soglia].id_aggregazione === 902){
              this.soglieneve[data[soglia].id_allertamento]["902"].push(data[soglia])
            }
          }
        }


        aree.forEach(area => {
          this.soglievento[area].sort((a, b) => (a.classe_intensita > b.classe_intensita) ? 1 : ((b.classe_intensita> a.classe_intensita) ? -1 : 0))
          this.soglieneve[area]["901"].sort((a, b) => (a.classe_intensita > b.classe_intensita) ? 1 : ((b.classe_intensita> a.classe_intensita) ? -1 : 0))
          this.soglieneve[area]["902"].sort((a, b) => (a.classe_intensita > b.classe_intensita) ? 1 : ((b.classe_intensita> a.classe_intensita) ? -1 : 0))
        });

        this.countfetch += 1
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
    async fetchVigilanza () {
      // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
      const response = await fetch('/api/w24/bulletins/' + this.vigilanza_id + '/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    async fetchSoglie () {
      // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
      const response = await fetch('/api/w24/soglie/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    async bulkUpdateW24(payload) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w24/bulletins/bulk_update/`,
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
        `/api/w24/${endpoint}/${id}/`,
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
    saveW24(stack) {
      this.bulkUpdateW24(stack).then((response) => {
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
        this.vigilanza.last_update = data.bulletin.last_update
        this.vigilanza.username = store.state.username
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
    saveW24Data(idw24data, new_value) {
      let myW24data = this.vigilanza.w24data_set.find(w24data => w24data.id_w24_data === idw24data)

      myW24data.numeric_value = new_value

      let id = myW24data.id_w24_data
      let stack = []
      const payload = {"id_key":"id_w24_data","id": id,"value_key":"numeric_value","new_value": new_value}
      const payloadusername = {"id_key":"id_w24","id":this.vigilanza.id_w24,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)
      stack.push(payload)

      this.saveW24(stack)
    },
    saveW24Value(idw24data, new_value) {
      let stack = []

      let myW24data = this.vigilanza.w24data_set.find(w24data => w24data.id_w24_data === idw24data)
      myW24data.numeric_value = new_value
      let id = myW24data.id_w24_data

      let max = 0
      const snow_meters = ["SNOW_400", "SNOW_700", "SNOW_1000", "SNOW_2000"]

      snow_meters.forEach(mt => {
        let tmp = this.vigilanza.w24data_set.find(w24data => w24data.id_parametro === mt 
        && w24data.id_allertamento === myW24data.id_allertamento && w24data.id_time_layouts === myW24data.id_time_layouts)

        if(parseInt(tmp.numeric_value) > parseInt(max)){
          max = tmp.numeric_value
        }
      })

      
      
      
      let aggregazione = ""
      if(myW24data.id_time_layouts == 48){
        aggregazione = "901"
      }else{
        aggregazione = "902"
      }

      let soglia0 = this.soglieneve[myW24data.id_allertamento][aggregazione][0]
      let soglia1 = this.soglieneve[myW24data.id_allertamento][aggregazione][1]
      let soglia2 = this.soglieneve[myW24data.id_allertamento][aggregazione][2]
      let soglia3 = this.soglieneve[myW24data.id_allertamento][aggregazione][3]

      let value_intensità = 0

      if(parseInt(max) >= parseInt(soglia0.soglia1) && parseInt(max) <= parseInt(soglia0.soglia1)){
        value_intensità = 0
      }else if(parseInt(max) >= parseInt(soglia1.soglia1) && parseInt(max) <= parseInt(soglia1.soglia2)){
        value_intensità = 1
      }else if(parseInt(max) >= parseInt(soglia2.soglia1) && parseInt(max) <= parseInt(soglia2.soglia2)){
        value_intensità = 2
      }else if(parseInt(max) >= parseInt(soglia3.soglia1)){
        value_intensità = 3
      }

      let neveclass = this.vigilanza.w24data_set.find(w24data => w24data.id_allertamento === myW24data.id_allertamento 
      && w24data.id_time_layouts === myW24data.id_time_layouts && w24data.id_parametro === "SNOW")

      neveclass.numeric_value = value_intensità

      const payloadclass = {"id_key":"id_w24_data","id": neveclass.id_w24_data,"value_key":"numeric_value","new_value": value_intensità}
      stack.push(payloadclass)
      
      
      
      const payload = {"id_key":"id_w24_data","id": id,"value_key":"numeric_value","new_value": new_value}
      const payloadusername = {"id_key":"id_w24","id":this.vigilanza.id_w24,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)
      
      stack.push(payload)



      this.saveW24(stack)
    },
    saveSintesiMeteo(value) {
      this.vigilanza.sintesi_meteo = value
      let stack = []
      const payload = {"id_key":"id_w24","id":this.vigilanza.id_w24,"value_key":"sintesi_meteo","new_value": value}
      const payloadusername = {"id_key":"id_w24","id":this.vigilanza.id_w24,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)
      stack.push(payload)
      this.saveW24(stack)
    },
    execute(action, reroute, message) {
      if (action === 'resend' && !confirm('Vuoi davvero ripetere l\'invio di questo bollettino?')) {
        return
      } else {
        this.really_execute(action, reroute, message)
      }
    },
    async fetchAction(action) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w24/bulletins/${this.vigilanza.id_w24}/${action}/`
      )
      return response
    },
    really_execute(action, reroute, message) {
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
          this.$router.push({ path: `/w24/${data.id_w24}`})
          this.vigilanza_id = data.id_w24
          this.countfetch = 0
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
        api.fetchBulletinDelete(this.vigilanza.id_w24, 'w24/bulletins', store).then(response => {
          if (response.ok) {
            this.$toast.open(
              {
                message: 'Bollettino cancellato',
                type: 'success',
                position: 'top-left'
              }
            )
            this.bozza_presente = false
            this.$router.push({ path: `/w24`})
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
  }
}
</script>
