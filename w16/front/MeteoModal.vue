// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt

<template>
  <div
    id="meteoModal"
    class="modal"
    tabindex="-1"
    aria-labelledby="meteoModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h5
            id="meteoModalLabel"
            class="modal-title"
          >
            Campi ICON-2I run 00 di oggi
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          />
        </div>
        <div
          class="modal-body"
          style="height: 670px"
        >
          <ul
            id="myTab"
            class="nav nav-tabs"
            role="tablist"
          >
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                id="prec-tab"
                class="nav-link"
                :class="{active: meteo === 'prec'}"
                type="button"
                role="tab"
                aria-controls="prec"
                aria-selected="true"
                @click="frame = 0; meteo = 'prec'"
              >
                Precipitazioni mm/6hr
              </button>
            </li>
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                id="temp-tab"
                class="nav-link"
                :class="{active: meteo === 'temp'}"
                type="button"
                role="tab"
                aria-controls="temp"
                aria-selected="false"
                @click="frame = 0; meteo = 'temp'"
              >
                Temperature a 700 hPa, °C
              </button>
            </li>
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                id="tma700-tab"
                class="nav-link"
                :class="{active: meteo === 'tma700'}"
                type="button"
                role="tab"
                aria-controls="tma700"
                aria-selected="false"
                @click="frame = 0; meteo = 'tma700'"
              >
                Nuvolosità e vento a 700 hPa
              </button>
            </li>
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                id="tma850-tab"
                class="nav-link"
                :class="{active: meteo === 'tma850'}"
                type="button"
                role="tab"
                aria-controls="tma850"
                aria-selected="false"
                @click="frame = 0; meteo = 'tma850'"
              >
                Nuvolosità e vento a 850 hPa
              </button>
            </li>
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                id="totclo-tab"
                class="nav-link"
                :class="{active: meteo === 'totclo'}"
                type="button"
                role="tab"
                aria-controls="totclo"
                aria-selected="false"
                @click="frame = 0; meteo = 'totclo'"
              >
                Total Cloud Cover, 0-1
              </button>
            </li>
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                id="wind700-tab"
                class="nav-link"
                :class="{active: meteo === 'wind700'}"
                type="button"
                role="tab"
                aria-controls="wind700"
                aria-selected="false"
                @click="frame = 0; meteo = 'wind700'"
              >
                Vento a 700 hPa, m/s
              </button>
            </li>
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                id="wind850-tab"
                class="nav-link"
                :class="{active: meteo === 'wind850'}"
                type="button"
                role="tab"
                aria-controls="wind850"
                aria-selected="false"
                @click="frame = 0; meteo = 'wind850'"
              >
                Vento a 850 hPa, m/s
              </button>
            </li>
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                id="wind950-tab"
                class="nav-link"
                :class="{active: meteo === 'wind950'}"
                type="button"
                role="tab"
                aria-controls="wind950"
                aria-selected="false"
                @click="frame = 0; meteo = 'wind950'"
              >
                Vento a 950 hPa, m/s
              </button>
            </li>
          </ul>

          <div class="h-100 position-relative">
            <transition name="fade">
              <img
                :key="frame"
                :src="current_meteo_images[frame]"
                width="800"
                class="position-absolute start-50 translate-middle"
                style="top: 280px"
              >
            </transition>
          </div>
        </div>
        <div class="row my-3 d-flex justify-content-between mx-3">
          <div class="btn-group col-9">
            <input
              id="range"
              v-model="frame"
              type="range"
              class="form-range"
              min="0"
              :max="current_meteo_images.length - 1"
              step="1"
            >
          </div>
          <div
            class="btn-group col-2"
            role="group"
          >
            <button
              type="button"
              class="btn btn-sm btn-outline-primary"
              :disabled="started"
              @click="start()"
            >
              <img
                src="~bootstrap-icons/icons/play-fill.svg"
                alt="play icon"
                width="18"
                height="18"
              >
            </button>
            <button
              type="button"
              class="btn btn-sm btn-outline-warning"
              :disabled="!started"
              :class="{active: paused}"
              @click="togglePause()"
            >
              <img
                src="~bootstrap-icons/icons/pause-fill.svg"
                alt="pause icon"
                width="18"
                height="18"
              >
            </button>
            <button
              type="button"
              class="btn btn-sm btn-outline-danger"
              :disabled="!started"
              @click="stop()"
            >
              <img
                src="~bootstrap-icons/icons/stop-fill.svg"
                alt="redo icon"
                width="18"
                height="18"
              >
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MeteoModal',
  props: {
    selectedVenue:  {
      type: Number,
      default: null
    },
    levels: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      // reactive properties
      meteo: "temp",
      frame: 0,
      started: false,
      paused: false,
      timeoutID: null,
      delay: 1000 // ms between frames
    }
  },
  computed: {
    current_meteo_images() {
      return this.meteo_images[this.meteo].slice().sort()
    },
    base_data_url () {
      return import.meta.env.VITE_BASE_DATA_URL || ""
    },
    meteo_images () {
      const base_url = this.base_data_url ? this.base_data_url + "/sc05_intranet/public/aria/images/meteo" : "/aria"
      return {
        "prec": [
          base_url + "/ICO2I0020_00_NWI_prec_06.png",
          base_url + "/ICO2I0020_00_NWI_prec_12.png",
          base_url + "/ICO2I0020_00_NWI_prec_18.png",
          base_url + "/ICO2I0020_00_NWI_prec_24.png",
          base_url + "/ICO2I0020_00_NWI_prec_30.png",
          base_url + "/ICO2I0020_00_NWI_prec_36.png",
          base_url + "/ICO2I0020_00_NWI_prec_42.png",
          base_url + "/ICO2I0020_00_NWI_prec_48.png",
          base_url + "/ICO2I0020_00_NWI_prec_54.png",
          base_url + "/ICO2I0020_00_NWI_prec_60.png",
          base_url + "/ICO2I0020_00_NWI_prec_66.png",
          base_url + "/ICO2I0020_00_NWI_prec_72.png"
        ],
        "temp": [
          base_url + "/ICO2I0020_00_NWI_Temp_700_03.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_06.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_09.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_12.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_15.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_18.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_21.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_24.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_27.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_30.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_33.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_36.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_39.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_42.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_45.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_48.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_51.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_54.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_57.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_60.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_63.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_66.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_69.png",
          base_url + "/ICO2I0020_00_NWI_Temp_700_72.png",
        ],
        "tma700": [
          base_url + "/ICO2I0020_00_NWI_TMA_700_03.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_06.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_09.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_12.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_15.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_18.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_21.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_24.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_27.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_30.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_33.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_36.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_39.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_42.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_45.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_48.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_51.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_54.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_57.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_60.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_63.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_66.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_69.png",
          base_url + "/ICO2I0020_00_NWI_TMA_700_72.png"
        ],
        "tma850": [
          base_url + "/ICO2I0020_00_NWI_TMA_850_03.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_06.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_09.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_12.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_15.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_18.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_21.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_24.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_27.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_30.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_33.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_36.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_39.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_42.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_45.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_48.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_51.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_54.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_57.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_60.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_63.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_66.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_69.png",
          base_url + "/ICO2I0020_00_NWI_TMA_850_72.png",
        ],
        "totclo": [
          base_url + "/ICO2I0020_00_NWI_totclo_06.png",
          base_url + "/ICO2I0020_00_NWI_totclo_12.png",
          base_url + "/ICO2I0020_00_NWI_totclo_18.png",
          base_url + "/ICO2I0020_00_NWI_totclo_24.png",
          base_url + "/ICO2I0020_00_NWI_totclo_30.png",
          base_url + "/ICO2I0020_00_NWI_totclo_36.png",
          base_url + "/ICO2I0020_00_NWI_totclo_42.png",
          base_url + "/ICO2I0020_00_NWI_totclo_48.png",
          base_url + "/ICO2I0020_00_NWI_totclo_54.png",
          base_url + "/ICO2I0020_00_NWI_totclo_60.png",
          base_url + "/ICO2I0020_00_NWI_totclo_66.png",
          base_url + "/ICO2I0020_00_NWI_totclo_72.png",
        ],
        "wind700": [
          base_url + "/ICO2I0020_00_NWI_Wind_700_03.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_06.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_09.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_12.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_15.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_18.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_21.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_24.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_27.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_30.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_33.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_36.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_39.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_42.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_45.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_48.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_51.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_54.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_57.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_60.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_63.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_66.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_69.png",
          base_url + "/ICO2I0020_00_NWI_Wind_700_72.png"
        ],
        "wind850": [
          base_url + "/ICO2I0020_00_NWI_Wind_850_03.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_06.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_09.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_12.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_15.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_18.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_21.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_24.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_27.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_30.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_33.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_36.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_39.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_42.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_45.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_48.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_51.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_54.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_57.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_60.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_63.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_66.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_69.png",
          base_url + "/ICO2I0020_00_NWI_Wind_850_72.png"
        ],
        "wind950": [
          base_url + "/ICO2I0020_00_NWI_Wind_950_03.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_06.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_09.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_12.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_15.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_18.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_21.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_24.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_27.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_30.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_33.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_36.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_39.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_42.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_45.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_48.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_51.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_54.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_57.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_60.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_63.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_66.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_69.png",
          base_url + "/ICO2I0020_00_NWI_Wind_950_72.png",
        ]
      }
    }
  },
  methods: {
    start() {
      this.stop()
      this.started = true
      this.paused = false
      this.frame = 0
      this.timeoutID = window.setTimeout(this.step, this.delay)
    },
    togglePause() {
      this.paused = !this.paused
    },
    step() {
      if (!this.paused) {
        this.frame = (this.frame + 1) % this.current_meteo_images.length
      }
      this.timeoutID = window.setTimeout(this.step, this.delay)
    },
    stop() {
      this.started = false
      this.paused = false
      if (this.timeoutID) {
        window.clearTimeout(this.timeoutID)
        this.timeoutID = null
      }
    }

  }
}

</script>
