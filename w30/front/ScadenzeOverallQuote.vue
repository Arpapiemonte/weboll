// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="row mt-1">
    <div
      v-for="timeLayout in timelayouts6h"
      :key="timeLayout"
      class="col-3"
    >
      <MapQuote
        :snow-level="previsione['Bollettino'].w30_data[timeLayout]['SNOW_LEV']"
        :freeze-level="previsione['Bollettino'].w30_data[timeLayout]['FRZLVL']"
        :timelayout="timeLayout"
        :readonly="readonly"
        :show-button="true"
        :show-title="true"
        :data-emissione="dataEmissione"
        :isd0="true"
        @toggle-view="toggleView"
        @setmeasure-freeze-snow="setmeasureFreezeSnow"
      />
    </div>
  </div>
</template>

<script>
import MapQuote from './MapQuote.vue'

export default {
  name: 'ScadenzeOverallQuote',
  components: {
    MapQuote
  },
  props: {
    previsione:  {
      type: Object,
      default: null
    },
    readonly:  {
      type: Boolean,
      default: true
    },
    dataEmissione: {
      type: String,
      default: null
    },
    timelayouts6h: {
      type: Array,
      default: () => { return [] }
    },
  },
  emits: ['setmeasureFreezeSnow', 'toggleView'],
  data () {
    return {
      
    }
  },
  methods: {
    setmeasureFreezeSnow(stack) {
      this.$emit('setmeasureFreezeSnow', stack)     
    },
    toggleView(timelayout) {
      this.$emit('toggleView', timelayout, false)
    },
  }
}
</script>