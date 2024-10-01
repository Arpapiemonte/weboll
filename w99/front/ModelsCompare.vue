// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="container-fluid">
    <div class="col-md-1 mb-3">
      <table class="table table-bordered">
        <tr>
          <td>
            <select
              @change="onChange"
            >
              <option
                v-for="(value, key) in stazioni_dict"
                :key="key"
                :value="key"
              >
                {{ value }}
              </option>
            </select>                     
          </td>
        </tr>  
      </table>
    </div>
    <div class="col-md-2 mb-3">
      <div class="form-check form-switch mt-4">
        <input
          id="viewMapCheck" 
          v-model="soloCapoluoghi" 
          class="form-check-input" 
          type="checkbox"
        >
        <label
          v-if="soloCapoluoghi"
          class="form-check-label" 
          for="viewMapCheck"
        >
          Stazioni relative ai capoluoghi
        </label>
        <label
          v-else
          class="form-check-label" 
          for="viewMapCheck"
        >
          Tutte le stazioni
        </label>
      </div>
    </div>
    <div class="d-flex justify-content-end">
      <button @click="resetZoom()">
        Reset Zoom
      </button>
    </div>
  </div>
  <div v-if="countfetch>4">
    <LineChart
      ref="chart"
      :data="chartData"
      :options="chartOptions"
      style="height:600px;width:100%"
    />
  </div>
</template>

<script lang="ts">
  export default {
    name: 'ModelsCompare',
    components: {
      LineChart
    }
  }
</script>

<script setup lang="ts">
import api from '../../src/api'
import { Ref, ref, onMounted, watch, computed } from 'vue'
import { useToast } from 'vue-toast-notification'
import { Line as LineChart } from 'vue-chartjs';
import 'chartjs-adapter-date-fns';
import zoomPlugin from 'chartjs-plugin-zoom';
import {it} from 'date-fns/locale';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale,
  zoomPlugin
)

const chart = ref("chart");

const toast = useToast()
const countfetch = ref(0)
const meteo_real_time = ref({})
const stazione_misura = ref({})
const stazione_misura_dict = ref({})

const run1 = ref()
const run2 = ref()
const forecast_values_run1 = ref({})
const forecast_values_run2 = ref({})
const lastmodels: Ref<LastModels> = ref({})
let soloCapoluoghi = ref(true)

const stazioniCapoluoghi = {
  '94061-001272-907': 'Torino Giardini Reali',
  '93447-001272-906': 'Torino Consolata',
  '90115-006003-900': 'Alessandria Lobbi',
  '94194-005005-900': 'Asti',
  '92566-002012-901': 'Biella',
  '92891-004078-901': 'Cuneo Camera di Commercio',
  '93254-004078-900': 'Cuneo Cascina Vecchia',
  '94193-003106-900': 'Novara',
  '90198-002158-900': 'Vercelli',
  '90641-003156-900': 'Pallanza'
}
const stazioni_dict = ref(stazioniCapoluoghi)
// default Giardini Reali
let stazDefault = '94061-001272-907'
let codStazMeteo = ref(stazDefault.split('-')[0])
let codIstatComune = ref(stazDefault.split('-')[1])
let progrPuntoCom = ref(stazDefault.split('-')[2])

function resetZoom(){
  chart.value.chart.resetZoom()
}

