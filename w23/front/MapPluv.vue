// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <!-- <code>{{ JSON.stringify(soglie) }}</code> -->
  <!-- {{ counts }} {{ Object.keys(counts).length }} -->
  <div
    v-if="Object.keys(counts).length > 0"
    class="progress"
  >
    <div
      class="progress-bar bg-success"
      role="progressbar"
      :style="'width: ' + counts.observations + '%'"
      :aria-valuenow="counts.observations"
      :title="'Osservazioni: ' + (counts.observations).toFixed() + '%'"
      aria-valuemin="0"
      aria-valuemax="100"
    />
    <div
      class="progress-bar bg-danger"
      role="progressbar"
      :style="'width: ' + counts.forecasts + '%'"
      :aria-valuenow="counts.forecasts"
      :title="'Previsioni: ' + (counts.forecasts).toFixed() + '%'"
      aria-valuemin="0"
      aria-valuemax="100"
    />
  </div>
  
  <svg
    viewBox="0 0 422.79207 587.44613"
    class="mt-3"
    width="100%"
    height="100%"
  >
    <template
      v-for="pos in inputsPosition"
      :key="pos.area"
    >
      <use
        :class="activeClasses(pos.area, values ? values[pos.area] : null)"
        :href="'#' + pos.area"
      >
        <title>{{ popover[pos.area] }}</title>
      </use>
      <text
        v-if="values && pos.area in values"
        :x="pos.x+15"
        :y="pos.y+30"
        :width="52"
        :height="38"
        text-anchor="middle"
      >
        <title>{{ popover[pos.area] }}</title>
        <tspan
          v-if="!isNaN(values[pos.area])"
          style="font-size: 40px;user-select: none; text-align: center;"
        >
          {{ Number(values[pos.area]).toFixed() }}
        </tspan>
        <tspan
          v-if="isNaN(values[pos.area])"
          style="font-size: 40px;user-select: none; text-align: center;"
        >
          N.D.
        </tspan>
      </text>
      <text
        v-else
        :x="pos.x+15"
        :y="pos.y+30"
        :width="52"
        :height="38"
        text-anchor="middle"
      >
        <tspan
          style="font-size: 40px;user-select: none; text-align: center;"
        >
          N.D.
        </tspan>
      </text>
    </template>
  </svg> 
</template>

<script>
export default {
  name: 'MapPluv',
  props: {
    values:  {
      type: Object,
      default: null
    },
    soglie: {
      type: Object,
      default: () => { return {} }
    },
    classes: {
      type: Array,
      default: () => []
    },
    counts: {
      type: Object,
      default: () => { return {} }
    },
  },
  data () {
    // non reactive data
    this.inputsPosition = [
      {
        x: 260,
        y: 100,
        area: "Piem-A" 
      },
      {
        x: 220,
        y: 180, 
        area: "Piem-B"
      },
      {
        x: 90,
        y: 280, 
        area: "Piem-C"
      },
      {
        x: 30,
        y: 360, 
        area: "Piem-D"
      },
      {
        x: 60,
        y: 490,
        area: "Piem-E"
      },
      {
        x: 180,
        y: 510,
        area: "Piem-F"
      },
      {
        x: 270,
        y: 420,
        area: "Piem-G"
      },
      {
        x: 350,
        y: 380,
        area: "Piem-H"
      },
      {
        x: 240,
        y: 270, 
        area: "Piem-I"
      },
      {
        x: 160,
        y: 340, 
        area: "Piem-L"
      },     
      {
        x: 130,
        y: 430,
        area: "Piem-M"
      },
      {
        x: 120,
        y: 180,
        area: "Piem-V"
      },
    ]
    return { }
  },
  computed: {
    popover() {
      let po = {}
      this.inputsPosition.forEach(pos => {
        po[pos.area] = `Area: ${pos.area}\n`
        if (this.values && pos.area in this.values) {
          po[pos.area] += `Valore: ${ Number(this.values[pos.area]).toFixed() }\n`
        }
        if (pos.area in this.soglie) {
          po[pos.area] += `Soglie: ${ this.soglie[pos.area].map(soglia => Number(soglia).toFixed()) }`
        }
      })
      return po
    }
  },
  methods: {
    activeClasses(area, value) {
      const factor = 1 // set this to 200 to see some colors when there is little or no precipitations
      if (value && this.soglie && area in this.soglie) {
        const cs = { none: true }
        if (!isNaN(value))
          cs["none"] = value < this.soglie[area][0] / factor
        this.classes.forEach((c, i) => {
          cs[c] = value >= this.soglie[area][i] / factor
        })
        // console.log(`activeClasses(${area}, ${value}) = ${JSON.stringify(cs)}`)
        return cs
      } else {
        // console.log(`this.soglie = ${JSON.stringify(this.soglie)}`)
        return { none: true }
      }
    }
  }
}
</script>

<style scoped>
  .none {fill: white;}
  .pre_all {fill: #dddddd;}
  .all_0 {fill: #6EBB00;}
  .all_1 {fill: #FFFF00;}
  .all_2 {fill: #FFA500;}
  .all_3 {fill: #FF0000;}
  .all_4 {fill: #ffffff;}
</style>

<style>
  .venues {fill:#00000000;stroke:#666;stroke-width:1;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;}
  input[type="Number"] {
    appearance: textfield;
  }
</style>