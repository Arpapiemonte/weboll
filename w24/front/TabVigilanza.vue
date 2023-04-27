// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    :id="`pills-${id}`"
    class="tab-pane fade"
    :class="{show: active, active: active}"
    role="tabpanel"
    :aria-labelledby="`pills-${id}-tab`"
  >
    <div class="row">
      <div class="col-xxl-9 col-md-12 mb-3">
        <nav
          class="navbar justify-content-center sticky-top bg-light border-bottom"
          style="top: 88px;"
        >
          <ul class="nav">
            <li
              class="nav-item px-1"
              @click="goto(`pioggia-${id}`)"
            >
              <a class="nav-link"> Pioggia </a>
            </li>
            <li
              class="nav-item px-1"
              @click="goto(`neve-${id}`)"
            >
              <a class="nav-link"> Neve </a>
            </li>
          </ul>
        </nav>
        <div
          :id="`pioggia-${id}`"
        >
          <h3>Pioggia</h3>
          <TabellaPioggia
            :data="data[timeLayouts[0]]"
            :timelayout="timeLayouts[0]"
            :readonly="readonly"
            :soglievento="soglievento"
            :tipoanomaliat="tipoanomaliat"
            @save-w24-data="saveW24Data"
          />
        </div> <!-- row -->
        <div
          :id="`neve-${id}`"
        >
          <h3>Neve</h3>
          <TabellaNeve
            :data="[timeLayouts[1] ? data[timeLayouts[1]] : null, timeLayouts[2] ? data[timeLayouts[2]] : null, data[timeLayouts[3]], data[timeLayouts[4]], data[timeLayouts[0]]]"
            :timelayout="timeLayouts[0]"
            :readonly="readonly"
            @save-w24-data="saveW24Data"
            @save-w24-value="saveW24Value"
          />
        </div> <!-- row -->
      </div>  <!--col-->
      <div class="col-xxl-3 col-md-12 mb-3">
        <div
          class="sticky-top pt-5"
          style="z-index: 0;"
        >
          <MapVigilanza 
            :vigilanza="data[timeLayouts[0]]"
            :quoteneve="[timeLayouts[1] ? data[timeLayouts[1]]['SNOW_LEV'] : null, timeLayouts[2] ? data[timeLayouts[2]]['SNOW_LEV'] : null, data[timeLayouts[3]]['SNOW_LEV'], data[timeLayouts[4]]['SNOW_LEV']]"
            :pluv="[timeLayouts[1] ? data[timeLayouts[1]]['PLUV'] : null, timeLayouts[2] ? data[timeLayouts[2]]['PLUV'] : null, data[timeLayouts[3]]['PLUV'], data[timeLayouts[4]]['PLUV']]"  
            :timelayout="timeLayouts[0]"
          />
        </div>
      </div> <!-- col -->
    </div> <!-- row -->
  </div>
</template>
<script>
import MapVigilanza from './MapVigilanza.vue'
import TabellaNeve from './TabellaNeve.vue'
import TabellaPioggia from './TabellaPioggia.vue'

export default {
  name: 'TabVigilanza',
  components: {
    MapVigilanza,
    TabellaNeve,
    TabellaPioggia
  },
  props: {
    data: {
      type: Object,
      default: () => { return {} }
    },
    timeLayouts: {
      type: Array,
      default: () => { return [] }
    },
    soglievento: {
      type: Object,
      default: () => { return {} }
    },
    id: {
      type: String,
      default: ''
    },
    tipoanomaliat: {
      type: String,
      default: ''
    },
    active: {
      type: Boolean,
      default: false
    },
    readonly: {
      type: Boolean,
      default: true
    },
  },
  emits: ['saveW24Data', 'saveW24Value'],
  methods: {
    goto(id) {
      const element = document.getElementById(id)
      element.scrollIntoView({ behavior: "smooth" })
    },
    saveW24Data(id_w24_data, value) {
      console.log(`TabVigilanza.saveW24Data(${id_w24_data}, ${value})`)
      this.$emit('saveW24Data', id_w24_data, value)
    },
    saveW24Value(id_w24_data, value) {
      console.log(`TabVigilanza.saveW24Value(${id_w24_data}, ${value})`)
      this.$emit('saveW24Value', id_w24_data, value)
    },
  }
}
</script>
