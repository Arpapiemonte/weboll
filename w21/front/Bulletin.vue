// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="container-fluid">
    <div
      class="row justify-content-end sticky-top py-1"
      style="background-color: #f8f9fa; z-index: 100;"
    >
      <!-- https://getbootstrap.com/docs/5.1/components/button-group/ -->
      <div
        class="btn-group w-auto"
        role="group"
        aria-label="Basic outlined example"
      >
        <a
          class="btn btn-outline-primary"
          :href="'/api/w21/pdf/' + autostrada.id_w21"
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
          v-if="autostrada.status === '0' && state.username"
          :disabled="actions.sending || sendable"
          type="button"
          class="btn btn-outline-success"
          @click="execute('send', false, 'Bollettino inviato')"
        >
          <span v-if="actions.sending">
            <span
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true">
            </span>
            Sto inviando il bollettino ...
          </span>
          <span v-else>
            <img
              src="~bootstrap-icons/icons/send-fill.svg"
              alt="unlock icon"
              width="18"
              height="18"
            > Invia
          </span>
        </button>
        <button
          v-if="autostrada.status === '0' && state.username"
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
        <button
          v-if="autostrada.status === '1' && state.username && autostrada.data_emissione.substring(0, 10) === today"
          type="button"
          class="btn btn-outline-warning"
          @click="execute('reopen', true, 'Bollettino riaperto')"
        >
          <span v-if="actions.reopening">
            <span
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"/>
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
      </div>
    </div>

    <div class="row mb-3">
      <h1>Strade della Provincia di Biella {{ autostrada.id_w21 }}</h1>
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="autostrada.status === '1'">
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Inviato"
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
            :value="getDateFormatted(autostrada.data_emissione, false)"
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
            :value="getDateFormatted(autostrada.last_update)"
          >
        </label>
      </div>
      <div class="col-md-1 mb-3">
        <label for="username">Autore
          <input
            id="username"
            disabled
            class="form-control"
            name="username"
            type="text"
            :value="autostrada.username"
          >
        </label>
      </div>
      <div v-if="ready">
        <div
          class="row sticky-top bg-light pt-5"
          style="z-index: 1024;"
        >
          <div class="col-md-12">
            <ul
              class="nav nav-tabs nav-justified"
              style="top: 46px;"
              role="tablist"
            >
              <li
                v-for="(value, key) in autostrada.w21_data"
                :key="key"
                class="nav-item"
                role="presentation"
              >
                <button
                  class="nav-link"
                  :class="{'active' : selected_time_layout === parseInt(key.toString()), 'text-danger' : tab_validity[key]}"
                  type="button"
                  role="tab"
                  @click="selected_time_layout = parseInt(key.toString())"
                >
                  {{ tabsDate[key] }}
                </button>
              </li>
            </ul>
          </div>
        </div>
        <div class="row">
          <div
            class="col-12 mb-3"
            style="z-index: 1023;"
          >
            <div class="row">
              <div class="col-md-6 mb-3">
                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th
                        class="text-center"
                        style="width: 8em;"
                        scope="col"
                      >
                        Località
                      </th>
                      <th
                        class="text-center"
                        style="width: 8em;"
                      >
                        Tempo Prevalente
                      </th>
                      <th
                        class="text-center"
                        style="width: 4em;"
                      >
                        Precipitazione
                      </th>
                      <th 
                        class="text-center"
                        style="width: 4em;"
                      >
                        Zero Termico
                      </th>
                      <th 
                        class="text-center"
                        style="width: 4em;"
                      >
                        Quota Neve
                      </th>
                      <th 
                        v-if="tempTitle.length > 0"
                        class="text-center"
                        style="width: 3em;"
                      >
                        {{ tempTitle }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td
                        class="text-center"
                      >
                        -
                      </td>
                      <td class="text-center">
                        <select
                          :value="placeholder.numeric_value"
                          :disabled="readonly"
                          class="form-select col"
                          @change="selectAll('SKY_CONDIT')"
                        >
                          <option
                            v-for="(d, j) in icons"
                            :key="j"
                            :value="d.id_sky_condition"
                          >
                            {{ d.description_ita }}
                          </option>
                        </select>
                      </td>
                      <td class="text-center">
                        <select
                          :value="placeholder.numeric_value"
                          :disabled="readonly"
                          class="form-select col"
                          @change="selectAll('PREC_CLASS')"
                        >
                          <option
                            v-for="(d, j) in configBi.precipitation"
                            :key="j"
                            :value="d.numeric_value"
                          >
                            {{ d.description }}
                          </option>
                        </select>
                      </td>
                      <td class="text-center">
                        <SnowInput 
                          :measure="placeholder.numeric_value"
                          :id-w21-data="0"
                          :campo="'FRZLVL'"
                          :refresher="refresher"
                          :readonly="readonly"
                          @setmeasure="selectAll('FRZLVL')"
                        />
                      </td>
                      <td class="text-center">
                        <SnowInput 
                          :measure="placeholder.numeric_value"
                          :id-w21-data="0"
                          :campo="'SNOW_LEV'"
                          :refresher="refresher"
                          :readonly="readonly"
                          @setmeasure="selectAll('SNOW_LEV')"
                        />
                      </td>
                      <td 
                        v-if="tempTitle.length > 0"
                        class="text-center"
                      >
                        <input
                          type="Number"
                          :value="placeholder.numeric_value"
                          class="form-control"
                          title="Temperatura aria"
                          :disabled="readonly"
                          @change="selectAll('TERMA')"
                        >
                      </td>
                    </tr>
                    <tr
                      v-for="tratto in autostrada.w21_data[selected_time_layout]"
                      :key="tratto.id_w21"
                    >
                      <td
                        class="text-center"
                      >
                        {{ getInfoVenue(tratto['FRZLVL'].id_venue).description + ' - ' + getInfoVenue(tratto['FRZLVL'].id_venue).quota + ' m' }}
                      </td>
                      <td class="text-center">
                        <select
                          :value="tratto['SKY_CONDIT'].numeric_value"
                          :disabled="readonly"
                          :style="skycond_validity[selected_time_layout][tratto['SKY_CONDIT'].id_venue] ? 'border: 3px solid #FFA500' : ''"
                          class="form-select col"
                          @change="setMeasure(tratto['SKY_CONDIT'].id_w21_data,'SKY_CONDIT',tratto['SKY_CONDIT'].id_venue)"
                        >
                          <option
                            v-for="(d, j) in icons"
                            :key="j"
                            :value="d.id_sky_condition"
                          >
                            {{ d.description_ita }}
                          </option>
                        </select>
                      </td>
                      <td class="text-center">
                        <select
                          :value="tratto['PREC_CLASS'].numeric_value"
                          :disabled="readonly"
                          :style="pluvValidity[selected_time_layout][tratto['PREC_CLASS'].id_venue] ? 'border: 3px solid #FF5C5C' : ''"
                          class="form-select col"
                          @change="setMeasure(tratto['PREC_CLASS'].id_w21_data,'PREC_CLASS',tratto['PREC_CLASS'].id_venue)"
                        >
                          <option
                          v-for="(d, j) in configBi.precipitation"
                            :key="j"
                            :value="d.numeric_value"
                          >
                            {{ d.description }}
                          </option>
                        </select>
                      </td>
                      <td class="text-center">
                        <SnowInput 
                          :measure="tratto['FRZLVL'].numeric_value"
                          :id-w21-data="tratto['FRZLVL'].id_w21_data"
                          :campo="'FRZLVL'"
                          :refresher="refresher"
                          :readonly="readonly"
                          @setmeasure="setMeasure(tratto['FRZLVL'].id_w21_data,'FRZLVL',tratto['FRZLVL'].id_venue)"
                        />
                      </td>
                      <td class="text-center">
                        <SnowInput 
                          :measure="tratto['SNOW_LEV'].numeric_value"
                          :id-w21-data="tratto['SNOW_LEV'].id_w21_data"
                          :campo="'SNOW_LEV'"
                          :refresher="refresher"
                          :readonly="readonly"
                          @setmeasure="setMeasure(tratto['SNOW_LEV'].id_w21_data,'SNOW_LEV',tratto['SNOW_LEV'].id_venue)"
                        />
                      </td>
                      <td 
                        v-if="tempTitle.length > 0"
                        class="text-center"
                      >
                        <input
                          v-model="tratto['TERMA'].numeric_value"
                          type="Number"
                          class="form-control"
                          title="Temperatura aria"
                          :disabled="readonly"
                          @change="setMeasure(tratto['TERMA'].id_w21_data,'TERMA',tratto['TERMA'].id_venue)"
                        >
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div
                ref="divMap"
                class="col-md-6 mb-3" 
                style="height: 700px;">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import SnowInput from './SnowInput.vue'

  export default {
    name: 'StradeBiella',
    components: {
      SnowInput
    }
  }
</script>

<script setup lang="ts">
import { Ref, ref, onMounted, computed, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vue-toast-notification'

import { Modal } from 'bootstrap'

import api from '../../src/api'
import store from '../../src/store'
import { divIcon, map, marker, tileLayer } from 'leaflet'
import { venues } from './venues'

import 'leaflet/dist/leaflet.css'

import { components } from '../../src/types/weboll'
import { configBi } from "../config";
type W21 = components["schemas"]["W21"]

const router = useRouter()
const route = useRoute()
const toast = useToast()
const divMap = ref("")
const myVenues = ref(venues)


//reactive properties
let autostrada_id = ref(NaN)
let autostrada = ref({
    id_w21: 0,
    data_emissione: '',
    status: '',
    last_update: '',
    username: '',
    w21_data: {}
})
let selected_time_layout = ref(46)
let tabsDate = ref({
  46: '',
  60: '',
  61: '',
  62: '',
  63: '',
  81: '',
  82: ''
})
let state = ref(store.state)
let ready = ref(false)
let readonly = ref(true)
let actions = ref({
  sending: false,
  reopening: false,
})
let refresher = ref(0)
let icons = ref([])
let countdown = ref(0)
let modalElement = ref({})
let myMap = ref()
let myMarkers = ref([])

const icon_blacklist = [ 10, 1, 32, 44, 45, 46 ]
const placeholder = ref({
  id_w21_data: 0,
  id_parametro: null,
  id_aggregazione: 0,
  numeric_value: null,  
  id_trend: null,
  id_w21: 0,
  id_venue: 0,
  id_time_layouts: 0,
})

const skycond_to_pluv = {
  "1": 0,
  "2": 0,
  "3": 0,
  "4": 0,
  "5": 0,
  "6": 3,
  "7": 3,
  "8": 1,
  "9": 1,
  "11": 0,
  "16": 0,
  "17": 2,
  "18": 1,
  "20": 1,
  "21": 2,
  "22": 0,
  "23": 2,
  "24": 1,
  "25": 4,
  "26": 4,
  "27": 0,
  "28": 0,
  "29": 0,
  "30": 1,
  "31": 1
}
// questa struttura stabilisce quali classi di precipitazione (intensità) sono ammesse a fronte di 
// ciascun tipo di tempo
const pluv_classlist = {
  class1: {
    //pioggia o neve debole
    icons: [ 8, 9 ],
    pluv_class: [ 1 ],
  },
  class2: {
    //pioggia o neve moderata
    icons: [ 17, 21 ],
    pluv_class: [ 2 ],
  },
  class3: {
    //pioggia o neve forte
    icons: [ 6, 7 ],
    pluv_class: [ 3 ],
  },
  class4: {
    //pioggia o neve molto forte
    icons: [ 26, 25 ],
    pluv_class: [ 4 ],
  },
  classAll: {
    // per Rovesci, Instabile, Temporali, Pioggia e neve, Vento e pioggia sono possibili tutte le classi
    icons: [ 23, 24, 20, 18, 30, 31 ],
    pluv_class: [ 1, 2, 3, 4, 5],
  },
  classNo: {
    // per tutti i tipi di tempo senza precipitazione è ammessa sono la classe assente
    icons: [ 2, 3, 4, 5, 11, 12, 16, 22, 29 ],
    pluv_class: [ 0 ],
  },
}

watch(() => countdown.value, (new_value) => {
  if(new_value > 1){
    createTabsDate()
    ready.value = true
    mountMap()
  }
})

watch(() => selected_time_layout.value, (new_value) => {
  // reset placeholder when change tab
  placeholder.value = {
    id_w21_data: 0,
    id_parametro: null,
    id_aggregazione: 0,
    numeric_value: null,  
    id_trend: null,
    id_w21: 0,
    id_venue: 0,
    id_time_layouts: 0
  }
  refreshMap()
})


const today = computed(() => {
  let d = new Date()
  return d.toISOString().substring(0, 10)
})


const pluvValidity = computed(() => {
  //borda di arancione la classe di precipitazione se non c'è coerenza tra sky_condit e precipitazione
  let validity = {}
  for(const tl in autostrada.value.w21_data){
    validity[tl] = {}
    let venues = autostrada.value.w21_data[tl]
    Object.keys(venues).forEach(d => {
      validity[tl][d] = false
      for(const classe in pluv_classlist){
        let w21data_skyc = autostrada.value.w21_data[tl][d]["SKY_CONDIT"]  
        let w21data_prec = autostrada.value.w21_data[tl][d]["PREC_CLASS"] 
        if(pluv_classlist[classe].icons.includes(w21data_skyc.numeric_value)){
          if(pluv_classlist[classe].pluv_class.includes(w21data_prec.numeric_value)){
            validity[tl][d] = false
          }else{
            validity[tl][d] = true
          }
        }
      }
    })
  }
  return validity
})
// il tab diventa rosso se c'è qualche errore bloccante
const tab_validity = computed(() => {
  let validity = {}
  for(const tl in pluvValidity.value){
    validity[tl] = false
    for(const venue in pluvValidity.value[tl]){
      if(pluvValidity.value[tl][venue]){
        validity[tl] = true
      }
      
    }
  }
  return validity
})
//skycondition di precipitazione
const pluv_skycond = [8, 17, 6, 25, 30]
//skycondition di neve
const snow_skycond = [9, 21, 7, 18, 31, 26]
const unst_skycond = [20, 23, 24] 

const skycond_validity = computed(() => {
  // borda di arancione nel caso in cui sia pioggia ma la quota neve sia prossima alla quota della stazione
  // o ci sia neve ma la quota neve sia alta. E' un warning non bloccante
  let validity = {}

  for(const tl in autostrada.value.w21_data){
    validity[tl] = {}
    let venues = autostrada.value.w21_data[tl]
    Object.keys(venues).forEach(d => {
      let w21data_skyc = autostrada.value.w21_data[tl][d]["SKY_CONDIT"]  
      let w21data_snowl = autostrada.value.w21_data[tl][d]["SNOW_LEV"] 
      let quota = getInfoVenue(d).quota
      if (pluv_skycond.includes(w21data_skyc.numeric_value) && w21data_snowl.numeric_value <= quota + 100) {
        validity[tl][d] = true
      } else if (snow_skycond.includes(w21data_skyc.numeric_value) && w21data_snowl.numeric_value > quota + 100) {
          validity[tl][d] = true
      } else {
        validity[tl][d] = false
      }
    })
  }
  return validity
})

const sendable = computed(() => {
  let validity = false
  for(const tl in tab_validity.value){
    if(tab_validity.value[tl]){
      validity = true
    }
  }
  return validity
})

const tempTitle = computed(() => {
  let temp_title = ""
  if (selected_time_layout.value === 62 ||
    selected_time_layout.value === 82 ||
    selected_time_layout.value === 46 ||
    selected_time_layout.value === 62 ||
    selected_time_layout.value === 82)
    temp_title = "Tmax"
  else if (selected_time_layout.value === 60 ||
    selected_time_layout.value === 81)
    temp_title = "Tmin"
  return temp_title
})

onMounted(() => {
  if(typeof route.params.id === 'string'){
    autostrada_id.value = parseInt(route.params.id)
  }
  fetchData()
  let element = document.getElementById('iconModal')
  if(element !== null){
    modalElement.value = new Modal(element)
  }
})

function AddIcons(){
  // funzione che disegna i markers con gli skycondition sulla mappa
  myVenues.value.forEach(async element => {
    let id_skycond = autostrada.value.w21_data[selected_time_layout.value][element.id_venue]["SKY_CONDIT"].numeric_value
    let info_sky_condition = icons.value.find((ic:any) => ic.id_sky_condition == id_skycond)
    const svg = await fetch(`/images/meteo/icons/${id_skycond}_${info_sky_condition.sky_condition}.svg`).then(response => response.text())

    let sky_cond_icon = divIcon({
      html: svg,
      className: "",
      iconSize: [70, 70],
      iconAnchor: [25, 40],
    })

    const myMarker = marker([element.lat, element.lon], { icon: sky_cond_icon }).addTo(myMap.value)
    var popoverContent = `${element.description} - ${element.quota} m`
    myMarker.bindPopup(popoverContent)
    myMarkers.value.push(myMarker)
  })
}

async function mountMap(){
  await nextTick()
  myMap.value = map(divMap.value).setView([45.602736, 8.0537645], 11)
  tileLayer('https://webgis.arpa.piemonte.it/ags/rest/services/topografia_dati_di_base/Topografica_Base_Multiscala/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'CCBY 2.5 Italia - Copyright © Agenzia Regionale per la Protezione dell\'Ambiente del Piemonte'
  }).addTo(myMap.value)
  AddIcons()
}

async function refreshMap(){
  for(var i = 0; i < myMarkers.value.length; i++){
    myMap.value.removeLayer(myMarkers.value[i]);
  }
  AddIcons()
}

function getInfoVenue(id_venue){
  let venue = myVenues.value.find(v => v.id_venue == id_venue)
  return venue
}

function forceUpdate(){
  refresher.value += 1
}

function rearrange(data: any[], key: string, func: ArrayTransformer | null = null) {
//function rearrange(data: any[], key: string, func=null) {
  // rearranges the array data in a dictionary
  // aggregating all records with the same key as an array
  // optionally transforming each array with the func function
  let value_data = {}
  let maptl_terma = {
    46: 46,
    60: 60,
    61: 61,
    62: 62,
    63: 63,
    81: 81,
    82: 82,
    50: 46, //massima D0
    68: 60, //minima D1
    67: 62, //massima D1
    85: 81, //minima D2
    84: 82 // massima D2
  }
  data.forEach((record: { [x: string]: string | number }) => {
    if (key ==="id_time_layouts")
      record[key] = maptl_terma[record[key]]
      
    if (!(record[key] in value_data)) {
      value_data[record[key]] = []
    }
    value_data[record[key]].push(record)
  })
  if (func) {
    Object.keys(value_data).forEach(key => value_data[key] = func(value_data[key]))
  }
  if (!Object.values(value_data).some(item => item != undefined)) value_data = {}
  return value_data
}

async function fetchData () {
  countdown.value = 0
  ready.value = false
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  fetchAutostrada(autostrada_id.value).then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero del bollettino`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(data => {
    let tmp = rearrange(
          data['w21data_set'],
          "id_time_layouts",
          pippo=>rearrange(pippo, "id_venue",
          pippo2=>rearrange(pippo2, "id_parametro", (arr: any[]) => arr[0] ))
        )

    autostrada.value = {
      id_w21: data.id_w21,
      data_emissione: data.data_emissione,
      status: data.status,
      last_update: data.last_update,
      username: data.username,
      w21_data: tmp
    }
    readonly.value = (autostrada.value.status === '1' || autostrada.value.status === '2' || !state.value.username)
    countdown.value += 1
  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })

  fetchIcons().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero delle icone`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(data => {
    icons.value = data.filter(icon => !icon_blacklist.includes(icon.id_sky_condition)).map(icon => {
      if (icon.classes.length > 0) {
        icon.id_parametro = icon.classes[0].id_parametro
        icon.ordinamento = icon.classes[0].ordinamento
        delete icon.classes
      } else {
        icon.id_parametro = null
        icon.ordinamento = null
      }
      return icon
    })
    countdown.value += 1
  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

function execute(action, reroute, message) {
  actions.value[action + 'ing']= true
  fetchAutostradaAction(action).then(response => {
    actions.value[action + 'ing'] = false
    if (response.ok) {
      return response.json()
    } else {
      toast.open(
        {
          message: `Errore ${response.status} nell'esecuzione del comando ${action}`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
  }).then(data => {
    toast.open(
      {
        message: message,
        type: 'success',
        position: 'top-left'
      }
    )
    if (reroute) {
      router.push({ path: `/w21/${data.id_w21}`})
      autostrada_id.value = data.id_w21
      fetchData()
    } else {
      fetchData()
    }
  }).catch((error) => {
    this[action + 'ing'] = false
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

function remove() {
  if (
    confirm('Vuoi davvero cancellare questo bollettino?')
  ) {
    api.fetchBulletinDelete(autostrada_id.value, 'w21/bulletins', store).then(response => {
      if (response.ok) {
        toast.open(
          {
            message: 'Bollettino cancellato',
            type: 'success',
            position: 'top-left'
          }
        )
        router.back()
      } else {
        toast.open(
          {
            message: `Errore ${response.status} nella cancellazione del bollettino`,
            type: 'error',
            position: 'top-left'
          }
        )
      }
    }).catch(error => {
      toast.open(
        {
          message: error,
          type: 'error',
          position: 'top-left'
        }
      )
    })
  }
}

function setMeasure(id_w21_data, campo, id_venue){
  // questa funzione ricava il nuovo valore da salvare
  if(window.event && window.event.target !== null){
    let new_value = parseInt((window.event.target as HTMLInputElement).value)
    saveW21Data(id_w21_data, campo, id_venue, new_value)
  }
}

function saveW21Data(id_w21_data, campo, id_venue, new_value){
  // funzione che prepara lo "stack", ovvero l'array con le modifiche da mandare al bulk_update del backend
  let w21data = autostrada.value.w21_data[selected_time_layout.value][id_venue]
  let stack : Array<Object> = []
  
  // se sto salvando uno sky_condition di precipitazione allora aggiorno anche la classe di pioggia corrispondente
  if(campo === 'SKY_CONDIT'){ 
    for(const classe in pluv_classlist){
      if(pluv_classlist[classe].icons.includes(new_value)){
        let pluv_value = skycond_to_pluv[new_value]
        const payloadPioggia = {"id_key":"id_w21_data","id":w21data["PREC_CLASS"].id_w21_data,"value_key":"PREC_CLASS","new_value": pluv_value }
        w21data["PREC_CLASS"].numeric_value = pluv_value
        stack.push(payloadPioggia)
      }
    }
  }
  let value = new_value
  if(isNaN(new_value)){
    value = null
  }
  const payload = {"id_key":"id_w21_data","id":w21data[campo].id_w21_data,"value_key":campo,"new_value": value}
  const payloadusername = {"id_key":"id_w21","id":autostrada.value.id_w21,"value_key":"username","new_value": store.state.username}
  w21data[campo].numeric_value = value
  
  stack.push(payload)
  stack.push(payloadusername)

  saveW21(stack)
}

function saveAll(campo, new_value){
  // funzione per il salvataggio su tutte le venue
  let venues = autostrada.value.w21_data[selected_time_layout.value]
  
  let stack : Array<Object> = []

  Object.keys(venues).forEach(d => {
    let w21data = autostrada.value.w21_data[selected_time_layout.value][d]
    const payload = {"id_key":"id_w21_data","id":w21data[campo].id_w21_data,"value_key":campo,"new_value": new_value}
    w21data[campo].numeric_value = new_value
    stack.push(payload)
  
    // se sto salvando uno sky_condition, controllo se è di precipitazione e allora aggiorno anche la classe di intensità corrispondente 
    // in tutte le venue
    if (campo == "SKY_CONDIT"){
      const arraypluv = pluv_skycond.concat(snow_skycond).concat(unst_skycond)
      if(arraypluv.includes(new_value)){
        let pluv_value = skycond_to_pluv[new_value]
        const payloadPioggia = {"id_key":"id_w21_data","id":w21data["PREC_CLASS"].id_w21_data,"value_key":"PREC_CLASS","new_value": pluv_value }
        w21data["PREC_CLASS"].numeric_value = pluv_value
        stack.push(payloadPioggia)
      }
    }
  })
  
  const payloadusername = {"id_key":"id_w21","id":autostrada.value.id_w21,"value_key":"username","new_value": store.state.username}

  stack.push(payloadusername)
  saveW21(stack)
}

function selectAll(campo){
  if(window.event && window.event.target !== null){
    let new_value:number|null = parseInt((window.event.target as HTMLInputElement).value)
    new_value = Number.isNaN(new_value) ? null : new_value

    saveAll(campo, new_value)
  }
}

function saveW21(stack) {
  forceUpdate()
  bulkUpdateW21(stack).then((response) => {
    if (response === undefined || !response.ok) {
      toast.open(
        {
          message: 'Errore nel salvataggio',
          type: 'error',
          position: 'top-left'
        }
      )
    }else{
      return response.json()
    }
  }).then(data => {
    toast.open(
      {
        message: 'Dato salvato',
        type: 'success',
        position: 'top-left'
      }
    )
    autostrada.value.last_update = data.bulletin.last_update
    autostrada.value.username = store.state.username || ""
    refreshMap()
  }).catch((error) => {
    toast.open(
      {
        message: `Errore di comunicazione: ${error}`,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

function createTabsDate(){
  let today = dateToString(new Date(autostrada.value.data_emissione))
  let tomorrow = dateToString(new Date(new Date(autostrada.value.data_emissione).setDate(new Date(autostrada.value.data_emissione).getDate()+1)))
  let afterTomorrow = dateToString(new Date(new Date(autostrada.value.data_emissione).setDate(new Date(autostrada.value.data_emissione).getDate()+2)))
  tabsDate.value = {
    46: `${today} 18-24`,
    60: `${tomorrow} 00-06`,
    61: `${tomorrow} 06-12`,
    62: `${tomorrow} 12-18`,
    63: `${tomorrow} 18-24`,
    81: `${afterTomorrow} 00-12`,
    82: `${afterTomorrow} 12-24`
  }
}

function dateToString(date): String{
  const yy = date.getFullYear()
  const mm = date.getMonth() + 1
  const dd = date.getDate()
  return [yy, (mm>9 ? '' : '0') + mm, (dd>9 ? '' : '0') + dd].join('-')
}

function getDateFormatted(rawString, time = true) {
  return api.getDateFormatted(rawString, time)
}

async function fetchAutostradaAction (action) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w21/bulletins/${autostrada_id.value}/${action}/`
  )
  return response
}

async function fetchAutostrada (id) {
  const response = await fetch('/api/w21/bulletins/' + id + '/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchIcons () {
  const response = await fetch('/api/w05/sky_conditions/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function bulkUpdateW21(payload) {
  // richiamo il bulk_update lato backend
  if(store.state.access !== null){
    const response = await api.fetch_wrapper(
      store.state.access,
      `/api/w21/bulletins/bulk_update/`,
      {
        method: 'POST',
        body: JSON.stringify(payload)
      }
    )
    return response
  }else{
    toast.open(
      {
        message: `Errore: non sei loggato`,
        type: 'error',
        position: 'top-left'
      }
    )
  }
  
}
</script>

<style>
table {
  table-layout: auto;
  width: 400px;
}

th {
  white-space: normal;
}

.nevetd {
  width: 60%;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="Number"] {
  appearance: textfield;
}
</style>