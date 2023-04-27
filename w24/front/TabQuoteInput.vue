// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <input
    :tabindex="tabindex"
    class="form-control"
    type="number"
    step="100"
    :disabled="readonly"
    :value="roundedValue"
    @change="setNeve()"
  >
</template>

<script>
export default {
  name: 'TabQuoteInput',
  props: {
    readonly:  {
      type: Boolean,
      default: true
    },
    measure:  {
      type: String,
      default: null
    },
    refresher:  {
      type: Number,
      default: null
    },
    tabindex:  {
      type: Number,
      default: null
    },
    idw24data: {
      type: Number,
      default: null
    },
  },
  emits: ['setNeve'],
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
    setNeve() {
        let value = parseInt(event.target.value)
        if(value % 100 >= 50){
            value = 100 * Math.ceil(value / 100);
        }else{
            value = 100 * Math.floor(value / 100);
        }

        if(value > 0 && value < 6000){
            this.$emit('setNeve', this.idw24data, value)
        }else if(value > 6000){
            this.$emit('setNeve', this.idw24data, 6000)
        }else if(value < 0){
            this.$emit('setNeve', this.idw24data, 0)
        }

    },
  }

}
</script>
