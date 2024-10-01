// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <IconModal
    :icons="icons"
    :venues-selected="venuesSelected"
    @set-icon="setIcons"
  />
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
        <!-- <a
          disabled
          class="btn btn-outline-primary"
          :href="'/api/w33/pdf/' + metap.id_w33"
          target="_blank"
          role="button"
        >
          <img
            src="~bootstrap-icons/icons/file-earmark-pdf-fill.svg"
            alt="PDF icon"
            width="18"
            height="18"
          > PDF
        </a> -->
        <button
          v-if="metap.status === '0' && state.username"
          :disabled="sending"
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
              src="~bootstrap-icons/icons/send-fill.svg"
              alt="unlock icon"
              width="18"
              height="18"
            > Invia
          </span>
        </button>
        <button
          v-if="metap.status === '1' && state.username && metap.data_emissione === today"
          type="button"
          class="btn btn-outline-warning"
          @click="execute('reopen', true, 'Bollettino riaperto')"
        >
          <span v-if="actions.reopening">
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
          v-if="metap.status === '0' && state.username"
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

    <div class="row mb-3">
      <h1>Metaprodotto {{ metap.seq_num }}</h1>
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="metap.status === '1'">
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
            :value="getDateFormatted(metap.data_emissione, false)"
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
            :value="getDateFormatted(metap.last_update)"
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
            :value="metap.username"
          >
        </label>
      </div>
      <div class="col-md-1 mb-3">
        <button
          type="button"
          class="btn btn-outline-primary btn-sm"
          @click="openTab('/images/autostrade/tab-soglie-w33.png')"
        >
          <img
            src="/images/autostrade/logo_tabelle_soglia_neve.png"
            width="55"
            height="55"
          >
        </button>
      </div>
      <div class="col-md-2 mb-3">
        <div class="form-check form-switch mt-4">
          <input 
            id="viewMapCheck" 
            v-model="viewMap" 
            class="form-check-input" 
            type="checkbox"
          >
          <label
            v-if="viewMap"
            class="form-check-label" 
            for="viewMapCheck"
          >
            Passa a Modalità Tabellare
          </label>
          <label
            v-else
            class="form-check-label" 
            for="viewMapCheck"
          >
            Passa a Modalità Mappa
          </label>
        </div>
      </div>
      <div class="col-md-2 mb-3">
        <div class="form-check form-switch mt-4">
          <input 
            id="viewMapCheck" 
            v-model="colorMap" 
            class="form-check-input" 
            type="checkbox"
          >
          <label
            v-if="colorMap"
            class="form-check-label" 
            for="viewMapCheck"
          >
            Passa a mappa in bianco e nero
          </label>
          <label
            v-else
            class="form-check-label" 
            for="viewMapCheck"
          >
            Passa a mappa a colori
          </label>
        </div>
      </div>
      <div 
        v-if="ready" 
      > 
        <div
          class="row sticky-top bg-light pt-5"
          style="z-index: 1021;"
        >
          <div class="col-md-12">
            <ul
              class="nav nav-tabs nav-justified"
              style="top: 46px;"
              role="tablist"
            >
              <li
                v-for="(value, key) in metap.w33_data"
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
        <div 
          v-if="viewMap"
          class="row"
        >
          <div
            class="col-md-5 mb-3"
          >
            <NeveMap
              :datatab="metap.w33_data[selected_time_layout]"
              :icons="icons"
              :venue-names="venueNames"
              :show-autostrade="showAutostrade"
              :heights="heights"
              :readonly="readonly"
              :cumulated-snow-validity="cumulatedSnowValidity[selected_time_layout]"
              :snow-level-info="snowLevelInfo[selected_time_layout]"
              @set-neve="setMeasure"
            />
          </div>
          <div
            class="col-md-5 mb-3"
          > 
            <div>
              <IconeMap
                :datatab="metap.w33_data[selected_time_layout]"
                :icons="icons"
                :venues-selected="venuesSelected"
                :show-autostrade="showAutostrade"
                :readonly="readonly"
                :campo-icon="'id_sky_condition'"
                @open-modal="openModal"
                @update-venue-selected="updateVenueSelected"
              />
            </div>
          </div>
        </div>
        <div 
          v-else
          class="row"
        >
          <div
            class="col-md-6 mb-3"
            style="z-index: 1020;"
          >
            <div class="row">
              <TabAutostrade
                :datatab="metap.w33_data[selected_time_layout]"
                :venue-names="venueNames"
                :icons="icons"
                :readonly="readonly"
                :heights="heights"
                :cumulated-snow-validity="cumulatedSnowValidity[selected_time_layout]"
                :snow-level-info="snowLevelInfo[selected_time_layout]"
                :skycond-validity="skycond_validity[selected_time_layout]"
                :autostrade-colors="autostradeColors"
                @save-w33-data="setMeasure"
                @set-neve="setMeasure"
              />
            </div>         
          </div>
          <div
            class="col-md-5 mb-3"
            style="z-index: 0;"
          >
            <div class="row sticky-top">
              <div class="text-end mt-4">
                <input 
                  id="viewMapCheck" 
                  v-model="mapChoice" 
                  class="form-check-input" 
                  type="checkbox"
                >
                <label
                  v-if="mapChoice"
                  class="form-check-label" 
                  for="viewMapCheck"
                >
                  Visualizza Mappa Neve
                </label>
                <label
                  v-else
                  class="form-check-label" 
                  for="viewMapCheck"
                >
                  Visualizza Mappa Icone
                </label>
              </div>
              <div
                v-if="mapChoice"
              >
                <IconeMap
                  :datatab="metap.w33_data[selected_time_layout]"
                  :icons="icons"
                  :show-autostrade="showAutostrade"
                  :venues-selected="venuesSelected"
                  :readonly="readonly"
                  :campo-icon="'id_sky_condition'"
                  @open-modal="openModal"
                  @update-venue-selected="updateVenueSelected"
                />
              </div>
              <div
                v-else
              >
                <NeveMap
                  :datatab="metap.w33_data[selected_time_layout]"
                  :icons="icons"
                  :venue-names="venueNames"
                  :show-autostrade="showAutostrade"
                  :heights="heights"
                  :readonly="readonly"
                  :cumulated-snow-validity="cumulatedSnowValidity[selected_time_layout]"
                  :snow-level-info="snowLevelInfo[selected_time_layout]"
                  @set-neve="setMeasure"
                />
              </div>
            </div>
          </div>
        </div>
        <div>
          <div class="d-flex justify-content-end">
            <div class="form-group row">
              <div
                v-for="(value, key) in showAutostrade"
                :key="key"
                class="col badge"
                :style="'background-color: ' + autostradeColors[key]"
              >
                <button
                  type="button"
                  class="btn btn-light btn-sm"
                  :disabled="readonly"
                  @click="showAutostrade[key] = !showAutostrade[key]"
                >
                  <img
                    v-if="showAutostrade[key]"
                    src="~bootstrap-icons/icons/eye-slash.svg"
                    alt="PDF icon"
                    width="18"
                    height="18"
                  >
                  <img
                    v-else
                    src="~bootstrap-icons/icons/eye.svg"
                    alt="PDF icon"
                    width="18"
                    height="18"
                  >
                </button>
                <h5>{{ key.toUpperCase() }}</h5>
                <button
                  type="button"
                  class="btn btn-light btn-sm"
                  :disabled="readonly"
                  @click="selectAutostrade(key)"
                >
                  <img
                    src="~bootstrap-icons/icons/archive-fill.svg"
                    alt="PDF icon"
                    width="18"
                    height="18"
                  >
                </button>
              </div>
              <div class="col badge">
                <button
                  type="button"
                  class="btn btn-outline-primary btn-sm"
                  :disabled="readonly"
                  @click="venuesSelected = []"
                >
                  <img
                    src="~bootstrap-icons/icons/trash3-fill.svg"
                    alt="PDF icon"
                    width="18"
                    height="18"
                  >
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <AutostradeMap 
    :color-map="colorMap"
  />
