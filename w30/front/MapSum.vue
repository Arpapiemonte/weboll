// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="row mt-5">
    <h4>
      <div class="d-flex justify-content-center">
        <span
          class="col-8 badge bg-primary"
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
      />
      <foreignObject
        x="30"
        y="30"
        width="50"
        height="50"
      />
      <foreignObject
        v-for="pos in inputsPosition"
        :key="pos.id"
        :x="showBoth ? pos.x+30 : pos.x"
        :y="pos.y"
        :width="80"
        :height="80"
      >
        <div v-if="sumpluv">
          <!-- <input
            v-model="scadenzavalues[pos.zone][idaggregazione]"
            type="Number"
            style="height: 1.5em; width: 2em; color: #00ff00; border: #00ff00; border:1px solid #00ff00; font-size: 26px;"
            :hidden="showBoth"
            disabled
          > -->
          <input
            v-model="sumpluvvalues[pos.zone][idaggregazione]" 
            data-bs-toggle="tooltip" 
            data-bs-placement="top"
            title="Massimo"
            type="Number"
            style="height: 1.5em; width: 2em; color: #ff0000; font-size: 26px; background-color: white;"
            :style="sumpluvvalues[pos.zone][idaggregazione] < 0 
              || sumpluvvalues[pos.zone][idaggregazione] === null
              || isNaN(sumpluvvalues[pos.zone][idaggregazione]) 
              || valuesvalidity[pos.zone] ? 'border: #ff0000; border:5px solid #ff0000;' : 'border: #ff0000; border:1px solid #ff0000;'"
            :disabled="readonly"
            @change="setMeasure('sumpluv', pos.zone, idaggregazione)"
          >
        </div>
      </foreignObject>
    </svg> 
  </div>
</template>

<script>

export default {
  name: 'MapSum',
  props: {
    maxscadenza:  {
      type: Object,
      default: null
    },
    sumpluv:  {
      type: Object,
      default: null
    },
    valuesvalidity:  {
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
    idaggregazione: {
      type: String,
      default: null
    },
    title: {
      type: String,
      default: null
    },
    showBoth: {
      type: Boolean,
      default: null
    }
  },
  emits: ['setMeasure', 'toggleView'],
  data () {
    // non reactive data
    this.inputsPosition= [
      {
        x: 260,
        y: 100,
        zone: "Piem-A" 
      },
      {
        x: 220,
        y: 180, 
        zone: "Piem-B"
      },
      {
        x: 90,
        y: 280, 
        zone: "Piem-C"
      },
      {
        x: 30,
        y: 360, 
        zone: "Piem-D"
      },
      {
        x: 60,
        y: 490,
        zone: "Piem-E"
      },
      {
        x: 180,
        y: 510,
        zone: "Piem-F"
      },
      {
        x: 270,
        y: 420,
        zone: "Piem-G"
      },
      {
        x: 350,
        y: 380,
        zone: "Piem-H"
      },
      {
        x: 240,
        y: 270, 
        zone: "Piem-I"
      },
      {
        x: 160,
        y: 340, 
        zone: "Piem-L"
      },     
      {
        x: 130,
        y: 430,
        zone: "Piem-M"
      },
      {
        x: 120,
        y: 180,
        zone: "Piem-V"
      },
      {
        x: 320,
        y: 40,
        zone: "Piem-T"
      },
    ],
    this.rangelayouts= {
      43: "6",
      44: "12",
      45: "18",
      46: "0",
      60: "6",
      61: "12",
      62: "18",
      63: "0",
      94: "6",
      95: "12",
      96: "18",
      97: "0",
    },
    this.offsetlayouts= {
      43: 0,
      44: 0,
      45: 0,
      46: 0,
      60: 1,
      61: 1,
      62: 1,
      63: 1,
      94: 2,
      95: 2,
      96: 2,
      97: 2,
    }
    return {
      ready: false,
      selected: "-",
    }
  },
  computed: {
    scadenzavalues () {
      let scadenzavalues = {}
      for(const aggregazione in this.maxscadenza){
          for(const value in this.maxscadenza[aggregazione]){
          if(this.maxscadenza[aggregazione][value].id_allertamento in scadenzavalues){
            scadenzavalues[this.maxscadenza[aggregazione][value].id_allertamento][aggregazione] = this.maxscadenza[aggregazione][value].numeric_value
          }else{
            let obj = {}
            obj[aggregazione] = this.maxscadenza[aggregazione][value].numeric_value
            scadenzavalues[this.maxscadenza[aggregazione][value].id_allertamento] = obj
          }
        }
      }
      return scadenzavalues
    },
    sumpluvvalues () {
      let sumpluvvalues = {}
      for(const aggregazione in this.sumpluv){
          for(const value in this.sumpluv[aggregazione]){
          if(this.sumpluv[aggregazione][value].id_allertamento in sumpluvvalues){
            sumpluvvalues[this.sumpluv[aggregazione][value].id_allertamento][aggregazione] = this.sumpluv[aggregazione][value].numeric_value
          }else{
            let obj = {}
            obj[aggregazione] = this.sumpluv[aggregazione][value].numeric_value
            sumpluvvalues[this.sumpluv[aggregazione][value].id_allertamento] = obj
          }
        }
      }
      return sumpluvvalues
    },
  },
  mounted() {

  },
  methods: {
    setMeasure(parameterName, id_allertamento, id_aggregazione) {
      const data = this[parameterName][id_aggregazione].find(e => e.id_allertamento === id_allertamento)
      let payload = {
        "new_value": parseInt(event.target.value),
        "id_allertamento": data.id_allertamento,
        "id_aggregazione": data.id_aggregazione,
        "id_time_layouts": data.id_time_layouts,
        "id_parametro": data.id_parametro
      }
      this.$emit('setMeasure', payload)
    },
         
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