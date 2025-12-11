// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="row mt-5">
    <h4>
      <div class="d-flex justify-content-center">
        <span
          v-if="showTitle"
          class="badge bg-primary"
        >{{ title }}</span>
      </div>
    </h4>
    <svg
      viewBox="0 0 422.79207 587.44613"
      class="mt-3"
      width="422.79208"
      height="587.44613"
    > 
      <use
        href="#pqaaMap"
        :opacity="(timelayout === '43' || timelayout === '44') && showTitle ? 0.3 : 1"
      />
      <foreignObject
        x="30"
        y="30"
        width="50"
        height="50"
      >
        <button
          v-if="showButton && !readonly"
          class="btn btn-outline-primary nottoprint"
          @click="toggleView()"
        ><img
          src="~bootstrap-icons/icons/zoom-in.svg"
          alt="PDF icon"
          width="18"
          height="18"
        >
        </button>
      </foreignObject>
      <foreignObject
        v-for="pos in inputsPosition"
        :key="pos.id"
        :opacity="(timelayout === '43' || timelayout === '44') && showTitle ? 0.3 : 1"
        :x="pos.x"
        :y="maxView ? pos.y-15 : pos.y"
        :width="150"
        :height="maxView ? 80 : 60"
      >
        <div v-if="snowvalues">
          <QuoteInput
            :timelayout="timelayout"
            :readonly="readonly"
            :measure="freezevalues[pos.zone]['0']"
            :parametername="'freezeLevel'"
            :zone="pos.zone"
            :tabindex="tabindex + pos.index"
            :refresher="refresher"
            :stilebox="!(readonly || timelayout === '43' || timelayout === '44')
              && freezevalues[pos.zone]['0'] < 0 
              || isNaN(freezevalues[pos.zone]['0'])
              || freezevalues[pos.zone]['0'] === null ? 'border: #ff0000; border:5px solid #ff0000;' : 'color: #000000; border: #000000; border:1px solid #000000;'"
            @setmeasure-freeze-snow="setmeasureFreezeSnow"
          />
          <QuoteInput
            :timelayout="timelayout"
            :readonly="readonly"
            :measure="snowvalues[pos.zone]['0']"
            :parametername="'snowLevel'"
            :zone="pos.zone"
            :tabindex="tabindex + pos.index"
            :refresher="refresher"
            :stilebox="!(readonly || timelayout === '43' || timelayout === '44')
              && snowvalues[pos.zone]['0'] < 0 
              || isNaN(snowvalues[pos.zone]['0'])
              || snowvalues[pos.zone]['0'] === null 
              || snowvalues[pos.zone]['0'] > freezevalues[pos.zone]['0'] ? 'border: #ff0000; border:5px solid #ff0000;' : 'color: #0000ff; border: #0000ff; border:1px solid #0000ff;'"
            :parameter="'Quota Neve'"
            @setmeasure-freeze-snow="setmeasureFreezeSnow"
          />
        </div>
      </foreignObject>
    </svg> 
  </div>
</template>

<script>
import QuoteInput from './QuoteInput.vue'

