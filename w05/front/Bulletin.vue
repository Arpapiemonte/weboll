// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <LoginModal ref="login" />
  <VeeForm 
    ref="form"
    as="div"
    class="container-fluid my-3 py-1"
  >
    <div
      id="iconModal"
      class="modal"
      tabindex="-1"
      aria-labelledby="iconModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5
              id="iconModalLabel"
              class="modal-title"
            >
              Cambia l'icona per {{ venueSelection }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            />
          </div>
          <div class="modal-body">
            <div
              class="row"
              role="group"
              aria-label="Icons"
            >
              <div
                v-for="(class_name, icon_class) in iconClasses"
                :key="icon_class"
              >
                <h5
                  class="mt-3"
                >
                  {{ class_name }}
                </h5>
                <button
                  v-for="icon in groupedIcons[icon_class]"
                  :key="icon.id_sky_condition"
                  type="button"
                  class="btn btn-outline-dark col"
                  @click="setIcon(icon.id_sky_condition)"
                >
                  <svg
                    width="75"
                    height="60"
                    viewBox="0 0 750 600"
                  >
                    <use
                      :href="'#id_' + icon.id_sky_condition"
                      x="0"
                      y="0"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="!ready"
      class="text-center"
    >
      <span
        class="spinner-border spinner-border-sm"
        role="status"
        aria-hidden="true"
      />
      Sto caricando il bollettino
    </div>
    <div v-else>
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
            :href="'/api/w05/pdf/' + meteo.id_w05"
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
            v-if="meteo.status === '0' && meteo.start_valid_time.substring(0, 10) === today && state.username"
            :disabled="reopening || sending || resending || reloading"
            type="button"
            class="btn btn-outline-info"
            @click="execute('reload', false, true, 'Temperature ricaricate con le nuove emissioni di multimodel')"
          >
            <span v-if="reloading">
              <span
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              />
              Sto ricaricando le temperature ...
            </span>
            <span v-else>
              <img
                src="~bootstrap-icons/icons/arrow-repeat.svg"
                alt="unlock icon"
                width="18"
                height="18"
              > Ricarica TERMA
            </span>
          </button>
          <button
            v-if="meteo.status === '1' && meteo.start_valid_time.substring(0, 10) === today && ! bozza_presente && state.username"
            :disabled="reopening || sending || reloading"
            type="button"
            class="btn btn-outline-warning"
            @click="execute('reopen', true, true, 'Bollettino riaperto')"
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
            v-if="meteo.status === '0' && meteo.start_valid_time.substring(0, 10) === today && state.username"
            :disabled="history.canUndo || reopening || sending || w05_classes_invalid"
            type="button"
            class="btn btn-outline-success"
            @click="execute('send', false, false, 'Bollettino inviato')"
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
            v-if="meteo.status === '1' && meteo.start_valid_time.substring(0, 10) === today && state.username"
            :disabled="reopening || resending"
            type="button"
            class="btn btn-outline-danger"
            @click="execute('resend', false, false, 'Invio ripetuto')"
          >
            <span v-if="resending">
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
              > Ripeti invio
            </span>
          </button>

          <button
            v-if="meteo.status === '0' && state.username"
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
        <h1>Bollettino Meteo {{ meteo.seq_num }}</h1>
        <div
          v-if="w05_classes_invalid"
          class="alert alert-danger"
        >
          Ci sono dei campi incompleti
        </div>
      </div>
      <div class="row">
        <div class="col-md-2 mb-3">
          <label for="stato">Stato</label>
          <span v-if="meteo.status == 1">
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
        </div>
        <div class="col-md-2 mb-3">
          <label for="start_valid_time">Data emissione</label>
          <input
            id="start_valid_time"
            disabled
            class="form-control"
            name="start_valid_time"
            type="text"
            :value="getDateFormatted(meteo.start_valid_time)"
          >
        </div>
        <div class="col-md-2 mb-3">
          <label for="last_update">Ultima modifica</label>
          <input
            id="last_update"
            disabled
            class="form-control"
            name="last_update"
            type="text"
            :value="getDateFormatted(meteo.last_update)"
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
            :value="meteo.version"
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
            :value="meteo.username"
          >
        </div>
      </div> <!-- end row -->
      <div class="row">
        <div class="col-md-12 mb-3">
          <label for="situazione">Situazione</label>
          <MeteoText
            :id="'situazione'"
            :readonly="readonly"
            :data="meteo"
            :history="history"
            :value-key="'situation'"
            :id-key="'id_w05'"
            @set-level="setLevel"
          />
        </div>
      </div>
      <div
        v-if="'w05_data' in meteo"
        class="row mt-5"
      >
        <div class="col-xl-7 col-md-12 mb-3">
          <!-- tabs start -->
          <ul
            class="nav nav-tabs nav-justified sticky-top bg-light"
            role="tablist"
            style="top: 46px"
          >
            <li
              v-for="i in giorni"
              :key="i"
              class="nav-item"
              role="presentation"
            >
              <button
                class="nav-link"
                :class="{active: giorno == i, 'text-danger': w05_classes_invalid_giornos[i]}"
                :aria-selected="giorno == i"
                type="button"
                role="tab"
                :aria-controls="'giorno' + i + '-tab'"
                @click="setGiorno(i)"
              >
                {{ giorniBulletin[i-1] }}
              </button>
            </li>
          </ul>
          <div
            v-if="ready"
            id="top"
            class="p-3"
          >
            <ValidTime
              :copertura-nuvolosa="meteo.w05_data[giorno == 1 ? 48 : (giorno + 2) * 17 - 2].COP_TOT[0]"
              :previsioni-meteo="meteo.w05_data[giorno == 1 ? 48 : (giorno + 2) * 17 - 2].WFR[0]"
              :readonly="readonly"
              :history="history"
              :giorno="giorno"
              @set-level="setLevel"
            />
            <SubMenu
              :nuvolosita-invalid="w05_classes_invalid_parametros.COP_TOT"
              :precipitazioni-invalid="w05_classes_invalid_parametros.PLUV"
              :zero-invalid="w05_classes_invalid_parametros.FRZLVL"
              :venti-invalid="w05_classes_invalid_parametros.VELV"
              :altri-fenomeni-invalid="w05_classes_invalid_parametros.WFOP"
            />
            <div
              v-if="giorno == 1"
              id="SkyCond"
              role="tabpanel"
              aria-labelledby="giorno1-tab"
            >
              <SkyCond1
                title="Situazione meteo"
                class="offset"
                :cieli="[meteo.w05_data[48], meteo.w05_data[51], meteo.w05_data[50]]"
                :index="1"
                :readonly="readonly"
                :selected-venues="selectedVenues"
                :icons="icons"
                :history="history"
                :venue-names="venueNames"
                @transformed="onTransformed"
                @set-venue="setVenue"
              />
            </div>
            <div
              v-else
              id="SkyCond"
              role="tabpanel"
              aria-labelledby="giorno2-tab"
            >
              <SkyCond2
                title="Situazione meteo"
                class="offset"
                :cieli="[meteo.w05_data[(giorno + 2) * 17 - 4], meteo.w05_data[(giorno + 2) * 17 - 3], meteo.w05_data[(giorno + 2) * 17], meteo.w05_data[(giorno + 2) * 17 - 1]]"
                :index="2"
                :readonly="readonly"
                :selected-venues="selectedVenues"
                :icons="icons"
                :periodo="periodo"
                :history="history"
                :venue-names="venueNames"
                @period-changed="changePeriod"
                @transformed="onTransformed"
                @set-venue="setVenue"
              />
            </div>
            <Nuvolosita
              id="Nuvolosita"
              class="offset"
              :copertura-nuvolosa="meteo.w05_data[giorno == 1 ? 48 : (giorno + 2) * 17 - 2].COP_TOT[0]"
              :classes0012="giorno == 1 ? null : meteo.w05_classes[(giorno + 2) * 17 - 4].COP_TOT"
              :classes1224="meteo.w05_classes[(giorno + 2) * 17 - 3].COP_TOT"
              :class-description="classes.COP_TOT"
              :readonly="readonly"
              :history="history"
              @set-class="setClass"
              @set-level="setLevel"
            />
            <Precipitazioni
              id="Precipitazioni"
              class="offset"
              :livello-pioggia="meteo.w05_data[giorno == 1 ? 48 : (giorno + 2) * 17 - 2].PLUV[0]"
              :classes0012="giorno == 1 ? null : meteo.w05_classes[(giorno + 2) * 17 - 4].PLUV"
              :classes1224="meteo.w05_classes[(giorno + 2) * 17 - 3].PLUV"
              :class-description="classes.PLUV"
              :readonly="readonly"
              :history="history"
              @set-class="setClass"
              @set-level="setLevel"
            />
            <ZeroTermico
              id="ZeroTermico"
              class="offset"
              :freezing-level-giornata="meteo.w05_data[giorno == 1 ? 48 : (giorno + 2) * 17 - 2].FRZLVL[0]"
              :freezing-level-mattino="giorno == 1 ? null : meteo.w05_data[(giorno + 2) * 17 - 4].FRZLVL[0]"
              :freezing-level-pomeriggio="meteo.w05_data[(giorno + 2) * 17 - 3].FRZLVL[0]"
              :classes0024="giorno == 1 ? null : meteo.w05_classes[(giorno + 2) * 17 - 2].FRZLVL[0]"
              :classes0012="giorno == 1 ? null : meteo.w05_classes[(giorno + 2) * 17 - 4].FRZLVL[0]"
              :classes1224="meteo.w05_classes[(giorno + 2) * 17 - 3].FRZLVL[0]"
              :class-description="classes.FRZLVL"
              :readonly="readonly"
              :history="history"
              @set-class="setClass"
              @set-level="setLevel"
            />
            <QuotaNeve
              id="QuotaNeve"
              class="offset"
              :data="meteo.w05_data[giorno == 1 ? 48 : (giorno + 2) * 17 - 2].SNOW_LEV"
              :classes="meteo.w05_classes[giorno == 1 ? 48 : (giorno + 2) * 17 - 2].SNOW_LEV"
              :class-description="classes.SNOW_LEV"
              :readonly="readonly"
              :history="history"
              @set-class="setClass"
              @set-level="setLevel"
            />
            <Venti
              id="Venti"
              class="offset"
              :velocita-vento="meteo.w05_data[giorno == 1 ? 48 : (giorno + 2) * 17 - 2].VELV[0]"
              :classes="meteo.w05_classes[giorno == 1 ? 48 : (giorno + 2) * 17 - 2].VELV"
              :class-description="classes.VELV"
              :readonly="readonly"
              :history="history"
              @set-class="setClass"
              @set-level="setLevel"
            />
            <AltriFenomeni
              id="AltriFenomeni"
              class="offset"
              :altri-fenomeni="meteo.w05_data[giorno == 1 ? 48 : (giorno + 2) * 17 - 2].WFOP[0]"
              :readonly="readonly"
              :history="history"
              @set-class="setClass"
              @set-level="setLevel"
            />
          </div> <!-- end top -->
          <div
            v-else
            class="d-flex justify-content-center m-5"
          >
            <div
              class="spinner-border text-info"
              role="status"
            >
              <span class="visually-hidden">Loading ...</span>
            </div>
          </div>
        </div> <!-- end col-md-7 -->

        <div class="col-xl-5 col-md-12 mb-3">
          <div
            class="sticky-top pt-5"
            style="z-index: 0;"
          >
            <MapMeteo
              :orography="true"
              :rivers="false"
              :provinces="false"
              :capitals="true"
              :meteo="true"
              :grouped-icons="groupedIcons"
              :selected-venues="selectedVenues"
              :icons="icons"
              :sky-condition="meteo.w05_data[timeLayout].SKY_CONDIT"
              :readonly="readonly"
              @open-modal="openModal"
              @toggle-venue="toggleVenue"
            />
            <div
              v-if="giorno != 1"
              class="caption text-center mt-5"
            >
              <button
                v-if="periodo==1"
                type="button"
                class="btn btn-outline-dark"
                title="passa a Pomeriggio"
                @click="periodo = 2"
              >
                <img
                  src="~bootstrap-icons/icons/clock-fill.svg"
                  alt="print icon"
                  width="18"
                  height="18"
                > Mattino
              </button>
              <button
                v-else
                type="button"
                class="btn btn-outline-dark"
                title="passa a Mattino"
                @click="periodo = 1"
              >
                <img
                  src="~bootstrap-icons/icons/clock.svg"
                  alt="print icon"
                  width="18"
                  height="18"
                > Pomeriggio
              </button>
            </div>
            <div
              v-else
              class="caption text-center mt-5"
            >
              <span>          <img
                src="~bootstrap-icons/icons/clock.svg"
                alt="print icon"
                width="18"
                height="18"
              > Pomeriggio</span>
            </div>
          </div>
        </div> <!-- end col-md-5 -->
      </div> <!-- end row -->
    </div>
  </VeeForm>
