// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="row mt-1">
    <div
      v-for="(timeLayout) in timelayouts6h"
      :key="timeLayout"
      class="col-3"
    >
      <MapPrevisione
        :pqaa-measures="previsione['Bollettino'].w30_data[timeLayout]['PLUV']"
        :timelayout="timeLayout"
        :readonly="readonly"
        :show-button="true"
        :show-title="true"
        :data-emissione="dataEmissione"
        :isd0="true"
        @set-measure="setMeasure"
        @toggle-view="toggleView"
      />
    </div>
  </div>
</template>

<script>
import MapPrevisione from './MapPrevisione.vue'

export default {
  name: 'ScadenzeOverall',
  components: {
    MapPrevisione
  },
  props: {
    previsione:  {
      type: Object,
      default: null
    },
    dataEmissione: {
      type: String,
      default: null
    },
    readonly: {
      type: Boolean,
      default: false
    },
    timelayouts6h: {
      type: Array,
      default: () => { return [] }
    },
  },
  emits: ['setMeasure', 'toggleView'],
  data () {
    return {
      
    }
  },
  methods: {
    setMeasure(data) {
      this.$emit('setMeasure', data)
    },
    toggleView(timelayout) {
      this.$emit('toggleView', timelayout, false)
    },
  }
}
</script>