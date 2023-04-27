// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    v-if="ready"
    class="m-3"
  >
    <div
      class="row justify-content-end sticky-top py-1 nottoprint"
      style="background-color: #f8f9fa;"
    >
      <div
        class="btn-group w-auto"
        role="group"
      >
        <div class="btn-group">
          <select
            v-if="!readonly && state.username"
            id="copyselect"
            v-model="modelToCopy"
            class="btn btn-outline-info"
          >
            <option selected>
              Copia Valori Modello:
            </option>
            <option
              v-for="model in availableModels"
              :key="model"
            >
              <a>
                {{ model }}
              </a>
            </option>
          </select>
        </div>

        <button
          class="btn btn-outline-primary"
          target="_blank"
          role="button"
          @click="topdf()"
        >
          <img
            src="~bootstrap-icons/icons/file-earmark-pdf-fill.svg"
            alt="PDF icon"
            width="18"
            height="18"
          > PDF
        </button>
        <button
          v-if="false"
          disabled
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
          v-if="previsione.Bollettino.status === '1' && state.username && previsione.Bollettino.data_emissione.substring(0, 10) === today"
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
          v-if="previsione.Bollettino.status === '0' && state.username"
          type="button"
          :disabled="!(validity_tab[0] && validity_tab[1] && validity_tab[2] && validity_tab[3] && validity_tab[4])"
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
          v-if="previsione.Bollettino.status === '0' && state.username"
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
    <div>
      <div
        id="bollettinoTitle"
        class="row mb-3 nottoprint"
      >
        <h1>Previsione su Aree Allerta {{ previsione.Bollettino.seq_num }}</h1>
      </div>
      <div class="row nottoprint">
        <div class="col-md-1 mb-3">
          <label for="stato">Stato</label>
          <span v-if="previsione.Bollettino.status == 1">
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Inviato"
            >
          </span>
          <span v-else-if="previsione.Bollettino.status == 2">
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
            :value="(new Date(previsione.Bollettino.data_emissione)).toLocaleString()"
          >
        </div>
        <div class="col-md-2 mb-3">
          <label for="dataAggiornamento">Ultima modifica</label>
          <input
            id="dataAggiornamento"
            disabled
            type="text"
            class="form-control"
            :value="(new Date(previsione.Bollettino.last_update)).toLocaleString()"
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
            :value="previsione.Bollettino.username"
          >
        </div>
        <div class="col-md-3 mb-3">
          <label for="username">First guess</label>
          <input
            id="firstguess"
            disabled
            class="form-control"
            name="username"
            type="text"
            :value="previsione.Bollettino.firstguess"
          >
        </div>
        <div
          v-if="previsione.Bollettino.status === '0'"
          class="col-md-2 mb-3 mt-4 nottoprint"
        >
          <select
            id="openselect"
            v-model="modelToOpen"
            class="btn btn-outline-primary form-select"
            aria-expanded="false"
          >
            <option selected>
              Visualizza Modello:
            </option>
            <option
              v-for="model in availableModels"
              :key="model"
              :value="model"
            >
              <a>
                {{ model }}
              </a>
            </option>
            <option>
              <a
                v-if="maxReady"
                :value="'MAX'"
              >MAX</a>
            </option>
          </select>
        </div>
      </div> <!-- end row -->
      <ul class="nav nav-tabs nottoprint">
        <li class="nav-item">
          <button
            class="nav-link"
            :class="{'active': active_tab === 0, 'text-danger' : !validity_tab[0]}"
            @click="active_tab = 0"
          >
            Precipitazioni in 6h
          </button>
        </li>
        <li class="nav-item">
          <button
            class="nav-link"
            :class="{'active': active_tab === 1, 'text-danger' : !validity_tab[1]}"
            @click="active_tab = 1"
          >
            Massimo in 12h - giorno 1
          </button>
        </li>
        <li class="nav-item">
          <button
            class="nav-link"
            :class="{'active': active_tab === 2, 'text-danger' : !validity_tab[2]}"
            @click="active_tab = 2"
          >
            Massimo in 12h - giorno 2
          </button>
        </li>
        <li class="nav-item">
          <button
            class="nav-link"
            :class="{'active': active_tab === 3, 'text-danger' : !validity_tab[3]}"
            @click="active_tab = 3"
          >
            Massimo in 24h - giorno 2
          </button>
        </li>
        <li class="nav-item">
          <button
            class="nav-link"
            :class="{'active': active_tab === 4, 'text-danger' : !validity_tab[4]}"
            @click="active_tab = 4"
          >
            Zero Termico e Quota Neve
          </button>
        </li>
      </ul>
    </div>
    <div>
      <div v-if="active_tab === 0">
        <div v-if="overallView">
          <ScadenzeOverall
            :previsione="previsione"
            :timelayouts6h="timelayouts6h"
            :data-emissione="previsione.Bollettino.data_emissione"
            :readonly="readonly"
            @set-measure="setMeasure"
            @toggle-view="toggleView"
          />
        </div>
        <div v-else>
          <ScadenzeDetail
            :previsione="previsione"
            :timelayouts6h="timelayouts6h"
            :detail-models="detailModels"
            :data-emissione="previsione.Bollettino.data_emissione"
            :readonly="readonly"
            @set-measure="setMeasure"
            @copy-scadenza="copyScadenza"
            @change-model="changeModel"
            @toggle-view="toggleView"
          />
        </div>
      </div>
      <div v-if="active_tab === 1">
        <Scadenze12
          :bollettino="previsione['Bollettino']['w30_data']"
          :timelayoutset="{'48': ['45', '46']}"
          :timelayout="'48'"
          :idaggregazione="'126'"
          :readonly="readonly"
          :data-emissione="previsione.Bollettino.data_emissione"
          @set-measure="setMeasure"
          @calculate-first-guess="calculateFirstGuess"
        />
      </div>
      <div v-if="active_tab === 2">
        <Scadenze12
          :bollettino="previsione['Bollettino']['w30_data']"
          :timelayoutset="{'64': ['60', '61'], '65': ['61', '62'], '67': ['62', '63']}"
          :timelayout="'66'"
          :idaggregazione="'126'"
          :readonly="readonly"
          :data-emissione="previsione.Bollettino.data_emissione"
          @set-measure="setMeasure"
          @calculate-first-guess="calculateFirstGuess"
        />
      </div>
      <div v-if="active_tab === 3">
        <Scadenze12
          :bollettino="previsione['Bollettino']['w30_data']"
          :timelayoutset="{'66': ['60', '61', '62', '63']}"
          :timelayout="'66'"
          :idaggregazione="'127'"
          :readonly="readonly"
          :data-emissione="previsione.Bollettino.data_emissione"
          @set-measure="setMeasure"
          @calculate-first-guess="calculateFirstGuess"
        />
      </div>
      <div v-if="active_tab === 4">
        <div v-if="overallView">
          <ScadenzeOverallQuote
            :previsione="previsione"
            :timelayouts6h="timelayouts6h"
            :readonly="readonly"
            :data-emissione="previsione.Bollettino.data_emissione"
            @setmeasure-freeze-snow="setmeasureFreezeSnow"
            @toggle-view="toggleView"
          />
        </div>
        <div v-else>
          <ScadenzeDetailQuote
            :previsione="previsione"
            :timelayouts6h="timelayouts6h"
            :detail-models="detailModels"
            :readonly="readonly"
            :data-emissione="previsione.Bollettino.data_emissione"
            @setmeasure-freeze-snow="setmeasureFreezeSnow"
            @copy-scadenza-f-s="copyScadenzaFreezeSnow"
            @change-model="changeModel"
            @toggle-view="toggleView"
          />
        </div>
      </div>
    </div>
    <PqaaMap />
  </div>