</template>

<script>
import { Modal } from 'bootstrap'

import { Form as VeeForm } from 'vee-validate'

// @ is an alias to /src
import SubMenu from './SubMenu.vue'
import ValidTime from './ValidTime.vue'

import MeteoText from './MeteoText.vue'
import SkyCond1 from './SkyCond1.vue'
import SkyCond2 from './SkyCond2.vue'
import MapMeteo from './MapMeteo.vue'
import HistoryStack from '@/components/History.js'
import api from '@/api'
import store from '@/store'
import apply from '@/components/apply'
import Nuvolosita from './Nuvolosita.vue'
import Precipitazioni from './Precipitazioni.vue'
import ZeroTermico from './ZeroTermico.vue'
import QuotaNeve from './QuotaNeve.vue'
import Venti from './Venti.vue'
import AltriFenomeni from './AltriFenomeni.vue'
import LoginModal from '@/components/LoginModal.vue'

export default {
  name: 'MeteoBulletin',
  components: {
    MeteoText,
    SubMenu,
    ValidTime,
    SkyCond1,
    SkyCond2,
    MapMeteo,
    Nuvolosita,
    Precipitazioni,
    ZeroTermico,
    QuotaNeve,
    Venti,
    AltriFenomeni,
    VeeForm,
    LoginModal,
  },
  data() {
    // non reactive properties
    this.icon_blacklist = [ 10, 12, 1, 26 ]
    this.iconModal = null
    this.iconClasses = {
      COP_TOT: "Copertura nuvolosa totale",
      PLUV: "Livello pioggia sui 10 minuti",
      SNOW: "Neve( cm)",
      STORM: "Classe temporali",
      VELV: "Velocita' vento (vettoriale)",
      VIS_10M: "Visibility 10 minutes average (max 50 km)"
    }
    return {
      // reactive properties
      giorno: 1,
      giorni: [1, 2, 3, 4],
      periodo: 2,  // 1 = mattina, 2 = pomeriggio
      meteo_id: null,
      ready: false,
      meteo: {},
      icons: [],
      classes: [],
      bulletins: [],
      bozza_presente: false,
      selectedVenues: {
        1: false,
        9: false,
        11: false,
        28: false,
        33: false,
        59: false,
        63: false,
        64: false,
        87: false,
        88: false,
        89: false,
        90: false,
        91: false,
        92: false,
        93: false
      },
      venueNames: [],
      readonly: true,
      history: new HistoryStack(),
      reopening: false,
      sending: false,
      resending: false,
      reloading: false,
      validationText: '',
      nuvolositaValid: true,
      precipitazioniValid: true,
      zeroValid: true,
      ventiValid: true,
      countdown: 0,
      state: store.state
    }
  },
  computed: {
    timeLayout() {
      let tl = (this.giorno + 2) * 17 - 5 + this.periodo
      return tl.toString()
    },
    today() {
      // returns today in 2021-04-22 format
      let d = new Date()
      return d.toISOString().substring(0, 10)
    },
    groupedIcons() {
      return this.icons.reduce((result, icon) => {
        if (!result[icon.id_parametro]) {
          result[icon.id_parametro] = []
        }
        result[icon.id_parametro].push(icon)
        result[icon.id_parametro].sort((a, b) => a.ordinamento - b.ordinamento)
        return result
      }, {})
    },
    terma_67() {
      // riarrangia i dati tabellari da w05_data per la venue 67 (intero Piemonte) e id_parametro pari a TERMA
      // estraendoli in un dizionario indicizzato per time_layout (51 serve poi per terma_delta[1][0]), esempio:
      // {
      //   "33": {
      //     "id_w05_data": 1107,
      //     "numeric_value": "10.00",
      //     "id_trend": 2,
      //     ...
      //   },
      //   "50": { ... },
      //   "51": { ... },
      //   "67": { ... },
      //   "68": { ... },
      //   "84": { ... },
      //   "85": { ... },
      //   "101": { ... },
      //   "102": { ... }
      // }
      let t_67 = {}
      if ('w05_data' in this.meteo) {
        Object.keys(this.meteo.w05_data).forEach(time_layout => {
          if ('TERMA' in this.meteo.w05_data[time_layout]) {
            this.meteo.w05_data[time_layout]['TERMA'].forEach(data => {
              if (data.id_venue === 67) {
                // console.log('terma_67() setto t_67',time_layout,data.id_aggregazione)
                t_67[time_layout] = data
              }
            })
          }
        })
      }
      return t_67
    },
    terma_67_classes() {
      // riarrangia i dati tabellari da w05_classes per la venue 67 (intero Piemonte) e id_parametro pari a TERMA
      // estraendoli in un dizionario indicizzato per time_layout, esempio:
      // {
      //   "50": {
      //     "id_w05_classes": 503,
      //     "id_classes_value": 34,
      //     ...
      //   },
      //   "51": { ... },
      //   "67": { ... },
      //   "68": { ... },
      //   "84": { ... },
      //   "85": { ... },
      //   "101": { ... },
      //   "102": { ... }
      // }
      let t_67 = {}
      if ('w05_classes' in this.meteo) {
        Object.keys(this.meteo.w05_classes).forEach(time_layout => {
          if ('TERMA' in this.meteo.w05_classes[time_layout]) {
            this.meteo.w05_classes[time_layout]['TERMA'].forEach(data => {
              if (data.id_venue === 67) {
                // console.log('terma_67_classes() setto t_67',time_layout,data.id_classes_value)
                t_67[time_layout] = data
              }
            })
          }
        })
      }
      return t_67
    },
    terma_delta() {
      // calcola le differenze in °C tra la temperatura minima e massima del giorno rispetto al giorno precedente
      // per tutti e quattro i giorni coperti dal bollettino meteo, esempio:
      //    [[1,-6],[-3,4],[-2,-2],[0,0]]
      // NOTA: terma_delta[0][0] è anomalo essendo valorizzato con l'id_trend (che può valere solo 1, 0 o 2)
      // però non viene mai usato
      let t = [[], [], [], []]

      // id_time_layouts = 33 corrisponde alle temperature massime di ieri
      // e serve per calcolare il trend delle massime di oggi
      if (33 in this.terma_67) {
        // per le minime

        // 1° giorno: id_trend (id_time_layouts=51) non lo modifico perchè è un dato osservato
        t[0][0] = this.terma_67[51].id_trend
        // 2° giorno: id_trend (id_time_layouts=68) valorizzato in base a value(tl=68)-value(tl=51)
        t[1][0] = this.terma_67[68].numeric_value - this.terma_67[51].numeric_value
        // 3° giorno: id_trend (id_time_layouts=85) valorizzato in base a value(tl=85)-value(tl=68)
        t[2][0] = this.terma_67[85].numeric_value - this.terma_67[68].numeric_value
        // 4° giorno: id_trend (id_time_layouts=102) valorizzato in base a value(tl=102)-value(tl=85)
        t[3][0] = this.terma_67[102].numeric_value - this.terma_67[85].numeric_value

        // per le massime

        // 1° giorno: id_trend (id_time_layouts=50) valorizzato in base a value(tl=50)-value(tl=33)
        t[0][1] = this.terma_67[50].numeric_value - this.terma_67[33].numeric_value
        // 2° giorno: id_trend (id_time_layouts=67) valorizzato in base a value(tl=67)-value(tl=50)
        t[1][1] = this.terma_67[67].numeric_value - this.terma_67[50].numeric_value
        // 3° giorno: id_trend (id_time_layouts=84) valorizzato in base a value(tl=84)-value(tl=67)
        t[2][1] = this.terma_67[84].numeric_value - this.terma_67[67].numeric_value
        // 4° giorno: id_trend (id_time_layouts=101) valorizzato in base a value(tl=101)-value(tl=84)
        t[3][1] = this.terma_67[101].numeric_value - this.terma_67[84].numeric_value
      }

      return t
    },
    w05_classes_invalid_time_layouts_id_parametro() {
      // validate the meteo classes and associated text_values for each combination of id_time_layout and id_parametro
      // returns a data structure like this (false means valid, true means invalid/incomplete data):
      // {
      //   48: {COP_TOT: true, PLUV: true, FRZLVL: true, SNOW_LEV: true, VELV: true, WFOP: false},
      //   50: {TERMA: true},
      //   51: {TERMA: true},
      //   64: {COP_TOT: true, PLUV: true, FRZLVL: true},
      //   65: {COP_TOT: true, PLUV: false, FRZLVL: false},
      //   66: {FRZLVL: true, SNOW_LEV: true, VELV: true, WFOP: false},
      //   67: {TERMA: true},
      //   68: {TERMA: false},
      //   ...
      // }
      let data = {}
      if ('w05_classes' in this.meteo) {
        let id_time_layouts = Object.keys(this.meteo.w05_classes)
        id_time_layouts.forEach(id_time_layout => {
          let id_parametros = Object.keys(this.meteo.w05_classes[id_time_layout])
          if (!('id_time_layout' in data)) {
            data[id_time_layout] = {}
          }
          id_parametros.forEach(id_parametro => {
            data[id_time_layout][id_parametro] = this.meteo.w05_classes[id_time_layout][id_parametro].some(element => element.id_classes_value > 80 )
          })
        })
      }
      if ('w05_data' in this.meteo) {
        let id_time_layouts = Object.keys(this.meteo.w05_data)
        const text_values = ['WFOP', 'COP_TOT', 'PLUV', 'VELV', 'FRZLVL']
        id_time_layouts.forEach(id_time_layout => {
          // array intersection https://stackoverflow.com/a/1885569
          let id_parametros = Object.keys(this.meteo.w05_data[id_time_layout]).filter(value => text_values.includes(value))
          if (!(id_time_layout in data)) {
            data[id_time_layout] = {}
          }
          id_parametros.forEach(id_parametro => {
            let invalid = this.meteo.w05_data[id_time_layout][id_parametro].some(element => this.isEmpty(element.text_value) )
            if (id_parametro === 'FRZLVL' && !(['48', '66', '83', '100'].includes(id_time_layout))) {
              // skip check for mattina / pomeriggio
            } else {
              if (id_parametro in data[id_time_layout]) {
                data[id_time_layout][id_parametro] = data[id_time_layout][id_parametro] || invalid
              } else {
                data[id_time_layout][id_parametro] = invalid
              }
            }
          })
        })
      }
      return data
    },
    w05_classes_invalid_giornos_id_parametro() {
      // validate the meteo classes and associated text_values for each combination of giorno and id_parametro
      // returns a data structure like this (false means valid, true means invalid/incomplete data):
      // {
      //   1: {COP_TOT: true, PLUV: true, FRZLVL: true, SNOW_LEV: true, VELV: true, WFOP: false},
      //   2: {COP_TOT: true, PLUV: true, FRZLVL: true, SNOW_LEV: true, VELV: true, WFOP: false},
      //   3: {COP_TOT: true, PLUV: false, FRZLVL: false, SNOW_LEV: false, VELV: true, WFOP: false},
      //   4: {COP_TOT: true, PLUV: false, FRZLVL: false, SNOW_LEV: false, VELV: true, WFOP: false}
      // }
      let data = {}
      if ('w05_data' in this.meteo) {
        data[1] = {
          COP_TOT: this.w05_classes_invalid_time_layouts_id_parametro[48]['COP_TOT'],
          PLUV: this.w05_classes_invalid_time_layouts_id_parametro[48]['PLUV'],
          FRZLVL: this.w05_classes_invalid_time_layouts_id_parametro[48]['FRZLVL'],
          VELV: this.w05_classes_invalid_time_layouts_id_parametro[48]['VELV'],
          WFOP: this.w05_classes_invalid_time_layouts_id_parametro[48]['WFOP'],
        };
        [2, 3, 4].forEach(giorno => {
          data[giorno] = {
            COP_TOT: this.w05_classes_invalid_time_layouts_id_parametro[(giorno + 2) * 17 - 4]['COP_TOT'] || this.w05_classes_invalid_time_layouts_id_parametro[(giorno + 2) * 17 - 3]['COP_TOT'] || this.w05_classes_invalid_time_layouts_id_parametro[(giorno + 2) * 17 - 2]['COP_TOT'],
            PLUV: this.w05_classes_invalid_time_layouts_id_parametro[(giorno + 2) * 17 - 4]['PLUV'] || this.w05_classes_invalid_time_layouts_id_parametro[(giorno + 2) * 17 - 3]['PLUV'] || this.w05_classes_invalid_time_layouts_id_parametro[(giorno + 2) * 17 - 2]['PLUV'],
            FRZLVL: this.w05_classes_invalid_time_layouts_id_parametro[(giorno + 2) * 17 - 2]['FRZLVL'] || this.w05_classes_invalid_time_layouts_id_parametro[(giorno + 2) * 17 - 4]['FRZLVL'] || this.w05_classes_invalid_time_layouts_id_parametro[(giorno + 2) * 17 - 3]['FRZLVL'] || this.w05_classes_invalid_time_layouts_id_parametro[(giorno + 2) * 17 - 2]['FRZLVL'],
            VELV: this.w05_classes_invalid_time_layouts_id_parametro[(giorno + 2) * 17 - 2]['VELV'],
            WFOP: this.w05_classes_invalid_time_layouts_id_parametro[(giorno + 2) * 17 - 2]['WFOP'],
          }
        })
      }
      return data
    },
    w05_classes_invalid_giornos() {
      // validate the meteo classes and associated text_values for each giorno
      // returns a data structure like this (false means valid, true means invalid/incomplete data):
      // {1: true, 2: true, 3: true, 4: true}
      let data = {}
      Object.keys(this.w05_classes_invalid_giornos_id_parametro).forEach(giorno => {
        let element = this.w05_classes_invalid_giornos_id_parametro[giorno]
        data[giorno] = Object.values(element).some(element => element)
      })
      return data
    },
    w05_classes_invalid_parametros() {
      // validate the meteo classes and associated text_values for the current giorno
      return this.w05_classes_invalid_giornos_id_parametro[this.giorno]
    },
    w05_classes_invalid() {
      // validate all the meteo classes and associated text_values
      if ('w05_data' in this.meteo) {
        return Object.values(this.w05_classes_invalid_giornos).some(element => element) || !this.meteo.situation.trim()
      } else {
        return false
      }
    },
    venueSelection() {
      return Object.keys(this.selectedVenues).filter(venue => { return this.selectedVenues[venue] })
    },
    giorniBulletin() {
      var bulletinDays = []
      var stringBulletinDays = ['', '', '', '']
      if ('start_valid_time' in this.meteo){
        var currentFullDate = new Date(this.meteo.start_valid_time)
        const startDay = currentFullDate.getDate()
        for(let i = 0; i <= 3 ; i++){
          bulletinDays[i] = new Date(currentFullDate.getTime())
          currentFullDate = new Date(this.meteo.start_valid_time)
          currentFullDate.setDate(startDay+i+1)
          stringBulletinDays[i] = bulletinDays[i].getDate() + "/" + (bulletinDays[i].getMonth()+1)  + "/" +  bulletinDays[i].getFullYear()
        }
      }
      return stringBulletinDays
    },
  },
  watch: {
    '$route': 'fetchData',
    terma_delta(val) {
      // aggiorna terma_67 e terma_67_classes ogni volta che l'utente cambia i valori TERMA per id_venue pari a 67
      // terma_67_classes è ricavato come funzione di terma_67
      // NOTA: val[0][0] non viene usato perché corrisponde al trend delle tmin osservate, quindi terma_67[51].id_trend
      // è già scritto nella pietra e non va mai modificato

      // dizionario di appoggio con la mappatura tra id_time_layout e indici all'interno di terma_delta
      const id_time_layouts_to_trend_index = {
        50: [0, 1],
        67: [1, 1],
        68: [1, 0],
        84: [2, 1],
        85: [2, 0],
        101: [3, 1],
        102: [3, 0]
      }
      // id_time_layouts = 33 corrisponde alle temperature massime di ieri
      // e serve per calcolare il trend delle massime di oggi
      if (33 in this.terma_67) {
        Object.keys(id_time_layouts_to_trend_index).forEach(id_time_layout => {
          const [i1, i2] = id_time_layouts_to_trend_index[id_time_layout]
          const trend = this.trend(val[i1][i2])
          this.terma_67[id_time_layout].id_trend = trend
        })
      }
    },
    countdown: {
      handler () {
        if (this.countdown >= 4) {
          this.ready = true
        }
      }
    },
  },
  created() {
    this.goto(0)
    this.fetchData()
  },
  mounted: function () {
    this.iconModal = new Modal(document.getElementById('iconModal'))
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
    isEmpty(s) {
      return ((typeof s == 'undefined') || (s == null) || (!s) || (s.trim().length == 0))
    },
    goto(page) {
      this.current_page = page
      api.fetchBulletins('w05/bulletins', page).then(response => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero della lista`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json()
      }).then(data => {
        this.bulletins = data.results
        this.count = data.count
        for (var i = 0; i < this.bulletins.length; i++) {
          if (!this.bozza_presente){
            if (this.bulletins[i].status === '0'){
              this.bozza_presente = true;
            }
          }
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
    },
    async fetchMeteo () {
      const response = await fetch('/api/w05/bulletins/' + this.meteo_id + '/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    setLevel(id_value, old_value, new_value, value_key, id_key='id_w05_data') {
      let data = {
        id_key: id_key,
        id: id_value,
        value_key: value_key,
        old_value: old_value,
        new_value: new_value
      }
      this.onTransformed(data)
    },
    setClass(id_w05_classes, old_value, new_value) {
      let data = {
        id_key: 'id_w05_classes',
        id: id_w05_classes,
        value_key: 'id_classes_value',
        old_value: old_value,
        new_value: new_value
      }
      // console.log(data)
      this.onTransformed(data)
    },
    onW05Changed(id_w05, value_key, old_value, new_value) {
      let data = {
        id_key: 'id_w05',
        id: id_w05,
        value_key: value_key,
        old_value: old_value,
        new_value: new_value
      }
      this.onTransformed(data)
    },
    // this handler is triggered to modify a single w05 or w05_data record
    onTransformed(snapshot) {
      apply(this.meteo, snapshot);
      this.history.record(snapshot)
    },
    changePeriod(p) {
      this.periodo = p
    },
    undo() {
      if (!this.readonly && this.history.canUndo) {
        let snapshot = this.history.undo()
        let found = apply(this.meteo, snapshot, true)
        if (snapshot.id_key.length === 6) {
          this.$toast.open(
              {
                message: 'Undo: '+ snapshot.value_key,
                type: 'success',
                position: 'top-left'
              }
            )
        } else {
          this.$toast.open(
              {
                message: 'Undo: icona nella venue ' + found.id_venue + ' con scadenza ' + found.end_valid_time +' a ' + snapshot.old_value,
                type: 'success',
                position: 'top-left'
              }
            )
        }
      }
    },
    redo() {
      if (!this.readonly && this.history.canRedo) {
        let snapshot = this.history.redo()
        let found = apply(this.meteo, snapshot);
        if (snapshot.id_key.length === 6) {
          this.$toast.open(
              {
                message: 'Redo: '+ snapshot.value_key,
                type: 'success',
                position: 'top-left'
              }
            )
        } else {
          this.$toast.open(
              {
                message: 'Redo: icona nella venue ' + found.id_venue + ' con scadenza ' + found.end_valid_time +' a ' + snapshot.new_value,
                type: 'info',
                position: 'top-left'
              }
            )
        }
      }
    },
    remove() {
      if (
        confirm('Vuoi davvero cancellare questo bollettino?')
      ) {
        api.fetchBulletinDelete(this.meteo_id, 'w05/bulletins', store).then(response => {
          if (response.ok) {
            this.$toast.open(
              {
                message: 'Bollettino cancellato',
                type: 'success',
                position: 'top-left'
              }
            )
            this.bozza_presente = false
            this.$router.back()
          } else {
            this.$toast.open(
              {
                message: `Errore ${response.status} nella cancellazione del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
            if (response.status === 401 || response.status === 403) {
              this.$refs.login.show()
              return null
            }
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
    async fetchMeteoAction(action) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w05/bulletins/${this.meteo_id}/${action}/`
      )
      return response
    },
    execute(action, reroute, draft, message) {
      // action: one of reload, reopen, send, resend
      // reroute: if true, will push a new location to the router (https://router.vuejs.org/guide/essentials/navigation.html#router-push-location-oncomplete-onabort)
      // draft: records the current bulletin as draft
      // message: on success, it will be shown in the toast
      if (action === 'send' && this.w05_classes_invalid) {
        this.$toast.open(
          {
            message: `Ci sono dei campi incompleti, impossibile inviare`,
            type: 'error',
            position: 'top-left'
          }
        )
        return
      } else if (action === 'resend' && !confirm('Vuoi davvero ripetere l\'invio di questo bollettino?')) {
        return
      } else {
        this.really_execute(action, reroute, draft, message)
      }
    },
    really_execute(action, reroute, draft, message) {
      this[action + 'ing'] = true
      this.fetchMeteoAction(action).then(response => {
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
        this.bozza_presente = draft
        if (reroute) {
          this.$router.push({ path: `/w05/${data.id_w05}`})
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
    async bulkUpdateW05(snapshots) {
      let payload = snapshots
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w05/bulletins/bulk_update/`,
        {
          method: 'POST',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    classes_trend(id_time_layouts, id_trend) {
      // funzione ausiliaria che mappa (id_time_layouts, id_trend) -> id_classes_value,
      // però in un modo differenziato per le massime e le minime, poiché il db è stato pensato così:
      // ogni andamento e ogni parametro ha un codice id_classes_value differente
      let result
      var tl_min=[51, 68, 85, 102];
      var tl_max=[50, 67, 84, 101];
      if (tl_min.includes(id_time_layouts)){
        switch (id_trend) {
          case 1:
            result = 34;
            break;
          case 0:
            result = 35;
            break;
          case 2:
            result = 36;
            break;
          default:
            break;
        }
      }else if (tl_max.includes(id_time_layouts)) {
        switch (id_trend) {
          case 1:
            result = 37;
            break;
          case 0:
            result = 38;
            break;
          case 2:
            result = 39;
            break;
          default:
            break;
        }
      }
      // console.log('classes_trend()', result)
      return result
    },
    save() {
      // console.log('save')
      this.history.shake()
      let discarded = this.history.splice()
      let original_length = discarded.length
      const original_discarded = [...discarded];

      // qui agli snapshot in coda per essere salvati (le modifiche direttamente fatte dal'utente) vengono aggiunti:

      [68, 85, 102, 50, 67, 84, 101].forEach(id_time_layouts => {
        // - i trend sia in w05_data ...
        discarded.push({
          id_key: "id_w05_data",
          id: this.terma_67[id_time_layouts].id_w05_data,
          value_key: "id_trend",
          old_value: null,
          new_value: this.terma_67[id_time_layouts].id_trend
        })
        // - ... che anche in w05_classes
        discarded.push({
          id_key: "id_w05_classes",
          id: this.terma_67_classes[id_time_layouts].id_w05_classes,
          value_key: "id_classes_value",
          old_value: null,
          new_value: this.classes_trend(id_time_layouts, this.terma_67[id_time_layouts].id_trend)
        })
      })

      // - version
      discarded.push({
        id_key: "id_w05",
        id: this.meteo.id_w05,
        value_key: "version",
        old_value: this.meteo.version,
        new_value: this.meteo.version + 1
      })
      // - e username
      discarded.push({
        id_key: "id_w05",
        id: this.meteo.id_w05,
        value_key: "username",
        old_value: this.meteo.username,
        new_value: this.state.username
      })
      this.bulkUpdateW05(discarded).then((response) => {
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
        this.meteo.version += 1
        this.meteo.username = this.state.username
        this.meteo.last_update = data.last_update
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
          if(snapshot.id_key === "id_w05"){
            if (snapshot.new_value !== data.bulletin[snapshot.value_key])
                snapshotUnsaved.push(snapshot)
          }else if (snapshot.id_key === "id_w05_data"){
            let element = data.bulletin.w05data_set.find(element => element.id_w05_data === snapshot.id)
            if(snapshot.value_key === "numeric_value"){
              if(Number(snapshot.new_value) !== Number(element[snapshot.value_key]))
                snapshotUnsaved.push(snapshot)
            }else if (snapshot.value_key === "text_value"){
              if(snapshot.new_value !== element[snapshot.value_key])
                snapshotUnsaved.push(snapshot)
            }
          }else if (snapshot.id_key === "id_w05_classes"){
            let element = data.bulletin.w05classes_set.find(element => element.id_w05_classes === snapshot.id)
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

          - pagina: https://production.example.com/w05/${this.meteo.id_w05}
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
    setGiorno(i) {
      if (i == 1) {
        this.periodo = 2
      } else {
        this.periodo = 1
      }
      this.giorno = i
    },
    async fetchIcons () {
      const response = await fetch('/api/w05/sky_conditions/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    async fetchVenues () {
      const response = await fetch('/api/w05/venue_names/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    async fetchClasses () {
      const response = await fetch('/api/w05/classes/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    fetchData() {
      this.meteo_id = this.$route.params.id
      if (typeof this.meteo_id === 'undefined') {
        return
      }
      this.fetchIcons().then(response => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero delle icone`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json()
      }).then(data => {
        this.icons = data.filter(icon => !this.icon_blacklist.includes(icon.id_sky_condition)).map(icon => {
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
        this.countdown++
      }).catch(error => {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
      this.fetchVenues().then(response => {
        if (!response.ok) {
          this.$toast.open(
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
          this.venueNames [element.id_venue] = element.description
        }
        this.countdown++
      }).catch(error => {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
      this.fetchClasses().then(response => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero delle classi`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json()
      }).then(data => {
        this.classes = data.reduce((accumulator, currentValue) => {
          accumulator[currentValue.id_parametro][currentValue.id_classes] = currentValue;
          return accumulator
        }, {COP_TOT: {}, FRZLVL: {}, PLUV: {}, SNOW_LEV: {}, TERMA: {}, VELV: {}})
        this.countdown++
      }).catch(error => {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
      this.fetchMeteo().then(response => {
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
        let meteo = data
        meteo.w05_data = { }
        if ('w05data_set' in meteo) {
          meteo.w05data_set.forEach((element) => {
            if (!(element.id_time_layouts in meteo.w05_data)) {
              meteo.w05_data[element.id_time_layouts] = { }
            }
            if (element.id_parametro in meteo.w05_data[element.id_time_layouts]) {
              meteo.w05_data[element.id_time_layouts][element.id_parametro].push(element)
            } else {
              meteo.w05_data[element.id_time_layouts][element.id_parametro] = [element]
            }
          })
          delete meteo.w05data_set
          meteo.w05_classes = { }
          if ('w05classes_set' in meteo) {
            meteo.w05classes_set.forEach((element) => {
              if (!(element.id_time_layouts in meteo.w05_classes)) {
                meteo.w05_classes[element.id_time_layouts] = { }
              }
              if (element.id_parametro in meteo.w05_classes[element.id_time_layouts]) {
                meteo.w05_classes[element.id_time_layouts][element.id_parametro].push(element)
              } else {
                meteo.w05_classes[element.id_time_layouts][element.id_parametro] = [element]
              }
            })
            delete meteo.w05classes_set
          }
        }
        this.meteo = meteo
        this.readonly = (meteo.status === '1' || !this.state.username)
        this.countdown++
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
    trend(delta) {
      return [2, 0, 1][Math.sign(delta) + 1]
    },
    openModal(venue = 0) {
      this.selectedVenues[venue] = true
      this.iconModal.show()
    },
    toggleVenue(venue) {
      this.selectedVenues[venue] = !this.selectedVenues[venue]
    },
    setVenue(venue, value) {
      console.log(`setVenue(${venue}, ${value})`)
      this.selectedVenues[venue] = value
    },
    setIcon(value) {
      if (this.venueSelection.length > 0) {
        let skyCondition = this.meteo.w05_data[this.timeLayout].SKY_CONDIT
        skyCondition.forEach((element, ) => {
          if (this.venueSelection.includes(element.id_venue.toString())) {
            this.setLevel(element.id_w05_data, element.numeric_value, value, 'numeric_value')
          }
        })
      }
      this.iconModal.hide()
      this.setAll(false)
    },
    setAll(status) {
      Object.keys(this.selectedVenues).forEach(venue => { this.selectedVenues[venue] = status})
    },
    getDateFormatted(rawString) {
      return api.getDateFormatted(rawString)
    }
  }
}
</script>

<style>
.dirty {
  border: 3px solid #0dcaf0;
}
</style>
