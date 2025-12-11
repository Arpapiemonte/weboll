// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
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
        <button
          v-if="previsioneAreeMeteo.status === '0' && state.username"
          :disabled="actions.sending || !validityObject['bollettino_ok']"
          type="button"
          class="btn btn-outline-success"
          @click="execute('send', false, 'Bollettino inviato')"
        >
          <span v-if="actions.sending">
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
          v-if="previsioneAreeMeteo.status === '1' && state.username && previsioneAreeMeteo.data_emissione.substring(0, 10) === today"
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
          v-if="previsioneAreeMeteo.status === '0' && state.username"
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
      <div class="row mb-3">
        <h1>Previsione Aree Meteo {{ previsioneAreeMeteo.id_w35 }}</h1>
      </div>
      <div class="row">
        <div class="col-md-2 mb-3">
          <label for="status">Stato
            <span v-if="previsioneAreeMeteo.status === '1'">
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
              :value="getDateFormatted(previsioneAreeMeteo.data_emissione, false)"
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
              :value="getDateFormatted(previsioneAreeMeteo.last_update)"
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
              :value="previsioneAreeMeteo.username"
            >
          </label>
        </div>
        <div v-if="ready">
          <div
            class="row sticky-top bg-light pt-2"
            style="z-index: 1024;"
          >
            <div class="col-md-12">
              <ul
                class="nav nav-tabs nav-justified"
                style="top: 46px;"
                role="tablist"
              >
                <li
                  v-for="(value, key) in previsioneAreeMeteo.w35_data"
                  :key="key"
                  class="nav-item"
                  role="presentation"
                >
                  <button
                    class="nav-link"
                    :class="{'active' : selected_time_layout === key.toString() ,'text-danger' : !validityObject[key]['tab']}"
                    type="button"
                    role="tab"
                    @click="selected_time_layout = key.toString()"
                  >
                    {{ tabsDate[key] }}
                    <!-- {{ key }} --><!-- debug id_time_layouts--> 
                  </button>
                </li>
              </ul>
            </div>
          </div>
          <div
            class="row"
          > 
            <div
              class="col-md-7 mb-3"
              style="z-index: 1023;"
            >
              <div class="row">
                <div class="col-md-12 mb-3">
                  <table class="table table-striped">
                    <thead>
                      <tr>
                        <th
                          class="text-center"
                          style="width: 4em;"
                          scope="col"
                        >
                          Area Meteo
                        </th>
                        <th
                          class="text-center"
                          style="width: 10em;"
                          scope="col"
                        >
                          Descrizione
                        </th>
                        <th
                          class="text-center"
                          style="width: 8em;"
                        >
                          Tempo prevalente
                        </th>
                        <th
                          class="text-center"
                          style="width: 3em;"
                        >
                          Zero<br>Termico (m)
                        </th>
                        <th
                          class="text-center"
                          style="width: 5em;"
                        >
                          Quota<br>neve (m)
                        </th>
                        <th
                          class="text-center"
                          style="width: 5em;"
                        >
                          Mantieni<br>l'icona
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <!-- inizio campi che fanno la saveAll -->
                      <tr>
                        <td
                          class="text-center"
                        >
                          -
                        </td>
                        <td
                          class="text-center"
                        >
                          -
                        </td>
                        <td class="text-center">
                          <select
                            :value="placeholder.id_sky_condition"
                            :disabled="readonly"
                            class="form-select col"
                            @change="selectAll('SKY_12', 'numeric_value')"
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
                        <td>
                          <input
                            type="number"
                            class="form-control col"
                            step="100"
                            min="0" 
                            max="6000"
                            :value="placeholder.freezing_level"
                            :disabled="readonly"
                            @change="selectAll('ZERO', 'numeric_value')"
                          >
                        </td>
                        <td class="text-center">
                          <input
                            type="number"
                            class="form-control col"
                            step="100"
                            min="0" 
                            max="6000"
                            :value="placeholder.snow_level"
                            :disabled="readonly"
                            @change="selectAll('SNOW_LEV', 'numeric_value')"
                          >
                        </td>
                        <td class="text-center">
                          <input
                            v-model="placeholder.ignore_refresh_forecast_comuni"
                            class="form-check-input"
                            type="checkbox"
                            :disabled="readonly"
                            @change="checkAll()"
                          >
                        </td>
                      </tr>
                      <!-- fine campi che fanno la saveAll-->
                      <tr
                        v-for="(zona, key) in previsioneAreeMeteo.w35_data[selected_time_layout]"
                        :key="zona"
                      >
                        <td
                          class="text-center"
                          :class="venuesSelected.includes(key) ? 'gray-td' : 'white-td'"
                        >
                          {{ key }}
                        </td>
                        <td
                          class="text-center"
                          :class="venuesSelected.includes(key) ? 'gray-td' : 'white-td'"
                        >
                          {{ AreeMeteoNames[key] }}
                        </td>
                        <td 
                          class="text-center"
                          :class="venuesSelected.includes(key) ? 'gray-td' : 'white-td'"
                        >
                          <select
                            :value="parseInt(zona.SKY_12.numeric_value)"
                            :disabled="readonly"
                            :style="validityObject[selected_time_layout][key]['SKY_12'] ? '':'border:2px solid red;'"
                            class="form-select col"
                            @change="setMeasure(zona.SKY_12.id_w35_data, 'SKY_12', key)"
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
                        <td 
                          class="text-center"
                          :class="venuesSelected.includes(key) ? 'gray-td' : 'white-td'"
                        >
                          <SnowInput 
                            :measure="parseInt(zona.ZERO.numeric_value)"
                            :id-w35-data="zona.ZERO.id_w35_data"
                            :campo="'ZERO'"
                            :zona="key"
                            field="numeric_value"
                            :refresher="refresher"
                            :readonly="readonly"
                            :tab-field-validity="validityObject[selected_time_layout][key]['ZERO']"
                            @setmeasure="saveW35Data"
                          />
                        </td>
                        <td 
                          class="text-center"
                          :class="venuesSelected.includes(key) ? 'gray-td' : 'white-td'"
                        >
                          <SnowInput 
                            :measure="parseInt(zona.SNOW_LEV.numeric_value)"
                            :id-w35-data="zona.SNOW_LEV.id_w35_data"
                            :campo="'SNOW_LEV'"
                            :zona="key"
                            field="numeric_value"
                            :refresher="refresher"
                            :readonly="readonly"
                            :tab-field-validity="validityObject[selected_time_layout][key]['SNOW_LEV']"
                            @setmeasure="saveW35Data"
                          />
                        </td>
                        <td 
                          class="text-center"
                          :class="venuesSelected.includes(key) ? 'gray-td' : 'white-td'"
                        >
                          <input 
                            id="flexCheckDefault"
                            v-model="zona.SKY_12.ignore_refresh_forecast_comuni"
                            class="form-check-input"
                            type="checkbox"
                            :disabled="readonly"
                            @change="setCheckbox(zona.SKY_12.id_w35_data, key)"
                          >
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            <div
              class="col-md-5 my-5 pt-5"
              style="z-index: 1022;"
            >
              <div
                class="sticky-top"
              >
                <AreeMeteo 
                  :color-map="true"
                  :readonly="readonly"
                  :values="previsioneAreeMeteo.w35_data[selected_time_layout]"
                  :icons="icons"
                  :venues-selected="venuesSelected"
                  @open-modal="openModal"
                  @update-venue-selected="updateVenueSelected"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
  import AreeMeteo from './AreeMeteo.vue' 
  import SnowInput from './SnowInput.vue'
  import IconModal from './IconModal.vue' 
  export default {
    name: 'PrevisioneAreeMeteoBulletin',
    components: {
      AreeMeteo,
      SnowInput,
      IconModal
    }
  }