</template>

<script>
import PqaaMap from './PqaaMap.vue'
import ScadenzeDetail from './ScadenzeDetail.vue'
import ScadenzeOverall from './ScadenzeOverall.vue'
import Scadenze12 from './Scadenze12.vue'
import ScadenzeOverallQuote from './ScadenzeOverallQuote.vue'
import ScadenzeDetailQuote from './ScadenzeDetailQuote.vue'
import store from '@/store'
import api from '@/api'

export default {
  name: 'PrevisioneBulletin',
  components: {
    PqaaMap,
    ScadenzeOverall,
    ScadenzeDetail,
    ScadenzeOverallQuote,
    ScadenzeDetailQuote,
    Scadenze12
  },
  data () {
    return {
      previsione_id: null,
      previsione: {},
      ready: false,
      maxReady: false,
      countdown: 0,
      modelsFetched: 0,
      copying: false,
      reopening: false,
      sending: false,
      overallView: true,
      availableModels: [],
      detailModels: ["","",""],
      active_tab: 0,
      timelayouts6h: ["43", "44", "45", "46", "60", "61", "62", "63", "77", "78", "79", "80"],
      validity_tab: [false,false,false,false,false],
      readonly: false,
      state: store.state,
      modelToOpen: "Visualizza Modello:",
      modelToCopy: "Copia Valori Modello:"
    }
  },
  computed: {
    base_data_url () {
      return import.meta.env.VITE_BASE_DATA_URL || ""
    },
    today() {
      // returns today in 2021-04-22 format
      let d = new Date()
      return d.toISOString().substring(0, 10)
    }
  },
  watch: {
    countdown: {
      handler () {
        if (this.countdown >= 1) {
          this.ready = true
          this.getModels()
        }
      }
    },
    active_tab: {
      handler () {
        this.overallView = true
        
        if(this.active_tab === 4 && this.detailModels.find(e => e === "MAX")){
          for(let i = 0; i<3; i++){
            let indexofMax = this.detailModels.indexOf("MAX")
            if(indexofMax < 2 && indexofMax !== -1){
              this.detailModels[indexofMax] = this.detailModels[indexofMax + 1]
              this.detailModels[indexofMax + 1] = ""
            }else{
              this.detailModels[indexofMax] = ""
            }
          }
        }
      }
    },
    modelsFetched: {
      handler () {
        if (this.availableModels.length > 0 && this.modelsFetched >= this.availableModels.length) {
          this.calculateMax()
          this.maxReady = true
        }
      }
    },
    modelToOpen: {
      handler () {
        if(this.modelToOpen !== "Visualizza Modello:"){
          this.openModel(this.modelToOpen)
          this.modelToOpen = "Visualizza Modello:"
        }
      }
    },
    modelToCopy: {
      handler () {
        if(this.modelToCopy !== "Copia Valori Modello:"){
          this.copyModel(this.modelToCopy)
          this.modelToCopy = "Copia Valori Modello:"
        }
      }
    },
    previsione: {
      deep: true,
      handler(){
        //controllo validità sulle 6h
        const timelayoutsvalidity = ["45", "46", "60", "61", "62", "63", "77", "78", "79", "80"]
        this.validity_tab[0] = true
        timelayoutsvalidity.forEach(time_layout => {
          this.previsione.Bollettino.w30_data[time_layout]["PLUV"]["900"].forEach(data => {
            if(data.numeric_value < 0 || isNaN(data.numeric_value) || data.numeric_value === null){
              this.validity_tab[0]=false
            }


          })
          this.previsione.Bollettino.w30_data[time_layout]["PLUV"]["125"].forEach(data => {
            if(data.numeric_value < 0 || isNaN(data.numeric_value) || data.numeric_value === null){
              this.validity_tab[0]=false
            }

            if(data.numeric_value < this.previsione.Bollettino.w30_data[time_layout]["PLUV"]["900"].find(e => e.id_allertamento === data.id_allertamento).numeric_value){
              this.validity_tab[0]=false
            }
          })
        })

        //controllo validità sulle 12h d0
        this.validity_tab[1] = true
        this.previsione.Bollettino.w30_data["48"]["PLUV"]["126"].forEach(data => {
          if(data.numeric_value === null || isNaN(data.numeric_value)){
            this.validity_tab[1]=false
          }

          ["45", "46"].forEach(tl => {
            if(data.numeric_value < this.previsione.Bollettino.w30_data[tl]["PLUV"]["125"].find(e => e.id_allertamento === data.id_allertamento).numeric_value){
              this.validity_tab[1]=false
            }
          })
        })

        //controllo validità sulle 12h d1
        this.validity_tab[2] = true
        this.previsione.Bollettino.w30_data["66"]["PLUV"]["126"].forEach(data => {
          if(data.numeric_value === null || isNaN(data.numeric_value)){
            this.validity_tab[2]=false
          }

          ["60", "61", "62", "63"].forEach(tl => {
            if(data.numeric_value < this.previsione.Bollettino.w30_data[tl]["PLUV"]["125"].find(e => e.id_allertamento === data.id_allertamento).numeric_value){
              this.validity_tab[2]=false
            }
          })
        })

        //controllo validità sulle 24h d1
        this.validity_tab[3] = true
        this.previsione.Bollettino.w30_data["66"]["PLUV"]["127"].forEach(data => {
          if(data.numeric_value === null || isNaN(data.numeric_value)){
            this.validity_tab[3]=false
          }

          if(data.numeric_value < this.previsione.Bollettino.w30_data["66"]["PLUV"]["126"].find(e => e.id_allertamento === data.id_allertamento).numeric_value){
            this.validity_tab[3]=false
          }

        })

        //controllo validità su FRZLVL E SNOW_LEV d1
        this.validity_tab[4] = true
        timelayoutsvalidity.forEach(time_layout => {
          this.previsione.Bollettino.w30_data[time_layout]["SNOW_LEV"]["0"].forEach(data => {
            if(data.numeric_value < 0 || data.numeric_value > 6000 || isNaN(data.numeric_value) || data.numeric_value === null){
              this.validity_tab[4]=false
            }

            if(data.numeric_value > this.previsione.Bollettino.w30_data[time_layout]["FRZLVL"]["0"].find(e => e.id_allertamento === data.id_allertamento).numeric_value){
              this.validity_tab[4]=false
            }

          })

          this.previsione.Bollettino.w30_data[time_layout]["FRZLVL"]["0"].forEach(data => {
            if(data.numeric_value < 0 || data.numeric_value > 6000 || isNaN(data.numeric_value) || data.numeric_value === null){
              this.validity_tab[4]=false
            }
          })

        })
      }
    }
  },
  mounted() {
    this.getPrevisione()
  },
  methods: {
    async fetchPrevisione () {
      const response = await fetch('/api/w30/bulletins/' + this.previsione_id + '/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    getPrevisione() {
      this.previsione_id = this.$route.params.id
      if (typeof this.previsione_id === 'undefined') {
        return
      }
      this.getBollettino()
    },
    getBollettino() {
      this.fetchPrevisione().then(response => {
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
        let previsione = data
        previsione.w30_data = { }
        if ('w30data_set' in previsione) {
         previsione.w30data_set.forEach((element) => {
            if (!(element.id_time_layouts in previsione.w30_data)) {
            previsione.w30_data[element.id_time_layouts] = { }
            }
            if (element.id_parametro in previsione.w30_data[element.id_time_layouts]) {
              if(element.id_aggregazione in previsione.w30_data[element.id_time_layouts][element.id_parametro]){
                previsione.w30_data[element.id_time_layouts][element.id_parametro][element.id_aggregazione].push(element)
              }else{
                previsione.w30_data[element.id_time_layouts][element.id_parametro][element.id_aggregazione] = [element]
              }
            } else {
            previsione.w30_data[element.id_time_layouts][element.id_parametro] = {}
            previsione.w30_data[element.id_time_layouts][element.id_parametro][element.id_aggregazione] = [element]
            }
          })
        }
        delete previsione.w30data_set
        this.previsione["Bollettino"] = previsione
        this.previsione["Bollettino"]["readonly"] = false
        this.readonly = false
        if(data.status !== "0"){
          this.readonly = true
          this.previsione["Bollettino"]["readonly"] = true
        }

        this.countdown += 1
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
    openModel(model){
      const element = document.getElementById("openselect")
      element.selectedIndex = 0
      let route = this.$router.resolve({path: `/w30/model/${model}`});
      window.open(route.href, '_blank');
    },
    copyModel(model){
      const element = document.getElementById("copyselect")
      element.selectedIndex = 0
      let stack = []
      let parameters = ["PLUV", "SNOW_LEV", "FRZLVL"]
      this.timelayouts6h.forEach(timelayout => {
        parameters.forEach(parameter => {
          for(const aggregazione in this.previsione.Bollettino.w30_data[timelayout][parameter]){
            for(const data in this.previsione.Bollettino.w30_data[timelayout][parameter][aggregazione]){
              let new_value = this.previsione[model].w30_data[timelayout][parameter][aggregazione][data].numeric_value
              this.previsione.Bollettino.w30_data[timelayout][parameter][aggregazione][data].numeric_value = new_value
              let idW30Data = this.previsione.Bollettino.w30_data[timelayout][parameter][aggregazione][data].id_w30_data

              const payload = {"id_key":"id_w30_data","id":idW30Data,"value_key":"numeric_value","new_value": new_value}
              stack.push(payload)
            }
          }
        })
      })
      const payloadusername = {"id_key":"id_w30","id":this.previsione.Bollettino.id_w30,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)
      const payload_firstguess = {"id_key":"id_w30","id":this.previsione.Bollettino.id_w30,"value_key":"firstguess","new_value": `Model: ${this.previsione[model].model} Date: ${this.previsione[model].date} Run: ${this.previsione[model].run}`}
      stack.push(payload_firstguess)
      this.saveW30(stack)
    },
    getModels() {
      console.log("getModels")
      this.modelsFetched = 0
      let url = this.base_data_url ? this.base_data_url + "/models_for_psa/" : "/models_for_psa/index.html"
      fetch(url).then(response => response.text()).then(text => {
        const parser = new DOMParser()
        const htmlDoc = parser.parseFromString(text, 'text/html')
        const as = htmlDoc.getElementsByTagName('a')
        const alist = Array.prototype.slice.call(as)
        this.availableModels = alist.map(a => a.getAttribute('href').split(".")).filter(href => href[1] === "json").map(a => a[0]).sort((a, b) => Number(a.split("_")[1]) - Number(b.split("_")[1]))
        this.availableModels.forEach(model => {
          this.previsione[model] = {readonly: true, w30_data: {}}
          fetch(`${this.base_data_url}/models_for_psa/${model}.json`)
          .then(response => response.json())
          .then(data => {
            let i = 0
            this.timelayouts6h.forEach(time_layout => {
              this.previsione[model].w30_data[time_layout] = JSON.parse(JSON.stringify(this.previsione.Bollettino.w30_data[time_layout]))
              for(const e in data.data){
                this.previsione[model].w30_data[time_layout]["PLUV"]["900"].find(element => element.id_allertamento === data.data[e]["area_allertamento"]).numeric_value = data.data[e]["PLUV"]["900"][i]
                this.previsione[model].w30_data[time_layout]["PLUV"]["125"].find(element => element.id_allertamento === data.data[e]["area_allertamento"]).numeric_value = data.data[e]["PLUV"]["125"][i]
                this.previsione[model].w30_data[time_layout]["SNOW_LEV"]["0"].find(element => element.id_allertamento === data.data[e]["area_allertamento"]).numeric_value = data.data[e]["SNOW_LEV"]["0"][i]
                this.previsione[model].w30_data[time_layout]["FRZLVL"]["0"].find(element => element.id_allertamento === data.data[e]["area_allertamento"]).numeric_value = data.data[e]["FRZLVL"]["0"][i]
              }
              i += 1
            })
            this.previsione[model].model = data.model
            this.previsione[model].date = data.date
            this.previsione[model].run = data.run
            this.modelsFetched += 1
          });
        })
      })
    },
    calculateMax() {
      this.previsione["MAX"] = {readonly: true, w30_data: {}}

      let firstguess = ""
      if (this.availableModels.findIndex(a => a === "ECMWF0100_00_D0") !== -1) {
        firstguess = "ECMWF0100_00_D0"
      } else if (this.availableModels.findIndex(a => a === "ECMWF0100_12_D1") !== -1) {
        firstguess = "ECMWF0100_12_D1"
      } else {
        firstguess = this.availableModels[0]
      }

      this.timelayouts6h.forEach(time_layout => {
        this.previsione["MAX"].w30_data[time_layout] = JSON.parse(JSON.stringify(this.previsione[firstguess].w30_data[time_layout]))
      })

      this.timelayouts6h.forEach(time_layout => {
        for(const parameter in this.previsione.MAX.w30_data[time_layout]){
          for(const aggregazione in this.previsione.MAX.w30_data[time_layout][parameter]){
            let i = 0
            this.previsione.MAX.w30_data[time_layout][parameter][aggregazione].forEach(data => {
              let max = -1
              this.availableModels.forEach(model => {
                if(max < this.previsione[model].w30_data[time_layout][parameter][aggregazione][i].numeric_value){
                  max = this.previsione[model].w30_data[time_layout][parameter][aggregazione][i].numeric_value
                  data.numeric_value = max
                  data["byModel"] = model
                }
              })
              i += 1
            })
          }
        }
      })

    },
    setmeasureFreezeSnow(payloads) {
      let stack = []

      payloads.forEach(data => {
        const id_time_layouts = data.id_time_layouts
        const id_parametro = data.id_parametro
        const id_aggregazione = data.id_aggregazione
        const new_value = data.new_value
        const id_allertamento = data.id_allertamento

        this.previsione.Bollettino.w30_data[id_time_layouts][id_parametro][id_aggregazione].find(element => element.id_allertamento === id_allertamento).numeric_value = new_value
        let idW30Data = this.previsione.Bollettino.w30_data[id_time_layouts][id_parametro][id_aggregazione].find(element => element.id_allertamento === id_allertamento).id_w30_data

        const payload = {"id_key":"id_w30_data","id":idW30Data,"value_key":"numeric_value","new_value": new_value}
        stack.push(payload)
      })
      const payloadusername = {"id_key":"id_w30","id":this.previsione.Bollettino.id_w30,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)

      this.saveW30(stack)

    },
    setMeasure(data) {
      const id_time_layouts = data.id_time_layouts
      const id_parametro = data.id_parametro
      const id_aggregazione = data.id_aggregazione
      const new_value = data.new_value
      const id_allertamento = data.id_allertamento

      this.previsione.Bollettino.w30_data[id_time_layouts][id_parametro][id_aggregazione].find(element => element.id_allertamento === id_allertamento).numeric_value = new_value
      let idW30Data = this.previsione.Bollettino.w30_data[id_time_layouts][id_parametro][id_aggregazione].find(element => element.id_allertamento === id_allertamento).id_w30_data

      let stack = []
      const payload = {"id_key":"id_w30_data","id":idW30Data,"value_key":"numeric_value","new_value": new_value}
      const payloadusername = {"id_key":"id_w30","id":this.previsione.Bollettino.id_w30,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)
      stack.push(payload)

      this.saveW30(stack)
    },
    saveW30(stack) {
      this.bulkUpdateW30(stack).then((response) => {
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
            message: 'Dati salvati',
            type: 'success',
            position: 'top-left'
        }
        )
        this.previsione.Bollettino.last_update = data.bulletin.last_update
        this.previsione.Bollettino.username = store.state.username
        this.previsione.Bollettino.firstguess = data.bulletin.firstguess
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
    execute(action, reroute, message) {
      if (action === 'resend' && !confirm('Vuoi davvero ripetere l\'invio di questo bollettino?')) {
        return
      } else {
        this.really_execute(action, reroute, message)
      }
    },
    really_execute(action, reroute, message) {
      this[action + 'ing'] = true
      this.fetchPSAAction(action).then(response => {
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
          this.$router.push({ path: `/w30/${data.id_w30}`})
          this.previsione_id = data.id_w30
          this.countdown = 0
          this.getBollettino()
        } else {
          this.getPrevisione()
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
        api.fetchBulletinDelete(this.previsione.Bollettino.id_w30, 'w30/bulletins', store).then(response => {
          if (response.ok) {
            this.$toast.open(
              {
                message: 'Bollettino cancellato',
                type: 'success',
                position: 'top-left'
              }
            )
            this.bozza_presente = false
            this.$router.push({ path: `/w30`})
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
    copyScadenzaFreezeSnow(timelayout, modelSelected){
      let stack = []
      const parameters = ["SNOW_LEV", "FRZLVL"]
      parameters.forEach(parameter => {
        for(const aggregazione in this.previsione.Bollettino.w30_data[timelayout][parameter]){
          for(const data in this.previsione.Bollettino.w30_data[timelayout][parameter][aggregazione]){
            let new_value = this.previsione[modelSelected].w30_data[timelayout][parameter][aggregazione][data].numeric_value
            this.previsione.Bollettino.w30_data[timelayout][parameter][aggregazione][data].numeric_value = new_value
            let idW30Data = this.previsione.Bollettino.w30_data[timelayout][parameter][aggregazione][data].id_w30_data
            
            const payload = {"id_key":"id_w30_data","id":idW30Data,"value_key":"numeric_value","new_value": new_value}
            stack.push(payload)
          }
        }
      })
      const payloadusername = {"id_key":"id_w30","id":this.previsione.Bollettino.id_w30,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)
      this.saveW30(stack)
    },
    copyScadenza(timelayout, parameter, modelSelected){
      let stack = []
      for(const aggregazione in this.previsione.Bollettino.w30_data[timelayout][parameter]){
        for(const data in this.previsione.Bollettino.w30_data[timelayout][parameter][aggregazione]){
          let new_value = this.previsione[modelSelected].w30_data[timelayout][parameter][aggregazione][data].numeric_value
          this.previsione.Bollettino.w30_data[timelayout][parameter][aggregazione][data].numeric_value = new_value
          let idW30Data = this.previsione.Bollettino.w30_data[timelayout][parameter][aggregazione][data].id_w30_data

          const payload = {"id_key":"id_w30_data","id":idW30Data,"value_key":"numeric_value","new_value": new_value}
          stack.push(payload)
        }
      }
      const payloadusername = {"id_key":"id_w30","id":this.previsione.Bollettino.id_w30,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)
      this.saveW30(stack)
    },
    calculateFirstGuess(timelayout, parameter, aggregazione, maxpluv){
      let stack = []
      this.previsione.Bollettino.w30_data[timelayout][parameter][aggregazione].forEach(data => {
        let new_value = maxpluv.find(e => e.id_allertamento === data.id_allertamento).numeric_value
        data.numeric_value = new_value
        let idW30Data = data.id_w30_data

        const payload = {"id_key":"id_w30_data","id":idW30Data,"value_key":"numeric_value","new_value": new_value}
        stack.push(payload)
      })
      const payloadusername = {"id_key":"id_w30","id":this.previsione.Bollettino.id_w30,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)
      this.saveW30(stack)
    },
    changeModel(model, value) {
      this.detailModels[model] = value
    },
    toggleView(timelayout, view) {
      this.overallView = view
      if(!view){
        this.$nextTick(() => {
          const element = document.getElementById(timelayout)
          element.scrollIntoView({ behavior: "smooth" })
        })
      }else{
        this.$nextTick(() => {
          const element = document.getElementById("bollettinoTitle")
          element.scrollIntoView({ behavior: "smooth" })
        })
      }
    },
    topdf(){
      window.print()
    },
    async fetchPatch(id, endpoint, payload) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w30/${endpoint}/${id}/`,
        {
          method: 'PATCH',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    async bulkUpdateW30(snapshots) {
      let payload = snapshots
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w30/data/bulk_update/`,
        {
          method: 'POST',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    async fetchPSAAction (action) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w30/bulletins/${this.previsione.Bollettino.id_w30}/${action}/`
      )
      return response
    },
  }
}
</script>

<style>
@media print {
  nav.navbar {display: none;}
  .footer {display: none;}
  .nottoprint { display: none;}
  .metadata {
    display: inline;
  }
}
</style>
