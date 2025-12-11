// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="row mt-3">
    <div
      v-if="!readonly"
      class="col"
    >
      <button
        class="btn btn-outline-primary"
        @click="calculateFirstGuess(timelayout, 'PLUV')"
      >
        <img
          src="~bootstrap-icons/icons/calculator.svg"
          alt="PDF icon"
          width="18"
          height="18"
        > Calcola First Guess
      </button>
    </div>
    
    <div
      class="row"
    >
      <div class="col-3">
        <MapSum
          :maxscadenza="maxscadenza"
          :sumpluv="bollettino[timelayout]['PLUV']"
          :valuesvalidity="valuesvalidity"
          :idaggregazione="idaggregazione"
          :readonly="readonly"
          :show-both="false"
          :title="'Compila'"
          @set-measure="setMeasure"
        />
      </div>
      <div
        v-if="detailModels[0] !== ''"
        class="col-3"
      >
        <MapSum
          :maxscadenza="maxscadenza"
          :sumpluv="sumpluv[0]"
          :valuesvalidity="{}"
          :idaggregazione="idaggregazione"
          :readonly="true"
          :show-both="true"
          :title="titles[0] + ' --- ' + titledata"
          @set-measure="setMeasure"
        />
      </div>
      <div
        v-if="sumpluv[1]"
        class="col-3"
      >
        <MapSum
          :maxscadenza="maxscadenza"
          :sumpluv="sumpluv[1]"
          :valuesvalidity="{}"
          :idaggregazione="idaggregazione"
          :readonly="true"
          :show-both="true"
          :title="titles[1] + ' --- ' + titledata"
          @set-measure="setMeasure"
        />
      </div>
      <div
        v-if="sumpluv[2]"
        class="col-3"
      >
        <MapSum
          :maxscadenza="maxscadenza"
          :sumpluv="sumpluv[2]"
          :valuesvalidity="{}"
          :idaggregazione="idaggregazione"
          :readonly="true"
          :show-both="true"
          :title="titles[2] + ' --- ' + titledata"
          @set-measure="setMeasure"
        />
      </div>
    </div>
  </div>
</template>

<script>
import MapSum from './MapSum.vue'

export default {
  name: 'ScadenzeDodici',
  components: {
    MapSum
  },
  props: {
    bollettino:  {
      type: Object,
      default: null
    },
    dataEmissione: {
      type: String,
      default: null
    },
    timelayout: {
      type: String,
      default: null
    },
    idaggregazione: {
      type: String,
      default: null
    },
    readonly:  {
      type: Boolean,
      default: true
    },
    detailModels: {
      type: Array,
      default: () => { return [] }
    },
    timelayoutset:  {
      type: Object,
      default: null
    },
  },
  emits: ['setMeasure', 'calculateFirstGuess'],
  data () {
    return {
      titledata: '',
      titles: []
    }
  },
  computed: {
    maxscadenza () {
      let tldict = {
        '48': '2',
        '64': '4',
        '66': '6',
      }
      let scadenzaoffset = tldict[Object.keys(this.timelayoutset)[0]]
      let maxpluv = JSON.parse(JSON.stringify(this.sumpluv[0][this.idaggregazione]))
      let maxscadenza = JSON.parse(JSON.stringify(this.sumpluv[0][this.idaggregazione]))
      maxscadenza.forEach(e => e.numeric_value = scadenzaoffset)
      for(let i=0; i<this.sumpluv[0][this.idaggregazione].length; i++){
        let j=0
        this.sumpluv.forEach(addpluv => {
          if(maxpluv[i].numeric_value < addpluv[this.idaggregazione].find(e => e.id_allertamento === maxpluv[i].id_allertamento).numeric_value){
            maxpluv[i].numeric_value = addpluv[this.idaggregazione].find(e => e.id_allertamento === maxpluv[i].id_allertamento).numeric_value
            maxscadenza.find(e => e.id_allertamento === maxpluv[i].id_allertamento).numeric_value = parseInt(scadenzaoffset)+j
          }
          j++
        })
      }
      if(this.idaggregazione === '126'){
        return { '126': maxscadenza}
        }else{
        return { '127': maxscadenza}
      }
    },
    sumpluv () {
      let sumpluv = []
      for(const timelayout in this.timelayoutset){
        let addpluv = JSON.parse(JSON.stringify(this.bollettino[this.timelayoutset[timelayout][0]]["PLUV"]['125']))
        for(let i=1; i<this.timelayoutset[timelayout].length; i++){
          for(let j=0; j<addpluv.length; j++){           
            addpluv[j].numeric_value += this.bollettino[this.timelayoutset[timelayout][i]]["PLUV"]['125'].find(e => e.id_allertamento === addpluv[j].id_allertamento).numeric_value
          }
        }
        if(this.idaggregazione === '126')
          sumpluv.push({ '126': addpluv})
        else
          sumpluv.push({ '127': addpluv})
      }
      return sumpluv
    },
    maxpluv (){
      let maxpluv = JSON.parse(JSON.stringify(this.sumpluv[0][this.idaggregazione]))
      for(let i=0; i<this.sumpluv[0][this.idaggregazione].length; i++){ 
        this.sumpluv.forEach(addpluv => {
          if(maxpluv[i].numeric_value < addpluv[this.idaggregazione].find(e => e.id_allertamento === maxpluv[i].id_allertamento).numeric_value){
            maxpluv[i].numeric_value = addpluv[this.idaggregazione].find(e => e.id_allertamento === maxpluv[i].id_allertamento).numeric_value 
          }
        })
      }
      return maxpluv
    },
    valuesvalidity (){
      let alltl = []
      for(const tlh in this.timelayoutset){
        this.timelayoutset[tlh].forEach(tl => {
          if(!alltl.find(mytl => mytl === tl)){
            alltl.push(tl)
          }
        })
      }

      let valuesvalidity = {}
      
      this.bollettino[this.timelayout]["PLUV"][this.idaggregazione].forEach(data => {
        valuesvalidity[data.id_allertamento] = false
        alltl.forEach(tl => {
          if(data.numeric_value < this.bollettino[tl]["PLUV"]["125"].find(e => e.id_allertamento === data.id_allertamento).numeric_value){
            valuesvalidity[data.id_allertamento] = true
          }
        })

        if(this.idaggregazione === "127" && data.numeric_value < this.bollettino["66"]["PLUV"]["126"].find(e => e.id_allertamento === data.id_allertamento).numeric_value){
          valuesvalidity[data.id_allertamento] = true
        }
      })
      
      return valuesvalidity
    }
  },
  watch: {

  },
  mounted() {
    const months = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
    "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
    var date = new Date(this.dataEmissione)
    if(this.timelayout === '66'){
      date.setDate(date.getDate()+1)
    }
    const dateDay = date.getDate()
    const dateMonth = date.getMonth()
    this.titledata = `${dateDay}-${months[dateMonth]}`
    
    let r1 = 0
    let r2 = 12
    if(this.timelayout === '48'){
      this.titles.push((r1+12) + ' - ' + (r2+12))
    }else{
      if(this.timelayoutset["65"]){
        let offset = 0
        for(let i = 0; i<3; i ++){
          this.titles.push((r1+offset) + ' - ' + (r2+offset))
          offset += 6
        }
        
      }else{
        this.titles.push((r1) + ' - ' + (r2+12))
      }
    }
  },
  methods: {
    setMeasure(data) {
      this.$emit('setMeasure', data)
    },
    calculateFirstGuess(timelayout, parameter){
     this.$emit('calculateFirstGuess', timelayout, parameter, this.idaggregazione, this.maxpluv)
    },
  }
}
</script>