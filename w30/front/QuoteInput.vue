// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <input
    :tabindex="tabindex"
    :value="roundedValue"
    data-bs-toggle="tooltip"
    data-bs-placement="top"
    :title="parameter"
    :disabled="readonly || timelayout === '43' || timelayout === '44'"
    type="number"
    step="100"
    style="height: 1.5em; width: 2.5em; font-size: 26px; background-color: white;"
    :style="stilebox"
    @change="setmeasure(roundedValue)"
  >
</template>

<script>

export default {
  name: 'QuoteInput',
  props: {
    timelayout: {
      type: String,
      default: null
    },
    readonly:  {
      type: Boolean,
      default: true
    },
    measure:  {
      type: Number,
      default: null
    },
    parametername:  {
      type: String,
      default: ''
    },
    zone:  {
      type: String,
      default: ''
    },
    stilebox:  {
      type: String,
      default: ''
    },
    refresher:  {
      type: Number,
      default: null
    },
    parameter:  {
      type: String,
      default: 'Zero Termico'
    },
    tabindex:  {
      type: Number,
      default: null
    },
  },
  emits: ['setmeasureFreezeSnow'],
  data () {
    return {

    }
  },
  computed: {
    roundedValue() {
      let value = this.measure
      if(value === null){
        value === null
      }else if(value % 100 >= 50){
        value = 100 * Math.ceil(value / 100);
      }else{
        value = 100 * Math.floor(value / 100);
      }
      return value
    },
  },
  methods: {
    setmeasure() {
        let value = parseInt(event.target.value)
        if(value % 100 >= 50){
            value = 100 * Math.ceil(value / 100);
        }else{
            value = 100 * Math.floor(value / 100);
        }
        this.$emit('setmeasureFreezeSnow', this.parametername, this.zone, value)
    },
  }

}
</script>