async function fetchMeteoRealTime () {
  const response = await fetch('/api/w99/meteo_real_time/?codice_istat_comune=' + codIstatComune.value + '&progr_punto_com=' + progrPuntoCom.value + '&id_parametro=TERMA', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchForecastValues (time) {
  console.log("TIME", time)
  const response = await fetch('/api/w99/forecast_values/?model_name=MULTMODEL&time_emiss='+time+'&id_parametro=TERMA&cod_staz_meteo='+codStazMeteo.value, {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchStazioneMisura () {
  const response = await fetch('/api/w99/stazione_misura/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchLastModels () {
  const response = await fetch('/api/w99/last_models/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchData () {
  fetchMeteoRealTime().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} dati osservati mancanti`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json() 
  }).then(data => {
    meteo_real_time.value = data
    countfetch.value = countfetch.value + 1
  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
  fetchStazioneMisura().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero dell'anagrafica stazioni`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json() 
  }).then(data => {
    stazione_misura.value = data
    stazione_misura_dict.value = rearrange(stazione_misura.value)
    countfetch.value = countfetch.value + 1
  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
  fetchLastModels().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero degli ultimi run disponibili`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json() 
  }).then(data => {
    lastmodels.value = data
    run1.value = data.filter(data => {
      return data.model_name === 'MULTMODEL'
    })[0]["time_emiss"]
    run2.value = data.filter(data => {
      return data.model_name === 'MULTMODEL'
    })[2]["time_emiss"]
    countfetch.value = countfetch.value + 1


    fetchForecastValues(run1.value).then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero dei dati previsti`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json() 
  }).then(data => {
    forecast_values_run1.value = data
    if (data.length == 0){
      toast.open(
        {
          message: `Dati previsti non presenti`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    countfetch.value = countfetch.value + 1
  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
  fetchForecastValues(run2.value).then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero dei dati previsti`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json() 
  }).then(data => {
    forecast_values_run2.value = data
    countfetch.value = countfetch.value + 1
  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })


  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
 
}

function rearrange(data: {}) {
  let value_data = {}
  
  Object.keys(data).forEach(function(key) {
    let chiave = data[key].cod_staz_meteo + "-" + data[key].codice_istat_comune + "-" + data[key].progr_punto_com
    value_data[chiave] = data[key].denominazione.substring(0,20)
  });
  return value_data
}

async function onChange(e: Event) {
  const target = e.target as HTMLInputElement
  var stazCod = target.value.split('-')
  codStazMeteo.value = parseInt(stazCod[0])
  codIstatComune.value = stazCod[1]
  progrPuntoCom.value = parseInt(stazCod[2])
  // codStazMeteo.value = parseInt(target.value)
  fetchData()
}

onMounted(async () => {
  fetchData()
})

const chartOptions = computed(() => {
  let result = {
    scales: {
      x: {
        type: "time",
        time: {
          unit: 'hour',
          displayFormats: {
            hour: 'dd/MM HH:mm'
          }
        }      
      },
      y: {
        position: "left",
        title: {
          display: true,
          text: "Temperatura °C"
        },
      }
    },
    // permette di mettere i valori nella stessa label
    interaction: {
      intersect: false,
      mode: 'index',
    },
    plugins: {
      zoom: {
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true
          },
          mode: 'xy',
        }
      },
      tooltip: {
        callbacks: {
        }
      }
    }
    
  }
  return result
})


const chartData = computed(() => {
  let result = {labels: [], datasets: []}
  let terma_ds = {label: 'Dato osservato', backgroundColor: '#f28f9c', borderColor: '#f28f9c', borderWidth: 1, yAxisID: 'y'}
  let model_ds = {label: 'Multimodel ' + run1.value.substring(1,5), backgroundColor: '#6495ED', borderColor: '#6495ED', yAxisID: 'y'}
  let model_ds_2 = {label: 'Multimodel ' + run2.value.substring(1,5), backgroundColor:'#3CB371', borderColor: '#3CB371', yAxisID: 'y'}
  for (const [key, value] of Object.entries(meteo_real_time.value)) {
    let data_ora = value.data + " " + value.ora
    if (result["labels"].indexOf(data_ora) == -1 )
      result["labels"].push(data_ora)
  }
  for (const [key, value] of Object.entries(forecast_values_run1.value)) {
    let data_ora = value.date_rif + " " + value.time_rif
    if (result["labels"].indexOf(data_ora) == -1 )
      result["labels"].push(data_ora)
  }
  for (const [key, value] of Object.entries(forecast_values_run2.value)) {
    let data_ora = value.date_rif + " " + value.time_rif
    if (result["labels"].indexOf(data_ora) == -1 )
      result["labels"].push(data_ora)
  }
  result["labels"].sort(function(a,b){
    return new Date(a) - new Date(b);
  });
  terma_ds["data"] = Array.apply(null, Array(result["labels"].length)).map(function () {})
  model_ds["data"] = Array.apply(null, Array(result["labels"].length)).map(function () {})
  model_ds_2["data"] = Array.apply(null, Array(result["labels"].length)).map(function () {})
  for (const [key, value] of Object.entries(meteo_real_time.value)) {
    let data_ora = value.data + " " + value.ora
    let index = result["labels"].indexOf(data_ora)
    terma_ds["data"][index] = value.valore_validato
  }
  for (const [key, value] of Object.entries(forecast_values_run1.value)) {
    let data_ora = value.date_rif + " " + value.time_rif
    let index = result["labels"].indexOf(data_ora)
    model_ds["data"][index] = value.value
  }
  for (const [key, value] of Object.entries(forecast_values_run2.value)) {
    let data_ora = value.date_rif + " " + value.time_rif
    let index = result["labels"].indexOf(data_ora)
    model_ds_2["data"][index] = value.value
  }
  result["datasets"].push(terma_ds)
  result["datasets"].push(model_ds)
  result["datasets"].push(model_ds_2)
  return result
})

watch(() => soloCapoluoghi.value, (new_value) => {
  if (new_value){
    console.log("new_value - true", new_value)
    stazioni_dict.value = stazioniCapoluoghi
  }else{
    console.log("new_value - false", new_value)
    fetchData()
    stazioni_dict.value = stazione_misura_dict.value
  }
})

</script>

<style scoped>

</style>