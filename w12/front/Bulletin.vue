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
        <a
          class="btn btn-outline-primary"
          :href="'/api/w12/pdf/' + autostrada.id_w12"
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
          v-if="autostrada.status === '0' && state.username && autostrada.start_valid_time.substring(0, 10) === today"
          :disabled="actions.sending || sendable"
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
          v-if="autostrada.status === '1' && state.username && autostrada.start_valid_time.substring(0, 10) === today"
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
      </div>
    </div>

    <div class="row mb-3">
      <h1>Bollettino A7-A26 {{ autostrada.id_w12 }}</h1>
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
        <label for="start_valid_time">Data emissione
          <input
            id="start_valid_time"
            disabled
            class="form-control"
            name="start_valid_time"
            type="text"
            :value="getDateFormatted(autostrada.start_valid_time, false)"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_validita">Data scadenza
          <input
            id="data_validita"
            disabled
            class="form-control"
            name="data_validita"
            type="text"
            :value="getDateFormatted(autostrada.next_blt_time, false)"
          >
          <!--<Datepicker
            v-model="autostrada.data_validita"
            :disabled="readonly"
            :style="readonly ? '--dp-disabled-color: #e9ecef' : '--dp-background-color: white'"
            format="dd/MM/yyyy"
            auto-apply
            @update:model-value="saveW12(autostrada.data_validita, autostrada.id_w12, 'data_validita')"
          />-->
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
      <div class="col-md-1 mb-3">
        <button
          type="button"
          class="btn btn-outline-primary btn-sm"
          @click="openTab('/images/autostrade/tab-neve-w12.png')"
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
                v-for="(value, key) in autostrada.w12_data"
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
            class="col-md-8 mb-3"
            style="z-index: 1023;"
          >
            <div class="row">
              <div class="col-md-12 mb-3">
                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th
                        class="text-center"
                        style="width: 10em;"
                        scope="col"
                      >
                        Tratto Autostradale
                      </th>
                      <th
                        class="text-center"
                        style="width: 8em;"
                      >
                        Tempo Prevalente
                      </th>
                      <th
                        class="text-center"
                        style="width: 5em;"
                      >
                        Cop. Nuv.
                      </th>
                      <th
                        class="text-center"
                        style="width: 8em;"
                      >
                        Precip.
                      </th>
                      <th
                        class="text-center"
                        style="width: 4em;"
                      >
                        Neve (cm)
                      </th>
                      <th 
                        class="text-center"
                        style="width: 5em;"
                      >
                        Zero Termico
                      </th>
                      <th 
                        class="text-center"
                        style="width: 5em;"
                      >
                        Quota Neve
                      </th>
                      <th
                        class="text-center"
                        style="width: 4em;"
                      >
                        Temp. Sotto zero
                      </th>
                      <th
                        class="text-center"
                        style="width: 4em;"
                      >
                        Rischio pioggia ghiacc.
                      </th>
                      <th
                        class="text-center"
                        style="width: 3em;"
                      >
                        Visibilità inf. 1000m
                      </th>
                      <th
                        class="text-center"
                        style="width: 8em;"
                      >
                        Venti
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
                          :value="placeholder.sky_condition"
                          :disabled="readonly"
                          class="form-select col"
                          @change="selectAll('sky_condition')"
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
                          :value="placeholder.cloud_amount"
                          class="form-select col"
                          :disabled="readonly"
                          @change="selectAll('cloud_amount')"
                        >
                          <option value="0">
                            0/8
                          </option>
                          <option value="1">
                            1/8
                          </option>
                          <option value="2">
                            2/8
                          </option>
                          <option value="3">
                            3/8
                          </option>
                          <option value="4">
                            4/8
                          </option>
                          <option value="5">
                            5/8
                          </option>
                          <option value="6">
                            6/8
                          </option>
                          <option value="7">
                            7/8
                          </option>
                          <option value="8">
                            8/8
                          </option>
                        </select>
                      </td>
                      <td class="text-center">
                        <ClassSelect 
                          :data="placeholder"
                          :classes-value="configA26.precipitation"
                          :validity="false"
                          :campo="'precipitation_class'"
                          :readonly="readonly"
                          @set-class="setClassAll"
                        />
                      </td>
                      <td class="text-center">
                        <input
                          type="Number"
                          :value="placeholder.cumulated_snow"
                          class="form-control"
                          title="Neve cumulata"
                          :disabled="readonly"
                          @change="selectAll('cumulated_snow')"
                        >
                      </td>
                      <td class="text-center">
                        <SnowInput 
                          :measure="placeholder.freezing_level"
                          :id-w12-data="0"
                          :campo="'freezing_level'"
                          :refresher="refresher"
                          :readonly="readonly"
                          @setmeasure="setClassAll"
                        />
                      </td>
                      <td class="text-center">
                        <SnowInput 
                          :measure="placeholder.snow_level"
                          :id-w12-data="0"
                          :campo="'snow_level'"
                          :refresher="refresher"
                          :readonly="readonly"
                          @setmeasure="setClassAll"
                        />
                      </td>
                      <td class="text-center">
                        <input 
                          id="flexCheckDefault"
                          v-model="placeholder.temperature_below_zero"
                          class="form-check-input"
                          type="checkbox"
                          :disabled="readonly"
                          @change="checkAll('temperature_below_zero')"
                        >
                      </td>
                      <td class="text-center">
                        <input 
                          id="flexCheckDefault"
                          v-model="placeholder.risk_freezing_rain"
                          class="form-check-input"
                          type="checkbox"
                          :disabled="readonly"
                          @change="checkAll('risk_freezing_rain')"
                        >
                      </td>
                      <td class="text-center">
                        <input 
                          id="flexCheckDefault"
                          v-model="placeholder.vis_inf_1000"
                          class="form-check-input"
                          type="checkbox"
                          :disabled="readonly"
                          @change="checkAll('vis_inf_1000')"
                        >
                        <ClassSelect 
                          :data="placeholder"
                          :classes-value="configA26.visInf1000"
                          :validity="false"
                          :campo="'vis_inf_1000_reason'"
                          :readonly="readonly"
                          @set-class="setClassAll"
                        />
                      </td>
                      <td class="text-center">
                        <ClassSelect 
                          :data="placeholder"
                          :classes-value="configA26.wind"
                          :validity="false"
                          :campo="'wind_class'"
                          :readonly="readonly"
                          @set-class="setClassAll"
                        />
                      </td>
                    </tr>
                    <tr
                      v-for="tratto in autostrada.w12_data[selected_time_layout]"
                      :key="tratto.id_w12"
                    >
                      <td
                        class="text-center"
                      >
                        {{ venueNames[tratto.id_venue] }} ({{ heights[tratto.id_venue].min }}-{{ heights[tratto.id_venue].max }} m)
                      </td>
                      <td class="text-center">
                        <select
                          :value="tratto.sky_condition"
                          :disabled="readonly"
                          :style="skycond_validity[selected_time_layout][tratto.id_venue] ? 'border: 3px solid #FFA500' : ''"
                          class="form-select col"
                          @change="setMeasure(tratto.id_w12_data, 'sky_condition')"
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
                          :value="tratto.cloud_amount"
                          class="form-select col"
                          :style="coptotValidity[selected_time_layout][tratto.id_venue] ? 'border: #FF5C5C; border:3px solid #FF5C5C;' : ''"
                          :disabled="readonly"
                          @change="setMeasure(tratto.id_w12_data, 'cloud_amount')"
                        >
                          <option value="0">
                            0/8
                          </option>
                          <option value="1">
                            1/8
                          </option>
                          <option value="2">
                            2/8
                          </option>
                          <option value="3">
                            3/8
                          </option>
                          <option value="4">
                            4/8
                          </option>
                          <option value="5">
                            5/8
                          </option>
                          <option value="6">
                            6/8
                          </option>
                          <option value="7">
                            7/8
                          </option>
                          <option value="8">
                            8/8
                          </option>
                        </select>
                      </td>
                      <td class="text-center">
                        <ClassSelect 
                          :data="tratto"
                          :classes-value="configA26.precipitation"
                          :validity="pluvValidity[selected_time_layout][tratto.id_venue]"
                          :campo="'precipitation_class'"
                          :readonly="readonly"
                          @set-class="saveW12Data"
                        />
                      </td>
                      <td class="text-center">
                        <input
                          v-model="tratto.cumulated_snow"
                          type="Number"
                          class="form-control"
                          title="Neve cumulata"
                          :style="cumulatedSnowValidity[selected_time_layout][tratto.id_venue] == 1 ? 'border: #FFA500; border:3px solid #FFA500;' : (
                            cumulatedSnowValidity[selected_time_layout][tratto.id_venue] == 2 ? 'border: #FF5C5C; border:3px solid #FF5C5C;' : '')"
                          :disabled="readonly"
                          @change="setMeasure(tratto.id_w12_data, 'cumulated_snow')"
                        >
                      </td>
                      <td class="text-center">
                        <SnowInput 
                          :measure="tratto.freezing_level"
                          :id-w12-data="tratto.id_w12_data"
                          :campo="'freezing_level'"
                          :refresher="refresher"
                          :readonly="readonly"
                          @setmeasure="saveW12Data"
                        />
                      </td>
                      <td class="text-center">
                        <SnowInput 
                          :measure="tratto.snow_level"
                          :id-w12-data="tratto.id_w12_data"
                          :style="snowLevValidity[selected_time_layout][tratto.id_venue] ? 'border: #FFA500; border:3px solid #FFA500;' : ''"
                          :campo="'snow_level'"
                          :refresher="refresher"
                          :readonly="readonly"
                          @setmeasure="saveW12Data"
                        />
                      </td>
                      <td class="text-center">
                        <input 
                          id="flexCheckDefault"
                          v-model="tratto.temperature_below_zero"
                          class="form-check-input"
                          type="checkbox"
                          :disabled="readonly"
                          @change="setCheckbox(tratto.id_w12_data, 'temperature_below_zero')"
                        >
                      </td>
                      <td class="text-center">
                        <input 
                          id="flexCheckDefault"
                          v-model="tratto.risk_freezing_rain"
                          class="form-check-input"
                          type="checkbox"
                          :disabled="readonly"
                          @change="setCheckbox(tratto.id_w12_data, 'risk_freezing_rain')"
                        >
                      </td>
                      <td class="text-center">
                        <input 
                          id="flexCheckDefault"
                          v-model="tratto.vis_inf_1000"
                          class="form-check-input"
                          type="checkbox"
                          :disabled="readonly"
                          @change="setCheckbox(tratto.id_w12_data, 'vis_inf_1000')"
                        >
                        <ClassSelect 
                          :data="tratto"
                          :classes-value="configA26.visInf1000"
                          :validity="false"
                          :campo="'vis_inf_1000_reason'"
                          :readonly="readonly || !tratto.vis_inf_1000"
                          @set-class="saveW12Data"
                        />
                      </td>
                      <td class="text-center">
                        <ClassSelect 
                          :data="tratto"
                          :classes-value="configA26.wind"
                          :validity="false"
                          :campo="'wind_class'"
                          :readonly="readonly"
                          @set-class="saveW12Data"
                        />
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div
            class="col-md-4 mb-3"
          > 
            <div>
              <IconeMap
                :datatab="autostrada.w12_data[selected_time_layout]"
                :icons="icons"
                :venues-selected="venuesSelected"
                :show-autostrade="{
                  a26: true,
                  a6: false,
                  a4: false,
                  a21: false,
                  a33: false,
                }"
                :campo-icon="'sky_condition'"
                :readonly="readonly"
                @open-modal="openModal"
                @update-venue-selected="updateVenueSelected"
              />
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
import ClassSelect from './ClassSelect.vue'
import SnowInput from './SnowInput.vue'
import IconeMap from '../../w33/front/IconeMap.vue'
import AutostradeMap from '../../w33/front/AutostradeMap.vue'
import IconModal from '../../w33/front/IconModal.vue'

  export default {
    name: 'AutostradaA7A26Bulletin',
    components: {
      ClassSelect,
      IconeMap,
      AutostradeMap,
      SnowInput,
      IconModal
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
import type { W12Processed, Icons } from "../types"
import { configA26 } from "../config";
type W12Data = components['schemas']['W12Data']

const router = useRouter()
const route = useRoute()
const toast = useToast()

//reactive properties
let autostrada_id = ref("")
let autostrada : Ref<W12Processed> = ref({
    id_w12: 0,
    start_valid_time: '',
    validity: 0,
    next_blt_time: '',
    status: '',
    last_update: '',
    username: '',
    w12_data: {
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
let venuesSelected : Ref<Array<string>> = ref([])
let selected_time_layout = ref(45)
let tabsDate = ref({
  45: '',
  46: '',
  60: '',
  61: '',
  62: '',
  63: '',
  81: '',
  82: ''
})
let state = ref(store.state)
let colorMap = ref(true)
let ready = ref(false)
let readonly = ref(true)
let actions = ref({
  sending: false,
  reopening: false,
})
let refresher = ref(0)
let venueNames = ref({})
let icons : Ref<Icons> = ref([])
let countdown = ref(0)
let modalElement = ref({})

const icon_blacklist = [ 10, 1, 32, 44, 45, 46 ]
const placeholder = ref({
  id_w12_data: 0,
  cloud_amount: null,
  precipitation_class: null,
  cumulated_snow: null,
  freezing_level: null,
  snow_level: null,
  temperature_below_zero: false,
  risk_freezing_rain: false,
  vis_inf_1000: false,
  vis_inf_1000_reason: null,
  wind_class: null,
  id_w12: 0,
  id_venue: 0,
  id_time_layouts: 0,
  id_sky_condition: 0,
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
})

const venueOrder = [
  105, 
  104, 
  103, 
  102, 
  101, 
  100, 
  99,
]

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
  class5: {
    icons: [ 18 ],
    min6: -1,
    max6: 25,
    min12: -1,
    max12: 30,
    isNull: false
  },
  classAll: {
    icons: [ 31, 44 ],
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

const skycond_coptot_validity = {
  "1": [5,6,7,8],
  "2": [7,8],
  "3": [0],
  "4": [1,2,3,4,5,6,7,8],
  "5": [1,2,3,4,5,6,7,8],
  "6": [5,6,7,8],
  "7": [5,6,7,8],
  "8": [5,6,7,8],
  "9": [5,6,7,8],
  "12": [],
  "11": [5,6],
  "16": [3,4],
  "17": [5,6,7,8],
  "18": [5,6,7,8],
  "20": [3,4,5,6,7,8],
  "21": [5,6,7,8],
  "22": [1,2],
  "23": [3,4,5,6,7,8],
  "24": [3,4,5,6,7,8],
  "25": [5,6,7,8],
  "26": [5,6,7,8],
  "27": [5,6,7,8],
  "28": [5,6,7,8],
  "29": [0,1,2,3,4,5,6,7,8],
  "30": [3,4,5,6,7,8],
  "31": [3,4,5,6,7,8]
}

const skycond_to_coptot = {
  "1": 8,
  "2": 7,
  "3": 0,
  "4": 3,
  "5": 3,
  "6": 8,
  "7": 8,
  "8": 8,
  "9": 8,
  "11": 5,
  "16": 3,
  "17": 8,
  "18": 8,
  "20": 5,
  "21": 8,
  "22": 1,
  "23": 8,
  "24": 6,
  "25": 8,
  "26": 8,
  "27": 8,
  "28": 8,
  "29": 1,
  "30": 8,
  "31": 8
}

// i valori devono corrispondere al dizionario skycond_to_pluv_A26 del file config/skycond_firstguess.json
const skycond_to_pluv = {
  "1": 0,
  "2": 0,
  "3": 0,
  "4": 0,
  "5": 0,
  "6": 4,
  "7": 4,
  "8": 2,
  "9": 2,
  "11": 0,
  "16": 0,
  "17": 3,
  "18": 2,
  "20": 2,
  "21": 3,
  "22": 0,
  "23": 3,
  "24": 2,
  "25": 5,
  "26": 5,
  "27": 1,
  "28": 1,
  "29": 0,
  "30": 2,
  "31": 2
}
// per ogni sky condition si definiscono le classi di intensità di precipitazione permesse 
const pluv_classlist = {
  // pioggia debole - neve debole
  class1: {
    icons: [ 8, 9 ],
    pluv_class: [ 1, 2],
  },
  // pioggia moderata - neve moderata
  class2: {
    icons: [ 17, 21 ],
    pluv_class: [ 3 ],
  },
  // pioggia forte - neve forte
  class3: {
    icons: [ 6, 7 ],
    pluv_class: [ 4 ],
  },
  // pioggia molto forte - neve molto forte
  class4: {
    icons: [ 25, 26 ],
    pluv_class: [ 5 ],
  },
  // pioggia e neve
  class5: {
    icons: [ 18 ],
    pluv_class: [ 1, 2, 3, 4 ],
  },
  // rovesci, temporali, instabile, vento e pioggia, vento e neve
  classAll: {
    icons: [ 20, 23, 24, 30, 31 ],
    pluv_class: [ 1, 2, 3, 4, 5],
  },
  // icone senza precipitazioni
  classNo: {
    icons: [ 2, 3, 4, 5, 11, 12, 16, 22, 29 ],
    pluv_class: [ 0 ],
  },
}

watch(() => countdown.value, (new_value) => {
  if(new_value > 2){
    createTabsDate()
    ready.value = true
  }
})

const today = computed(() => {
  let d = new Date()
  return d.toISOString().substring(0, 10)
})


const snowLevValidity = computed(() => {
  // warning se la quota neve è superiore al tratto autostradale + 100 m
  let validity = {}
  for(const tl in autostrada.value.w12_data){
    validity[tl] = {}
    autostrada.value.w12_data[tl].forEach(e => {
      validity[tl][e.id_venue] = 0
      for(const classe in snow_classlist){
        if(snow_classlist[classe].icons.includes(e.sky_condition) && classe !== "classNo" ){
          if((e.cumulated_snow !== null || e.cumulated_snow !== 0) && (e.snow_level === null || e.snow_level > heights.value[e.id_venue].max + 100)){
            validity[tl][e.id_venue] = 1
          }else{
            validity[tl][e.id_venue] = 0
          }
        }
      }
    })
  }
  return validity
})

watch(() => selected_time_layout.value, (new_value) => {
  placeholder.value = {
    id_w12_data: 0,
    cloud_amount: null,
    precipitation_class: null,
    cumulated_snow: null,
    freezing_level: null,
    snow_level: null,
    temperature_below_zero: false,
    vis_inf_1000: null,
    vis_inf_1000_reason: null,
    air_temperature: 0,
    wind_class: null,
    id_w12: 0,
    id_venue: 0,
    id_time_layouts: 0,
    sky_condition: 0,
  }
})


const cumulatedSnowValidity = computed(() => {
  // 0 ok, 1 warining, 2 Errore: warning se i cm non corrispondono alla classe, errore se cumulated_snow is null
  let validity = {}
  for(const tl in autostrada.value.w12_data){
    validity[tl] = {}
    autostrada.value.w12_data[tl].forEach(e => {
      validity[tl][e.id_venue] = 0
      for(const classe in snow_classlist){
        if([ 45, 46, 60, 61, 62, 63].includes(parseInt(tl))){
          if(snow_classlist[classe].icons.includes(e.sky_condition)){
            if(snow_classlist[classe].isNull && e.cumulated_snow === null){
              validity[tl][e.id_venue] = 0
            // caso icona di neve ma valore a null, è un errore bloccante
            }else if (e.cumulated_snow === null || e.cumulated_snow ===""){
              validity[tl][e.id_venue] = 2
            }else if(snow_classlist[classe].min6 < e.cumulated_snow && snow_classlist[classe].max6 >= e.cumulated_snow && e.cumulated_snow !== null){
              validity[tl][e.id_venue] = 0
            }else{
              validity[tl][e.id_venue] = 1
            }
          }
        }else if ([81, 82].includes(parseInt(tl))){
          if(snow_classlist[classe].icons.includes(e.sky_condition)){
            if(snow_classlist[classe].isNull && e.cumulated_snow === null){
              validity[tl][e.id_venue] = 0
            // caso icona di neve ma valore a null, è un errore bloccante
            }else if (e.cumulated_snow === null || e.cumulated_snow ===""){
              validity[tl][e.id_venue] = 2
            }else if(snow_classlist[classe].min12 < e.cumulated_snow && snow_classlist[classe].max12 > e.cumulated_snow){
              validity[tl][e.id_venue] = 0
            }else{
              validity[tl][e.id_venue] = 1
            }
          }
        }
        // solo per A26 sia in 6h sia in 12h la neve accumulata di 0 o 1 cm dev'essere associata alla classe di precipitazione "molto debole"
        if(snow_classlist[classe].icons.includes(e.sky_condition) && classe !== "classNo" ){
          if (e.precipitation_class === 1) {
            if (e.cumulated_snow === 0 || e.cumulated_snow === 1 ){
              validity[tl][e.id_venue] = 0
            }else if (e.cumulated_snow === null || e.cumulated_snow ===""){
              validity[tl][e.id_venue] = 2
            }else{
             validity[tl][e.id_venue] = 1
            }
          // nel caso di classe debole rimane il controllo sullo sky_cond ma segnalo warning per cumulate di 0 e 1 cm
          } else if (e.precipitation_class === 2) {
            if (e.cumulated_snow === 0 || e.cumulated_snow === 1 ){
              validity[tl][e.id_venue] = 1
            }
          }
        }
      }
    })
  }
  return validity
})



const pluvValidity = computed(() => {
  let validity = {}
  for(const tl in autostrada.value.w12_data){
    validity[tl] = {}
    autostrada.value.w12_data[tl].forEach(e => {
      validity[tl][e.id_venue] = false
      for(const classe in pluv_classlist){
        if(pluv_classlist[classe].icons.includes(e.sky_condition)){
          if(pluv_classlist[classe].pluv_class.includes(e.precipitation_class)){
            validity[tl][e.id_venue] = false
          }else{
            validity[tl][e.id_venue] = true
          }
        }
      }
    })
  }
  console.log(validity)
  return validity
})

const coptotValidity = computed(() => {
  let validity = {}
  for(const tl in autostrada.value.w12_data){
    validity[tl] = {}
    autostrada.value.w12_data[tl].forEach(e => {
      validity[tl][e.id_venue] = false
      if(!skycond_coptot_validity[e.sky_condition].includes(e.cloud_amount)){
        validity[tl][e.id_venue] = true
      }
    })
  }
  return validity
})

const tab_validity = computed(() => {
  let validity = {}
  for(const tl in pluvValidity.value){
    validity[tl] = false
    for(const venue in pluvValidity.value[tl]){
      if(pluvValidity.value[tl][venue]){
        validity[tl] = true
      }
      if(coptotValidity.value[tl][venue]){
        validity[tl] = true
      }
      if(cumulatedSnowValidity.value[tl][venue] == 2){
        validity[tl] = true
      }
    }
    
  }
  return validity
})

const pluv_skycond = [8, 17, 6, 25]

const skycond_validity = computed(() => {
  let validity = {}
  for(const tl in autostrada.value.w12_data){
    validity[tl] = {}
    autostrada.value.w12_data[tl].forEach(data => {
      if(pluv_skycond.includes(data.sky_condition) && data.snow_level <= heights.value[data.id_venue].max + 100){
        validity[tl][data.id_venue] = true
      }else{
        validity[tl][data.id_venue] = false
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

onMounted(() => {
  autostrada_id.value = props.id
  fetchData()
  let element = document.getElementById('iconModal')
  if(element !== null){
    modalElement.value = new Modal(element)
  }
})

function forceUpdate(){
  refresher.value += 1
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
    if ('w12data_set' in data) {
      data.w12data_set.forEach((element) => {
        tmp[element.id_time_layouts].push(element)
      })
    }

    for(const tl in tmp){
      let tmparray: Array<W12Data> = []
      venueOrder.forEach(e => {
        let tratto = tmp[tl].find(v => v.id_venue === e)
        if(tratto){
          tmparray.push(tratto)
        }
      })
      tmp[tl] = tmparray
    }

    autostrada.value = {
      id_w12: data.id_w12,
      start_valid_time: data.start_valid_time,
      validity: data.validity,
      next_blt_time: data.next_blt_time,
      status: data.status,
      last_update: data.last_update,
      username: data.username,
      w12_data: tmp
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
      router.push({ path: `/w12/${data.id_w12}`})
      autostrada_id.value = data.id_w12
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
    api.fetchBulletinDelete(autostrada_id.value, 'w12/bulletins', store).then(response => {
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

function setCheckbox(id_w12_data, campo){
  if(window.event && window.event.target !== null){
    let new_value = (window.event.target as HTMLInputElement).checked
    saveW12Data(id_w12_data, campo, new_value)
  }
}
function setMeasure(id_w12_data, campo){
  if(window.event && window.event.target !== null){
    let new_value = parseInt((window.event.target as HTMLInputElement).value)
    saveW12Data(id_w12_data, campo, new_value)
  }
}

function saveW12Data(id_w12_data, campo, new_value){
  let w12data = autostrada.value.w12_data[selected_time_layout.value].find(e => e.id_w12_data === id_w12_data)
  let stack : Array<Object> = []

  if(campo === 'sky_condition'){
    if(icon_list.includes(new_value)){
      const payloadAzzeramento = {"id_key":"id_w12_data","id":w12data.id_w12_data,"value_key":"cumulated_snow","new_value": null}
      w12data["cumulated_snow"] = null
      stack.push(payloadAzzeramento)
    } 
    w12data["cloud_amount"] = skycond_to_coptot[new_value]
    const payloadCop = {"id_key":"id_w12_data","id":w12data.id_w12_data,"value_key":"cloud_amount","new_value": skycond_to_coptot[new_value]}
    stack.push(payloadCop)
    for(const classe in pluv_classlist){
      if(pluv_classlist[classe].icons.includes(new_value)){
        let pluv_value = skycond_to_pluv[new_value]
        const payloadPioggia = {"id_key":"id_w12_data","id":w12data.id_w12_data,"value_key":"precipitation_class","new_value": pluv_value }
        w12data["precipitation_class"] = pluv_value
        stack.push(payloadPioggia)
      }
    }
  }

  let value = new_value
  if(isNaN(new_value)){
    value = null
  }

  const payload = {"id_key":"id_w12_data","id":w12data.id_w12_data,"value_key":campo,"new_value": value}
  const payloadusername = {"id_key":"id_w12","id":autostrada.value.id_w12,"value_key":"username","new_value": store.state.username}

  w12data[campo] = value
  stack.push(payload)
  stack.push(payloadusername)


  saveW12(stack)
}

function saveAll(campo, new_value){
  let w12datas = autostrada.value.w12_data[selected_time_layout.value]
  let stack : Array<Object> = []

  w12datas.forEach(d => {
    const payload = {"id_key":"id_w12_data","id":d.id_w12_data,"value_key":campo,"new_value": new_value}
    d[campo] = new_value
    stack.push(payload)
    if(campo === 'sky_condition' && icon_list.includes(new_value)){
      const payloadAzzeramento = {"id_key":"id_w12_data","id":d.id_w12_data,"value_key":"cumulated_snow","new_value": null}
      d["cumulated_snow"] = null
      stack.push(payloadAzzeramento)
      for(const classe in pluv_classlist){
        if(pluv_classlist[classe].icons.includes(new_value)){
          let pluv_value = skycond_to_pluv[new_value]
          const payloadPioggia = {"id_key":"id_w12_data","id":d.id_w12_data,"value_key":"precipitation_class","new_value": pluv_value }
          d["precipitation_class"] = pluv_value
          stack.push(payloadPioggia)
        }
      }
    }
    if(campo === 'sky_condition'){
      d["cloud_amount"] = skycond_to_coptot[new_value]
      const payloadCop = {"id_key":"id_w12_data","id":d.id_w12_data,"value_key":"cloud_amount","new_value": skycond_to_coptot[new_value]}
      stack.push(payloadCop)
    }
})
  
  const payloadusername = {"id_key":"id_w12","id":autostrada.value.id_w12,"value_key":"username","new_value": store.state.username}

  stack.push(payloadusername)
  saveW12(stack)
}

function selectAll(campo){
  if(window.event && window.event.target !== null){
    let new_value:number|null = parseInt((window.event.target as HTMLInputElement).value)
    new_value = Number.isNaN(new_value) ? null : new_value
    saveAll(campo, new_value)
  }
}

function checkAll(campo){
  if(window.event && window.event.target !== null){
    let new_value = (window.event.target as HTMLInputElement).checked
    saveAll(campo, new_value)
  }
}

function setClassAll(da, campo, new_value){
  saveAll(campo, new_value)
}

function openTab (path) {
  window.open(path, "_blank");
}

function saveW12(stack) {
  forceUpdate()
  bulkUpdateW12(stack).then((response) => {
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
  let today = dateToString(new Date(autostrada.value.start_valid_time))
  let tomorrow = dateToString(new Date(new Date(autostrada.value.start_valid_time).setDate(new Date(autostrada.value.start_valid_time).getDate()+1)))
  let afterTomorrow = dateToString(new Date(new Date(autostrada.value.start_valid_time).setDate(new Date(autostrada.value.start_valid_time).getDate()+2)))
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

const icon_list = [ 1, 10, 11, 12, 16, 17, 2, 20, 22, 23, 24, 25, 29, 3, 30, 32, 4, 45, 46, 5, 6, 8 ]

function setIcons(id_sky_condition){  
  let stack : Array<Object> = []
  venuesSelected.value.forEach(venue => {
    let w12data = autostrada.value.w12_data[selected_time_layout.value].find(e => e.id_venue === parseInt(venue))
    const payload = {"id_key":"id_w12_data","id":w12data.id_w12_data,"value_key":"sky_condition","new_value": id_sky_condition}

    if(icon_list.includes(id_sky_condition) && w12data.cumulated_snow !== null){
      const payloadAzzeramento = {"id_key":"id_w12_data","id":w12data.id_w12_data,"value_key":"cumulated_snow","new_value": null}
      w12data["cumulated_snow"] = null
      stack.push(payloadAzzeramento)
    }

    for(const classe in pluv_classlist){
      if(pluv_classlist[classe].icons.includes(id_sky_condition)){
        let pluv_value = skycond_to_pluv[id_sky_condition]
        const payloadPioggia = {"id_key":"id_w12_data","id":w12data.id_w12_data,"value_key":"precipitation_class","new_value": pluv_value }
        w12data["precipitation_class"] = pluv_value
        stack.push(payloadPioggia)
      }
    }
    w12data["cloud_amount"] = skycond_to_coptot[id_sky_condition]
    const payloadCop = {"id_key":"id_w12_data","id":w12data.id_w12_data,"value_key":"cloud_amount","new_value": skycond_to_coptot[id_sky_condition]}
    stack.push(payloadCop)

    w12data["sky_condition"] = id_sky_condition
    stack.push(payload)
  })

  venuesSelected.value = []
  closeModal()
  const payloadusername = {"id_key":"id_w12","id":autostrada.value.id_w12,"value_key":"username","new_value": store.state.username}
  stack.push(payloadusername)
  saveW12(stack)
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

function openModal(){
  modalElement.value.show()
}

function closeModal(){
  modalElement.value.hide()
}

function updateVenueSelected(venues){
  venuesSelected.value = venues
}

async function fetchAutostradaAction (action) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w12/bulletins/${autostrada_id.value}/${action}/`
  )
  return response
}

async function fetchAutostrada (id) {
  const response = await fetch('/api/w12/bulletins/' + id + '/', {
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

async function fetchIcons () {
  const response = await fetch('/api/w05/sky_conditions/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function bulkUpdateW12(payload) {
  if(store.state.access !== null){
    const response = await api.fetch_wrapper(
      store.state.access,
      `/api/w12/bulletins/bulk_update/`,
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