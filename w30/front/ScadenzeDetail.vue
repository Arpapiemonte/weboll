// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    class="row sticky-top py-1"
    style="background-color: #f8f9fa;"
  > 
    <div class="col">
      <button
        class="btn btn-outline-primary"
        @click="toggleView()"
      >
        <img
          src="~bootstrap-icons/icons/zoom-out.svg"
          alt="PDF icon"
          width="18"
          height="18"
        > Torna al Bollettino
      </button>
    </div>
    <div
      class="col w-auto"
      role="group"
    > 
      <select
        :value="detailModels[0]"
        class="form-select"
        aria-label="Default select example"
        @change="$emit('changeModel', 0, $event.target.value)"
      >
        <option
          value=""
          selected="true"
          disabled="disabled"
        >
          Seleziona il primo Modello
        </option>
        <option
          v-for="model in availableModels"
          :key="model"
          :value="model"
        >
          {{ model }}
        </option>
      </select>
    </div>
    <div
      class="col w-auto"
      role="group"
    > 
      <select
        :value="detailModels[1]"
        class="form-select"
        aria-label="Default select example"
        :disabled="detailModels[0] === ''"
        @change="$emit('changeModel', 1, $event.target.value)"
      >
        <option
          value=""
          selected="true"
          disabled="disabled"
        >
          Seleziona il secondo Modello
        </option>
        <option
          v-for="model in availableModels"
          :key="model"
          :value="model"
        >
          {{ model }}
        </option>
      </select>
    </div>
    <div
      class="col w-auto"
      role="group"
    >
      <select
        :value="detailModels[2]"
        class="form-select"
        aria-label="Default select example"
        :disabled="detailModels[1] === ''"
        @change="$emit('changeModel', 2, $event.target.value)"
      >
        <option
          value=""
          selected="true"
          disabled="disabled"
        >
          Seleziona il terzo Modello
        </option>
        <option
          v-for="model in availableModels"
          :key="model"
          :value="model"
        >
          {{ model }}
        </option>
      </select>
    </div>
  </div>
  <div class="row mt-3">
    <div
      v-for="timeLayout in timelayouts6h"
      :id="timeLayout"
      :key="timeLayout"
      class="row"
    >
      <div class="col-3">
        <MapPrevisione
          :pqaa-measures="previsione['Bollettino'].w30_data[timeLayout]['PLUV']"
          :timelayout="timeLayout"
          :readonly="readonly"
          :show-button="false"
          :show-title="true"
          :max-view="false"
          :data-emissione="dataEmissione"
          :isd0="true"
          @set-measure="setMeasure"
        />
      </div>
      <div
        v-for="detailModel in detailModels"
        :id="detailModel"
        :key="detailModel"
        class="col-3"
      >
        <div
          v-if="detailModel !== ''"
        >
          <MapPrevisione
            :pqaa-measures="previsione[detailModel].w30_data[timeLayout]['PLUV']"
            :timelayout="timeLayout"
            :readonly="true"
            :show-button="false"
            :show-title="false"
            :max-view="detailModel === 'MAX'"
            :data-emissione="dataEmissione"
            :isd0="true"
            @set-measure="setMeasure"
          />
          <div
            v-if="!readonly"
            class="row d-flex justify-content-center mt-3 ms-5 me-5"
          > 
            <button
              class="btn btn-success"
              aria-label="Copia Valori"
              :disabled="timeLayout === '43' || timeLayout === '44' || detailModel === 'MAX'"
              @click="copyScadenza(timeLayout, 'PLUV', detailModel)"
            >
              Copia Valori Scadenza
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MapPrevisione from './MapPrevisione.vue'

export default {
  name: 'ScadenzeDetail',
  components: {
    MapPrevisione
  },
  props: {
    previsione:  {
      type: Object,
      default: null
    },
    readonly: {
      type: Boolean,
      default: false
    },
    dataEmissione: {
      type: String,
      default: null
    },
    detailModels: {
      type: Array,
      default: () => { return [] }
    },
    timelayouts6h: {
      type: Array,
      default: () => { return [] }
    },
  },
  emits: ['setMeasure', 'toggleView', 'changeModel', 'copyScadenza'],
  data () {
    return {

    }
  },
  computed: {
    availableModels () {
      let modelsArray = []
      for(const model in this.previsione){
        if(model !== "Bollettino" && model !== "last_update" && model !== "username"){
          modelsArray.push(model)
        }
      }
      return modelsArray
    },
  },
  methods: {
    setMeasure(data) {
      this.$emit('setMeasure', data)
    },
    toggleView(timelayout) {
      console.log("test")
      this.$emit('toggleView', timelayout, true)
    },
    copyScadenza(timelayout, parameter, modelSelected){
     this.$emit('copyScadenza', timelayout, parameter, modelSelected)
    },
  }
}
</script>