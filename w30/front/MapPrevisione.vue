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
        <div v-if="values">
          <div
            v-if="maxView"
            class="btn-group"
          >
            <span
              style="width: 7em; font-size: 50%"
              class="badge bg-secondary text-wrap text-break"
            >{{ pqaaMeasures['900'].find(e => e.id_allertamento === pos.zone).byModel }}</span>
            <span
              style="width: 7em; font-size: 50%"
              class="badge bg-secondary text-wrap text-break"
            >{{ pqaaMeasures['125'].find(e => e.id_allertamento === pos.zone).byModel }}</span>
          </div>
          <input
            v-model="values[pos.zone]['900']" 
            data-bs-toggle="tooltip" 
            data-bs-placement="top"
            title="Medie"
            :disabled="readonly || timelayout === '43' || timelayout === '44'"
            type="Number"
            style="height: 1.5em; width: 2em; color: #0000ff; font-size: 26px; background-color: white;"
            :style="!(readonly || timelayout === '43' || timelayout === '44')
              && (values[pos.zone]['900'] < 0 
                || values[pos.zone]['900'] === null 
                || isNaN(values[pos.zone]['900'])) ? 'border: #ff0000; border:5px solid #ff0000;' : 'border: #0000ff; border:1px solid #0000ff;' + (maxView ? 'margin-left: 8px;' : '')"
            :tabindex="tabindex + pos.index"
            @change="setMeasure(pos.zone, '900')"
          >
          <input
            v-model="values[pos.zone]['125']" 
            data-bs-toggle="tooltip" 
            data-bs-placement="top"
            title="Massime"
            :disabled="readonly || timelayout === '43' || timelayout === '44'"
            type="Number"
            style="height: 1.5em; width: 2em; color: #ff0000; font-size: 26px; background-color: white;"
            :style="!(readonly || timelayout === '43' || timelayout === '44')
              && (values[pos.zone]['125'] < 0 
                || values[pos.zone]['125'] === null
                || values[pos.zone]['125'] < values[pos.zone]['900']
                || isNaN(values[pos.zone]['125'])) ? 'border: #ff0000; border:5px solid #ff0000;' : 'border: #ff0000; border:1px solid #ff0000;'"
            :tabindex="tabindex + pos.index"
            @change="setMeasure(pos.zone, '125')"
          >
        </div>
      </foreignObject>
    </svg> 
  </div>
</template>

<script>

export default {
  name: 'MapPrevisione',
  props: {
    pqaaMeasures:  {
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
  emits: ['setMeasure', 'toggleView'],
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
        x: 20,
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
        x: 220,
        y: 420,
        zone: "Piem-G",
        index: 7, 
      },
      {
        x: 315,
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
        x: 110,
        y: 430,
        zone: "Piem-M",
        index: 11,
      },
      {
        x: 60,
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
    }
  },
  computed: {
    values () {
      let values = {}
      for(const aggregazione in this.pqaaMeasures){
          for(const value in this.pqaaMeasures[aggregazione]){
          if(this.pqaaMeasures[aggregazione][value].id_allertamento in values){
            values[this.pqaaMeasures[aggregazione][value].id_allertamento][aggregazione] = this.pqaaMeasures[aggregazione][value].numeric_value
          }else{
            let obj = {}
            obj[aggregazione] = this.pqaaMeasures[aggregazione][value].numeric_value
            values[this.pqaaMeasures[aggregazione][value].id_allertamento] = obj
          }
        }
      }
      return values
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
    setMeasure(id_allertamento, id_aggregazione) {
      const data = this.pqaaMeasures[id_aggregazione].find(e => e.id_allertamento === id_allertamento)
      let payload = {
        "new_value": parseInt(event.target.value),
        "id_allertamento": data.id_allertamento,
        "id_aggregazione": data.id_aggregazione,
        "id_time_layouts": data.id_time_layouts,
        "id_parametro": data.id_parametro
      }
      this.$emit('setMeasure', payload)
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