</script>

<script setup lang="ts">
import { Ref, ref, onMounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vue-toast-notification'

import { Modal } from 'bootstrap'

import api from '../../src/api'
import store from '../../src/store'

import { components } from '../../src/types/weboll'
import type { Icons, TabsDate } from "../types"

const router = useRouter()
const route = useRoute()

type W35Full = components['schemas']['W35'] & { w35data_set: components['schemas']['W35Data'][] }

const toast = useToast()
const countfetch = ref(0)
const ready = ref(false)
const previsioneAreeMeteo: Ref<W35Full> = ref({})
const AreeMeteoNames = ref({})
const previsioneAreeMeteo_id = ref("")
const state = ref(store.state)
const actions = ref({
  sending: false,
  reopening: false,
})
const readonly = ref(false)
let icons : Ref<Icons> = ref([])
const selected_time_layout = ref("48")
const icon_blacklist = [10, 12, 1, 26]
let refresher = ref(0)
let modalElement = ref({})
let venuesSelected : Ref<Array<string>> = ref([])
let tabsDate : Ref<TabsDate> = ref({
  48: '',
  64: '',
  65: '',
  81: '',
  82: '',
  98: '',
  99: ''
})
const placeholder = ref({
  freezing_level: null,
  snow_level: null,
  id_sky_condition: null,
  ignore_refresh_forecast_comuni: false,
})

const props = defineProps({
  id: {
      type: String,
      default: () => ''
  },
})

const today = computed(() => {
  let d = new Date()
  return d.toISOString().substring(0, 10)
})

watch(() => countfetch.value, (new_value) => {
  if(new_value > 2){
    ready.value = true
  }
})

watch(() => selected_time_layout.value, (new_value) => {
  // reset placeholder when change tab
  placeholder.value = {
    freezing_level: null,
    snow_level: null,
    id_sky_condition: null,
    ignore_refresh_forecast_comuni: false,
  }
})

onMounted(async () => {
    previsioneAreeMeteo_id.value = props.id
    fetchData()
    modalElement.value = new Modal(document.getElementById('iconModal'))
})

function getDateFormatted(rawString, time = true): String {
  return api.getDateFormatted(rawString, time)
}

function forceUpdate(){
  refresher.value += 1
}

function openModal(){
  modalElement.value.show()
}

function closeModal(){
  modalElement.value.hide()
}

function updateVenueSelected(venues){
  // console.log("updateVenueSelected", venues)
  venuesSelected.value = venues
}

async function fetchData () {
  fetchprevisioneAreeMeteo(previsioneAreeMeteo_id.value).then(response => {
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
    
    previsioneAreeMeteo.value = data
    readonly.value = previsioneAreeMeteo.value.status === "1"
    // codice per riarranggiare meteo dati
    let rearrangePrevisioneAreeMeteo = rearrange(
        previsioneAreeMeteo.value.w35data_set,
        "id_time_layouts",
        bulletin=>rearrange(bulletin, "id_area_meteo", 
        bulletin2=>rearrange(bulletin2, "id_parametro", (arr: any[]) => arr[0] ))
      )
    // Assegnazione del riarrangiamento
    previsioneAreeMeteo.value['w35_data']= rearrangePrevisioneAreeMeteo
    createTabsDate()
    countfetch.value += 1
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
    countfetch.value += 1
  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })

  fetchAreeMeteo().then(response => {
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
      AreeMeteoNames.value[element.id_area_meteo] = element.descrizione
    }
    countfetch.value += 1
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

function remove() {
  if (
    confirm('Vuoi davvero cancellare questo bollettino?')
  ) {
    if(typeof store.state.access === 'string'){
      api.fetchBulletinDelete(previsioneAreeMeteo_id.value, 'w35/bulletins', store).then(response => {
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

function createTabsDate(){
  let today = dateToString(new Date(previsioneAreeMeteo.value.data_emissione))
  let tomorrow = dateToString(new Date(new Date(previsioneAreeMeteo.value.data_emissione).setDate(new Date(previsioneAreeMeteo.value.data_emissione).getDate()+1)))
  let afterTomorrow = dateToString(new Date(new Date(previsioneAreeMeteo.value.data_emissione).setDate(new Date(previsioneAreeMeteo.value.data_emissione).getDate()+2)))
  let aAfterTomorrow = dateToString(new Date(new Date(previsioneAreeMeteo.value.data_emissione).setDate(new Date(previsioneAreeMeteo.value.data_emissione).getDate()+3)))
  tabsDate.value = {
    48: `${today} 12-24`,
    64: `${tomorrow} 00-12`,
    65: `${tomorrow} 12-24`,
    81: `${afterTomorrow} 00-12`,
    82: `${afterTomorrow} 12-24`,
    98: `${aAfterTomorrow} 00-12`,
    99: `${aAfterTomorrow} 12-24`,
  }
}

function dateToString(date): String{
  const yy = date.getFullYear()
  const mm = date.getMonth() + 1
  const dd = date.getDate()
  return [yy, (mm>9 ? '' : '0') + mm, (dd>9 ? '' : '0') + dd].join('-')
}

function execute(action, reroute, message) {
  actions.value[action + 'ing'] = true
  let check = true

  fetchPrevisioneAction(action).then(response => {
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
      router.push({ path: `/w35/${data.id_w35}`})
      previsioneAreeMeteo_id.value = data.id_w35
      fetchData()
    } else {
      if (action == 'send'){
        router.push({ path: `/w35/tasks`})
      }else{
        fetchData()
      }
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
  
}

function setMeasure(id_w35_data, campo, zona){
  let w35data = previsioneAreeMeteo.value.w35_data[selected_time_layout.value][zona][campo]
  let stack : Array<Object> = []
  let value = (window.event.target as HTMLInputElement).value

  w35data.numeric_value = value
  const payload = {"id_key":"id_w35_data","id":id_w35_data,"value_key":"numeric_value","new_value": value}
  const payloadusername = {"id_key":"id_w35","id":previsioneAreeMeteo.value.id_w35,"value_key":"username","new_value": store.state.username}

  stack.push(payload)
  stack.push(payloadusername)
  saveW35(stack)
}

function saveW35Data(id_w35_data, campo, zona, field, value){
  // console.log("saveW35Data", id_w35_data, campo, zona, field, value)
  let w35data = previsioneAreeMeteo.value.w35_data[selected_time_layout.value][zona][campo]
  let stack : Array<Object> = []
  if (isNaN(value)){
    toast.open(
      {
        message: 'Devi inserire un valore!',
        type: 'error',
        position: 'top-left'
      }
    )
  }else if ( (campo == 'SNOW_LEV' || campo == 'ZERO') && (value < 0 || value > 6000) ){
    toast.open(
      {
        message: 'Lo zero termico o la quota neve non possono essere < 0 o > 6000!',
        type: 'error',
        position: 'top-left'
      }
    )
  }
  w35data[field] = value
  const payload = {"id_key":"id_w35_data","id":id_w35_data,"value_key":field,"new_value": value}
  const payloadusername = {"id_key":"id_w35","id":previsioneAreeMeteo.value.id_w35,"value_key":"username","new_value": store.state.username}
  
  stack.push(payload)
  stack.push(payloadusername)
  forceUpdate()
  saveW35(stack)
}

function setIcons(id_sky_condition){
  // console.log("Bulletin setIcons", id_sky_condition, venuesSelected.value)
  let stack : Array<Object> = []
  venuesSelected.value.forEach(venue => {
    let w35data = previsioneAreeMeteo.value.w35_data[selected_time_layout.value][venue].SKY_12
    const payload = {"id_key":"id_w35_data","id":w35data.id_w35_data,"value_key":"numeric_value","new_value": id_sky_condition}

    w35data.numeric_value = id_sky_condition
    stack.push(payload)    
  })
  venuesSelected.value = []
  // console.log("Bulletin setIcons reset venues", venuesSelected.value)
  closeModal()
  const payloadusername = {"id_key":"id_w35","id":previsioneAreeMeteo.value.id_w35,"value_key":"username","new_value": store.state.username}
  stack.push(payloadusername)

  saveW35(stack)
}

function saveW35(stack) {
  bulkUpdateW35(stack).then((response) => {
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
    previsioneAreeMeteo.value.last_update = data.bulletin.last_update
    previsioneAreeMeteo.value.username = store.state.username || ""
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

async function fetchPrevisioneAction (action) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w35/bulletins/${previsioneAreeMeteo_id.value}/${action}/`
  )
  return response
}


async function fetchprevisioneAreeMeteo (id) {
  const response = await fetch('/api/w35/bulletins/' + id + '/', {
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

async function fetchAreeMeteo () {
  const response = await fetch('/api/w35/aree_meteo/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

function rearrange(data: any[], key: string, func: ArrayTransformer | null = null) {
//function rearrange(data: any[], key: string, func=null) {
  // rearranges the array data in a dictionary
  // aggregating all records with the same key as an array
  // optionally transforming each array with the func function
  let value_data = {}
  data.forEach((record: { [x: string]: string | number }) => {
    if (!(record[key] in value_data)) {
      value_data[record[key]] = []
    }
    // console.log('rearrange record', record)
    value_data[record[key]].push(record)
  })
  if (func) {
    Object.keys(value_data).forEach(key => value_data[key] = func(value_data[key]))
  }
  if (!Object.values(value_data).some(item => item != undefined)) value_data = {}
  return value_data
}

async function bulkUpdateW35(payload) {
  if(store.state.access !== null){
    const response = await api.fetch_wrapper(
      store.state.access,
      `/api/w35/bulletins/bulk_update/`,
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

function selectAll(campo:String, field:String){
  if(window.event && window.event.target !== null){
    let new_value:number|null = parseInt((window.event.target as HTMLInputElement).value)
    new_value = Number.isNaN(new_value) ? null : new_value
    saveAll(campo, field, new_value)
  }
}

function checkAll(){
  if(window.event && window.event.target !== null){
    let new_value = (window.event.target as HTMLInputElement).checked
    let venues = previsioneAreeMeteo.value.w35_data[selected_time_layout.value]
  
    let stack : Array<Object> = []

    Object.keys(venues).forEach(d => {
      let w35data = previsioneAreeMeteo.value.w35_data[selected_time_layout.value][d]['SKY_12']
      // console.log(w35data, new_value)
      const payload = {"id_key":"id_w35_data","id":w35data.id_w35_data,"value_key":"ignore_refresh_forecast_comuni","new_value": new_value}
      w35data.ignore_refresh_forecast_comuni = new_value
      stack.push(payload)
    })
    
    const payloadusername = {"id_key":"id_w35","id":previsioneAreeMeteo.value.id_w35,"value_key":"username","new_value": store.state.username}
    stack.push(payloadusername)
    saveW35(stack)
  }
}

function saveAll(campo:String, field:String, new_value:number){
  // funzione per il salvataggio su tutte le venue
  if ( (campo == 'SNOW_LEV' || campo == 'ZERO') && (new_value < 0 || new_value > 6000) ){
    toast.open(
      {
        message: 'Lo zero termico o la quota neve non possono essere < 0 o > 6000',
        type: 'error',
        position: 'top-left'
      }
    )
  }
  let venues = previsioneAreeMeteo.value.w35_data[selected_time_layout.value]
  
  let stack : Array<Object> = []

  Object.keys(venues).forEach(d => {
    let w35data = previsioneAreeMeteo.value.w35_data[selected_time_layout.value][d]
    const payload = {"id_key":"id_w35_data","id":w35data[campo].id_w35_data,"value_key":field,"new_value": new_value}
    w35data[campo][field] = new_value
    stack.push(payload)
  })
  
  const payloadusername = {"id_key":"id_w35","id":previsioneAreeMeteo.value.id_w35,"value_key":"username","new_value": store.state.username}
  stack.push(payloadusername)
  saveW35(stack)
}

function setCheckbox(id_w35_data, zona){
  // console.log("setCheckbox", id_w35_data, zona)
  if(window.event && window.event.target !== null){
    let new_value = (window.event.target as HTMLInputElement).checked
    let w35data = previsioneAreeMeteo.value.w35_data[selected_time_layout.value][zona]['SKY_12']
    let stack : Array<Object> = []
    w35data.ignore_refresh_forecast_comuni = new_value
    const payload = {"id_key":"id_w35_data","id":id_w35_data,"value_key":"ignore_refresh_forecast_comuni","new_value": new_value}
    const payloadusername = {"id_key":"id_w35","id":previsioneAreeMeteo.value.id_w35,"value_key":"username","new_value": store.state.username}
    
    stack.push(payload)
    stack.push(payloadusername)
    forceUpdate()
    saveW35(stack)
  }
}

/*
validity object:

{
  "48": {
    "MET-1": {
      "SKY_12": true,
      "SNOW_LEV": false,
      "ZERO": false
    },
    "MET-2": {
      "SKY_12": true,
      "SNOW_LEV": false,
      "ZERO": false
    },
    ...
    "tab": true
  }
  "64": {
    "MET-1": {
      "SKY_12": false,
      "SNOW_LEV": false,
      "ZERO": false
    },
    "MET-2": {
      "SKY_12": false,
      "SNOW_LEV": false,
      "ZERO": false
    },
    ...
    "tab": true
  },
  ...
  "bollettino_ok": true
}
*/

const validityObject = computed(() => {
  let validity = {"bollettino_ok": true}
  // validity={'48': {'MET-1': {'SKY-12':true}}}
  for (const [tl, value] of Object.entries(previsioneAreeMeteo.value.w35_data)) {
    validity[tl] = {}
    validity[tl]["tab"] = true
    for (const [id_area_meteo, value2] of Object.entries(previsioneAreeMeteo.value.w35_data[tl])) {
      validity[tl][id_area_meteo] = {}
      let snow_lev = -1
      let zero =  -1
      for (const [id_parametro, value3] of Object.entries(previsioneAreeMeteo.value.w35_data[tl][id_area_meteo])) {
        // console.log(tl, id_area_meteo, id_parametro, value3['numeric_value'])
        validity[tl][id_area_meteo][id_parametro] = true
        if (value3['numeric_value'] == null){
          validity[tl][id_area_meteo][id_parametro] = false
          validity[tl]["tab"] = false
          validity["bollettino_ok"] = false
        }
        if (isNaN(value3['numeric_value'])){
          validity[tl][id_area_meteo][id_parametro] = false
          validity[tl]["tab"] = false
          validity["bollettino_ok"] = false
        }
        if (id_parametro == 'SKY_12' && value3['numeric_value'] == 12){
          validity[tl][id_area_meteo][id_parametro] = false
          validity[tl]["tab"] = false
          validity["bollettino_ok"] = false
        }
        if ( (id_parametro == 'ZERO' || id_parametro == 'SNOW_LEV') && 
          (value3['numeric_value'] < 0 || value3['numeric_value'] > 6000) ){
          validity[tl][id_area_meteo][id_parametro] = false
          validity[tl]["tab"] = false
          validity["bollettino_ok"] = false
        }
        if ( id_parametro == 'ZERO' && zero == -1) zero = parseInt(value3['numeric_value'])
        if ( id_parametro == 'SNOW_LEV' && snow_lev == -1) snow_lev = parseInt(value3['numeric_value'])
        // console.log("testo tutti e 2 maggiori di zero", zero, snow_lev)
        if (zero >= 0 && snow_lev >= 0){
          // console.log("sono tutti e 2 maggiori di zero", zero, snow_lev)
          if (snow_lev > zero){
            // console.log("attenzione snow_lev > di zero", zero, snow_lev)
            validity[tl][id_area_meteo]['SNOW_LEV'] = false
            validity[tl]["tab"] = false
            validity["bollettino_ok"] = false
          }
        }
      }
    }
  }
  return validity
})

</script>
<style>
  .gray-td {
    background-color: gray  !important;
  }
  .white-td {
    background-color:  white  !important;
  }
</style>