export default {
  name: 'MapQuote',
  components: {
    QuoteInput
  },
  props: {
    snowLevel:  {
      type: Object,
      default: null
    },
    freezeLevel:  {
      type: Object,
      default: null
    },
    readonly:  {
      type: Boolean,
      default: true
    },
    timelayout: {
      type: String,
      default: null
    },
    dataEmissione: {
      type: String,
      default: null
    },
    showTitle: {
      type: Boolean,
      default: null
    },
    showButton: {
      type: Boolean,
      default: null
    },
    maxView: {
      type: Boolean,
      default: null
    },
    isd0: {
      type: Boolean,
      default: null
    },
  },
  emits: ['setmeasureFreezeSnow', 'toggleView'],
  data () {
    // non reactive data
    this.inputsPosition= [
      {
        x: 230,
        y: 100,
        zone: "Piem-A",
        index: 1, 
      },
      {
        x: 190,
        y: 180, 
        zone: "Piem-B",
        index: 2,
      },
      {
        x: 50,
        y: 280, 
        zone: "Piem-C",
        index: 3,
      },
      {
        x: 0,
        y: 360, 
        zone: "Piem-D",
        index: 4,
      },
      {
        x: 20,
        y: 490,
        zone: "Piem-E",
        index: 5,
      },
      {
        x: 150,
        y: 510,
        zone: "Piem-F",
        index: 6,
      },
      {
        x: 240,
        y: 420,
        zone: "Piem-G",
        index: 7,
      },
      {
        x: 300,
        y: 380,
        zone: "Piem-H",
        index: 8,
      },
      {
        x: 220,
        y: 270, 
        zone: "Piem-I",
        index: 9,
      },
      {
        x: 140,
        y: 340, 
        zone: "Piem-L",
        index: 10,
      },     
      {
        x: 90,
        y: 430,
        zone: "Piem-M",
        index: 11,
      },
      {
        x: 40,
        y: 180,
        zone: "Piem-V",
        index: 12,
      },
      {
        x: 300,
        y: 40,
        zone: "Piem-T",
        index: 13,
      },
    ],
    this.rangelayouts= {
      43: "06",
      44: "12",
      45: "18",
      46: "00",
      60: "06",
      61: "12",
      62: "18",
      63: "00",
      77: "06",
      78: "12",
      79: "18",
      80: "00",
    },
    this.offsetlayouts= {
      43: 0,
      44: 0,
      45: 0,
      46: 1,
      60: 1,
      61: 1,
      62: 1,
      63: 2,
      77: 2,
      78: 2,
      79: 2,
      80: 3,
    }
    return {
      ready: false,
      selected: "-",
      refresher: 0,
    }
  },
  computed: {
    snowvalues () {
      let snowvalues = {}
      for(const aggregazione in this.snowLevel){
          for(const value in this.snowLevel[aggregazione]){
          if(this.snowLevel[aggregazione][value].id_allertamento in snowvalues){
            snowvalues[this.snowLevel[aggregazione][value].id_allertamento][aggregazione] = this.snowLevel[aggregazione][value].numeric_value
          }else{
            let obj = {}
            obj[aggregazione] = this.snowLevel[aggregazione][value].numeric_value
            snowvalues[this.snowLevel[aggregazione][value].id_allertamento] = obj
          }
        }
      }
      return snowvalues
    },
    freezevalues () {
      let freezevalues = {}
      for(const aggregazione in this.freezeLevel){
          for(const value in this.freezeLevel[aggregazione]){
          if(this.freezeLevel[aggregazione][value].id_allertamento in freezevalues){
            freezevalues[this.freezeLevel[aggregazione][value].id_allertamento][aggregazione] = this.freezeLevel[aggregazione][value].numeric_value
          }else{
            let obj = {}
            obj[aggregazione] = this.freezeLevel[aggregazione][value].numeric_value
            freezevalues[this.freezeLevel[aggregazione][value].id_allertamento] = obj
          }
        }
      }
      return freezevalues
    },
    title () {
      const months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
      "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
      var date = new Date(this.dataEmissione)
      if(!this.isd0){
        date.setDate(date.getDate() + 1)
      }
      date.setDate(date.getDate() + this.offsetlayouts[this.timelayout])
      const dateDay = date.getDate()
      const dateMonth = date.getMonth()
      return `${dateDay}-${months[dateMonth]}  h:${this.rangelayouts[this.timelayout]}`
    },
    tabindex (){
      return parseInt(this.timelayout) * 100
    }
  },
  mounted() {

  },
  methods: {
    setmeasureFreezeSnow(parameterName, id_allertamento, roundedValue) {
      if(roundedValue > -1){
        let data = this[parameterName]['0'].find(e => e.id_allertamento === id_allertamento)
        let stack = []
        let payload = {
          "new_value": roundedValue,
          "id_allertamento": data.id_allertamento,
          "id_aggregazione": data.id_aggregazione,
          "id_time_layouts": data.id_time_layouts,
          "id_parametro": data.id_parametro
        }

        stack.push(payload)

        if(parameterName ===  'freezeLevel'){
          let snowvalue = roundedValue - 300
          if(roundedValue < 300){
            snowvalue = 0
          }
          let snowpayload = {
          "new_value": snowvalue,
          "id_allertamento": data.id_allertamento,
          "id_aggregazione": data.id_aggregazione,
          "id_time_layouts": data.id_time_layouts,
          "id_parametro": 'SNOW_LEV'
          }
          stack.push(snowpayload)
        }
        this.$emit('setmeasureFreezeSnow', stack)
      }
      this.forceUpdate()
    },
    forceUpdate(){
      this.refresher += 1
    },
    toggleView() {
      this.$emit('toggleView', this.timelayout)
    }
         
  }
}
</script>

<style>
  .venues {fill:#00000000;stroke:#666;stroke-width:1;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;}
  .venues .selected {fill:#555555}  
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  input[type="Number"] {
    appearance: textfield;
  }
</style>