</template>

<script lang="ts">
  import TabAutostrade from './TabAutostrade.vue'
  import IconeMap from './IconeMap.vue'
  import IconModal from './IconModal.vue'
  import AutostradeMap from './AutostradeMap.vue'
  import NeveMap from './NeveMap.vue'

  export default {
    name: 'MetaprodottoBulletin',
    components: {
      TabAutostrade,
      IconeMap,
      IconModal,
      AutostradeMap,
      NeveMap
    }
  }
</script>

<script setup lang="ts">

import { Ref, ref, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vue-toast-notification'

import { Modal } from 'bootstrap'

import api from '../../src/api'
import store from '../../src/store'

import { components } from '../../src/types/weboll'
import type { W33Processed, TabsDate, Icons, VenueNames } from "../types"

const router = useRouter()
const route = useRoute()
const toast = useToast()

type W33Full = components['schemas']['W33'] & { w33data_set: components['schemas']['W33Data'][] }

let showAutostrade = ref({
  a26: true,
  a6: true,
  a4: true,
  a21: true,
  a33: true,
})

// reactive properties
let metap_id = ref("")
let selected_time_layout = ref(45)
let state = ref(store.state)
let ready = ref(false)
let readonly = ref(true)
let sending = ref(false)
let viewMap = ref(true)
let colorMap = ref(true)
let mapChoice = ref(true)
let icons : Ref<Icons> = ref([])
let venueNames : Ref<VenueNames> = ref({})
let countdown = ref(0)
let venuesSelected : Ref<Array<string>> = ref([])
let metap : Ref<W33Processed> = ref({
    id_w33: 0,
    data_emissione: '',
    seq_num: 0,
    status: '0',
    /** Format: date-time */
    last_update: '',
    username: '',
    w33_data: {
      45: [],
      46: [],
      60: [],
      61: [],
      62: [],
      63: [],
      81: [],
      82: []
    }
})
let tabsDate : Ref<TabsDate> = ref({
  45: '',
  46: '',
  60: '',
  61: '',
  62: '',
  63: '',
  81: '',
  82: ''
})

let autostradeCheck = ref({
  a26: false,
  a4: false,
  a6: false,
  a21: false,
  a33: false,
})
const props = defineProps({
  id: {
      type: String,
      default: () => ''
  },
})


const heights = ref({
  '99': {min: 207, max : 265},
  '100': {min: 205, max : 300},
  '101': {min: 142, max : 245},
  '102': {min: 90, max : 166},
  '103': {min: 106, max : 251},
  '104': {min: 252, max : 325},
  '105': {min: 199, max : 455},
  '19': {min: 166, max : 213},
  '25': {min: 185, max : 215},
  '41': {min: 116, max : 166},
  '47': {min: 214, max : 224},
  '94': {min: 218, max : 411},
  '95': {min: 382, max : 435},
  '96': {min: 370, max : 655},
  '97': {min: 25, max : 410},
  '24': {min: 65, max : 110},
  '49': {min: 120, max : 190},
  '66': {min: 244, max : 255},
  '106': {min: 116, max : 260},
  '107': {min: 85, max : 90},
  '108': {min: 50, max : 70},
  '187': {min: 450, max : 540},
  '188': {min: 240, max : 350},
  '189': {min: 160, max : 220},
})


let modalElement = ref({})

const actions = ref({
  sending: false,
  reopening: false,
})

const autostrade = {
  a26: ['99', '100', '101', '102', '103', '104', '105'],
  a4: ['19', '25', '41', '47'],
  a6: ['94', '95', '96', '97'],
  a21: ['24', '49', '66', '106', '107', '108'],
  a33: ['187', '188', '189']
}

const autostradeColors = {
  a26: '#F21111',
  a7: '#F21111',
  a4: '#880ED4',
  a6: '#1638DB',
  a21: '#F7A706',
  a33: '#F91EDA'
}
const icon_blacklist = [ 10, 1, 32, 44, 45, 46 ]

// TODO: CONVERT sending -> actions.sending
// let actions = ref({ sending: false })

watch(() => countdown.value, (new_value) => {
  if(new_value > 2){
    readonly.value = (metap.value.status === '1' || metap.value.status === '2' || !state.value.username)
    createTabsDate()
    ready.value = true
  }
})

watch(() => venuesSelected.value, (new_value) => {
  for(const autostrada in autostrade){
    autostradeCheck.value[autostrada] = true
    autostrade[autostrada].forEach(tratto => {
      if(!new_value.includes(parseInt(tratto))){
        autostradeCheck.value[autostrada] = false
      }
    })
  }
})

watch(() => showAutostrade.value, (new_value) => {
  for(const autostrada in new_value){
    if(!new_value[autostrada]){
      autostrade[autostrada].forEach(a => {
        if(venuesSelected.value.includes(a)){
          venuesSelected.value = venuesSelected.value.filter(v => v !== a)
        }
      })
    }
  }
}, { deep: true })

const snow_classlist = {
  class1: {
    icons: [ 9 ],
    min6: -1,
    max6: 5,
    min12: -1,
    max12: 10,
    isNull: false
  },
  class2: {
    icons: [ 21 ],
    min6: 5,
    max6: 15,
    min12: 10,
    max12: 30,
    isNull: false
  },
  class3: {
    icons: [ 7 ],
    min6: 15,
    max6: 25,
    min12: 30,
    max12: 50,
    isNull: false
  },
  class4: {
    icons: [ 26 ],
    min6: 25,
    max6: 9999,
    min12: 50,
    max12: 9999,
    isNull: false
  },
  classAll: {
    icons: [ 18, 31, 44 ],
    min6: -1,
    max6: 9999,
    min12: -1,
    max12: 9999,
    isNull: false
  },
  classNo: {
    icons: [ 1, 10, 11, 12, 16, 17, 2, 20, 22, 23, 24, 25, 29, 3, 30, 32, 4, 45, 46, 5, 6, 8 ],
    min6: 0,
    max6: 0,
    min12: 0,
    max12: 0,
    isNull: true
  },
}

const pluv_skycond = [8, 17, 6, 25]

const today = computed(() => {
  let d = new Date()
  return d.toISOString().substring(0, 10)
})

const cumulatedSnowValidity = computed(() => {
  let validity = {}
  for(const tl in metap.value.w33_data){
    validity[tl] = {}
    metap.value.w33_data[tl].forEach(e => {
      validity[tl][e.id_venue] = false
      for(const classe in snow_classlist){
        if([ 45, 46, 60, 61, 62, 63].includes(parseInt(tl))){
          if(snow_classlist[classe].icons.includes(e.id_sky_condition)){
            if(snow_classlist[classe].isNull && e.cumulated_snow === null){
              validity[tl][e.id_venue] = false
            }else if((e.cumulated_snow !== null || e.cumulated_snow !== 0) && e.snow_level > heights.value[e.id_venue].max + 100){
              validity[tl][e.id_venue] = true
            }else if(snow_classlist[classe].min6 < e.cumulated_snow && snow_classlist[classe].max6 >= e.cumulated_snow && e.cumulated_snow !== null){
              validity[tl][e.id_venue] = false
            }else{
              validity[tl][e.id_venue] = true
            }
          }
        }else if ([81, 82].includes(parseInt(tl))){
          if(snow_classlist[classe].icons.includes(e.id_sky_condition)){
            if(snow_classlist[classe].isNull && e.cumulated_snow === null){
              validity[tl][e.id_venue] = false
            }else if((e.cumulated_snow !== null || e.cumulated_snow !== 0) && e.snow_level > heights.value[e.id_venue].max + 100){
              validity[tl][e.id_venue] = true
            }else if(snow_classlist[classe].min12 < e.cumulated_snow && snow_classlist[classe].max12 >= e.cumulated_snow){
              validity[tl][e.id_venue] = false
            }else{
              validity[tl][e.id_venue] = true
            }
          }
        }
      }
    })
  }
  return validity
})

const tab_validity = computed(() => {
  let validity = {}
  for(const tl in cumulatedSnowValidity.value){
    validity[tl] = false
    for(const snow in cumulatedSnowValidity.value[tl]){
      if(cumulatedSnowValidity.value[tl][snow]){
        validity[tl] = true
      }
    }
  }
  return validity
})

const skycond_validity = computed(() => {
  let validity = {}
  for(const tl in metap.value.w33_data){
    validity[tl] = {}
    metap.value.w33_data[tl].forEach(data => {
      if(pluv_skycond.includes(data.id_sky_condition) && data.snow_level <= heights.value[data.id_venue].max + 100){
        validity[tl][data.id_venue] = true
      }else{
        validity[tl][data.id_venue] = false
      }
    })
  }
  return validity
})

const snowLevelInfo = computed(() => {
  let info = {}
  for(const tl in metap.value.w33_data){
    info[tl] = {}
    metap.value.w33_data[tl].forEach(e => {
      info[tl][e.id_venue] = false
      if(e.snow_level < heights.value[e.id_venue].max + 100 && e.snow_level !== null){
        info[tl][e.id_venue] = true
      }
    })
  }
  return info
})

onMounted(() => {
  metap_id.value = props.id

  fetchData()
  modalElement.value = new Modal(document.getElementById('iconModal'))
})



async function fetchData () {
  countdown.value = 0
  ready.value = false
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  fetchMetap(metap_id.value).then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero del bollettino`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json() as Promise<W33Full>
  }).then(data => {
    let tmp = {
      45: [],
      46: [],
      60: [],
      61: [],
      62: [],
      63: [],
      81: [],
      82: []
    }
    if ('w33data_set' in data) {
      data.w33data_set.forEach((element) => {
        tmp[element.id_time_layouts].push(element)
      })
    }

    metap.value = {
      id_w33: data.id_w33,
      data_emissione: data.data_emissione,
      seq_num: data.seq_num,
      status: data.status,
      last_update: data.last_update,
      username: data.username,
      w33_data: tmp
    }
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

  fetchVenues().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero delle venues`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(data => {
    for(const element of data){    
      venueNames.value[element.id_venue] = element.description
    }
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

function selectAutostrade(autostrada){
  if(!autostradeCheck.value[autostrada]){
    autostrade[autostrada].forEach(e => {
      if(!venuesSelected.value.includes(parseInt(e))){
        venuesSelected.value.push(parseInt(e))
      }
    })
    autostradeCheck.value[autostrada] = true
  }else{
    autostrade[autostrada].forEach(e => {
      if(venuesSelected.value.includes(parseInt(e))){
        venuesSelected.value = venuesSelected.value.filter(v => v !== parseInt(e))
      }
    })
    autostradeCheck.value[autostrada] = false
  }
}

function createTabsDate(){
  let today = dateToString(new Date(metap.value.data_emissione))
  let tomorrow = dateToString(new Date(new Date(metap.value.data_emissione).setDate(new Date(metap.value.data_emissione).getDate()+1)))
  let afterTomorrow = dateToString(new Date(new Date(metap.value.data_emissione).setDate(new Date(metap.value.data_emissione).getDate()+2)))
  tabsDate.value = {
    45: `${today} 12-18`,
    46: `${today} 18-24`,
    60: `${tomorrow} 00-06`,
    61: `${tomorrow} 06-12`,
    62: `${tomorrow} 12-18`,
    63: `${tomorrow} 18-24`,
    81: `${afterTomorrow} 00-12`,
    82: `${afterTomorrow} 12-24`
  }
}

function openModal(){
  modalElement.value.show()
}

function closeModal(){
  modalElement.value.hide()
}

function openTab (path) {
  window.open(path, "_blank");
}

function updateVenueSelected(venues){
  venuesSelected.value = venues
}

const icon_list = [ 1, 10, 11, 12, 16, 17, 2, 20, 22, 23, 24, 25, 29, 3, 30, 32, 4, 45, 46, 5, 6, 8 ]

function setIcons(id_sky_condition){  
  let stack : Array<Object> = []
  venuesSelected.value.forEach(venue => {
    let w33data = metap.value.w33_data[selected_time_layout.value].find(e => e.id_venue === parseInt(venue))
    const payload = {"id_key":"id_w33_data","id":w33data.id_w33_data,"value_key":"id_sky_condition","new_value": id_sky_condition}

    if(icon_list.includes(id_sky_condition) && w33data.cumulated_snow !== null){
      const payloadAzzeramento = {"id_key":"id_w33_data","id":w33data.id_w33_data,"value_key":"cumulated_snow","new_value": null}
      w33data["cumulated_snow"] = null
      stack.push(payloadAzzeramento)
    }

    w33data["id_sky_condition"] = id_sky_condition
    stack.push(payload)    
  })

  venuesSelected.value = []
  closeModal()
  const payloadusername = {"id_key":"id_w33","id":metap.value.id_w33,"value_key":"username","new_value": store.state.username}
  stack.push(payloadusername)
  saveW33(stack)
}

function setMeasure(id_venue, campo, new_value){
  let w33data = metap.value.w33_data[selected_time_layout.value].find(e => e.id_venue === id_venue)
  let stack : Array<Object> = []

  if(campo === 'id_sky_condition' && icon_list.includes(new_value)){
    const payloadAzzeramento = {"id_key":"id_w33_data","id":w33data.id_w33_data,"value_key":"cumulated_snow","new_value": null}
    w33data["cumulated_snow"] = null
    stack.push(payloadAzzeramento)
  }

  let value = new_value
  if(isNaN(new_value)){
    value = null
  }

  const payload = {"id_key":"id_w33_data","id":w33data.id_w33_data,"value_key":campo,"new_value": value}
  const payloadusername = {"id_key":"id_w33","id":metap.value.id_w33,"value_key":"username","new_value": store.state.username}
  
  w33data[campo] = value
  stack.push(payload)
  stack.push(payloadusername)
  
  saveW33(stack)
}

async function fetchMetap (id) {
  const response = await fetch('/api/w33/bulletins/' + id + '/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

function getDateFormatted(rawString, time = true): String {
  return api.getDateFormatted(rawString, time)
}

function dateToString(date): String{
  const yy = date.getFullYear()
  const mm = date.getMonth() + 1
  const dd = date.getDate()
  return [yy, (mm>9 ? '' : '0') + mm, (dd>9 ? '' : '0') + dd].join('-')
}

function saveW33(stack) {
  bulkUpdateW33(stack).then((response) => {
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
    metap.value.last_update = data.bulletin.last_update
    metap.value.username = store.state.username || ""
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

function remove() {
  if (
    confirm('Vuoi davvero cancellare questo bollettino?')
  ) {
    if(typeof store.state.access === 'string'){
      api.fetchBulletinDelete(metap_id.value, 'w33/bulletins', store).then(response => {
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
}

async function fetchMetapAction (action) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w33/bulletins/${metap_id.value}/${action}/`
  )
  return response
}

function execute(action, reroute, message) {
  actions.value[action + 'ing'] = true
  let check = true

  if(action === 'send'){
    let message = "Ci sono i seguenti warning di validità: \n"
    let errorFounded = false
    for(const tl in cumulatedSnowValidity.value){
      for(const validity in cumulatedSnowValidity.value[tl]){
        if(cumulatedSnowValidity.value[tl][validity]){
          message += venueNames.value[validity] + " - " + tabsDate.value[tl] + "\n"
          errorFounded = true
        }
      }
    }

    message += "\nVuoi davvero inviare?"

    if(errorFounded){
      check = confirm(message)
    }
  }

  if(check){
    console.log("op")
    fetchMetapAction(action).then(response => {
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
        router.push({ path: `/w33/${data.id_w33}`})
        metap_id.value = data.id_w33
        fetchData()
      } else {
        fetchData()
      }
    }).catch((error) => {
      actions.value[action + 'ing'] = false
      toast.open(
        {
          message: error,
          type: 'error',
          position: 'top-left'
        }
      )
    })
  }else{
    actions.value[action + 'ing'] = false
  }
}

async function fetchIcons () {
  const response = await fetch('/api/w05/sky_conditions/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchVenues () {
  const response = await fetch('/api/w05/venue_names/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function bulkUpdateW33(payload) {
  if(store.state.access !== null){
    const response = await api.fetch_wrapper(
      store.state.access,
      `/api/w33/bulletins/bulk_update/`,
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
  .bgA26{
    background-color:#F21111;
  }
  .bgA6{
    background-color:#1638DB;
  }
  .bgA21{
    background-color:#F7A706;
  }
  .bgA4{
    background-color:#880Ed4;
  }
</style>