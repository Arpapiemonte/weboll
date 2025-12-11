// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <modalNoteSelect 
    :readonly="readonly"
    :selectedarea="selectedarea"
    @save-w26-data="saveW26Data"
  />
  <div class="container-fluid">
    <div
      class="row justify-content-end sticky-top py-1"
      style="background-color: #f8f9fa;"
    >
      <!-- https://getbootstrap.com/docs/5.1/components/button-group/ -->
      <div
        class="btn-group w-auto"
        role="group"
        aria-label="Basic outlined example"
      >
        <a
          class="btn btn-outline-primary"
          :href="'/api/w26/pdf/' + bis.id_w26"
          target="_blank"
          role="button"
        >
          <img
            src="~bootstrap-icons/icons/file-earmark-pdf-fill.svg"
            alt="PDF icon"
            width="18"
            height="18"
          > PDF
        </a>
        <button
          v-if="bis.status === '0' && state.username"
          :disabled="actions.sending"
          type="button"
          class="btn btn-outline-success"
          @click="execute('send', false, 'Bollettino inviato')"
        >
          <span v-if="actions.sending">
            <span
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
            />
            Sto inviando il bollettino ...
          </span>
          <span v-else>
            <img
              src="~bootstrap-icons/icons/send-fill.svg"
              alt="unlock icon"
              width="18"
              height="18"
            > Invia
          </span>
        </button>
        <button
          v-if="bis.status === '1' && state.username && bis.data_emissione.substring(0, 10) === today"
          type="button"
          class="btn btn-outline-warning"
          @click="execute('reopen', true, 'Bollettino riaperto')"
        >
          <span v-if="actions.reopening">
            <span
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
            />
            Sto riaprendo il bollettino ...
          </span>
          <span v-else>
            <img
              src="~bootstrap-icons/icons/unlock-fill.svg"
              alt="unlock icon"
              width="18"
              height="18"
            > Riapri
          </span>
        </button>
        <button
          v-if="bis.status === '0' && state.username"
          type="button"
          class="btn btn-outline-danger"
          @click="remove()"
        >
          <img
            src="~bootstrap-icons/icons/trash-fill.svg"
            alt="unlock icon"
            width="18"
            height="18"
          > Elimina
        </button>
      </div>
    </div>

    <div class="row mb-3">
      <h1>Bollettino BIS {{ bis.numero_bollettino }}</h1>
      <!--
      <div
        class="alert alert-danger"
      >
        Ci sono dei campi incompleti
      </div>-->
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="bis.status === '1'">
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Inviato"
            >
          </span>
          <span v-else>
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Bozza"
            >
          </span>
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_emissione">Data emissione
          <input
            id="data_emissione"
            disabled
            class="form-control"
            name="data_emissione"
            type="text"
            :value="getDateFormatted(bis.data_emissione, false)"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_validita">Data scadenza
          <input
            id="data_validita"
            disabled
            class="form-control"
            name="data_validita"
            type="text"
            :value="getDateFormatted(bis.data_validita, false)"
          >
          <!--<Datepicker
            v-model="bis.data_validita"
            :disabled="readonly"
            :style="readonly ? '--dp-disabled-color: #e9ecef' : '--dp-background-color: white'"
            format="dd/MM/yyyy"
            auto-apply
            @update:model-value="saveW26(bis.data_validita, bis.id_w26, 'data_validita')"
          />-->
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="last_update">Ultima modifica
          <input
            id="last_update"
            disabled
            class="form-control"
            name="last_update"
            type="text"
            :value="getDateFormatted(bis.last_update)"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="username">Autore
          <input
            id="username"
            disabled
            class="form-control"
            name="username"
            type="text"
            :value="bis.username"
          >
        </label>
      </div>
      <div v-if="ready">
        <div class="d-flex justify-content-center">
          <div
            class="col-md-11 mb-3"
          >
            <div class="row">
              <div class="col-md-12 mb-3">
                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th
                        class="text-center"
                        colspan="2"
                      >
                        ANAGRAFICA
                      </th>
                      <th
                        class="text-center"
                        colspan="3"
                      >
                        LIVELLI
                      </th>
                      <th
                        class="text-center"
                        colspan="3"
                      >
                        PORTATE
                      </th>
                      <th
                        class="text-center"
                        colspan="1"
                      >
                        Note
                      </th>
                    </tr>
                    <tr>
                      <th scope="col">
                        Corso d'acqua
                      </th>
                      <th scope="col">
                        Localita
                      </th>
                      <th scope="col">
                        Hmin
                      </th>
                      <th scope="col">
                        Hmed
                      </th>
                      <th scope="col">
                        Hmax
                      </th>
                      <th scope="col">
                        Qmin
                      </th>
                      <th scope="col">
                        Qmed
                      </th>
                      <th scope="col">
                        Qmax
                      </th>
                      <th scope="col">
                        id_Note
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="area in bis.w26data_set"
                      :key="area.id_w26_data"
                    >
                      <th scope="row">
                        {{ area.id_w26_zone.corsoacqua }}
                      </th>
                      <th scope="row">
                        {{ area.id_w26_zone.localita }}
                      </th>
                      <td>
                        <input
                          id="hmin"
                          :readonly="readonly"
                          class="form-control"
                          :style="valuesValidity[area.id_w26_zone.id_w26_zone].hmin ? 'border: #FFBF00; border:5px solid #FFBF00;' : ''"
                          name="hmin"
                          type="text"
                          :value="area.hmin"
                          @change="saveW26Data($event.target.value, area.id_w26_data, 'hmin')"
                        >
                      </td>
                      <td>
                        <input
                          id="hmed"
                          :readonly="readonly"
                          class="form-control"
                          :style="valuesValidity[area.id_w26_zone.id_w26_zone].hmed ? 'border: #FFBF00; border:5px solid #FFBF00;' : ''"
                          name="hmed"
                          type="text"
                          :value="area.hmed"
                          @change="saveW26Data($event.target.value, area.id_w26_data, 'hmed')"
                        >
                      </td>
                      <td>
                        <input
                          id="hmax"
                          :readonly="readonly"
                          class="form-control"
                          :style="valuesValidity[area.id_w26_zone.id_w26_zone].hmax ? 'border: #FFBF00; border:5px solid #FFBF00;' : ''"
                          name="hmax"
                          type="text"
                          :value="area.hmax"
                          @change="saveW26Data($event.target.value, area.id_w26_data, 'hmax')"
                        >
                      </td>
                      <td>
                        <input
                          id="qmin"
                          :readonly="readonly"
                          class="form-control"
                          :style="valuesValidity[area.id_w26_zone.id_w26_zone].qmin ? 'border: #FFBF00; border:5px solid #FFBF00;' : ''"
                          name="qmin"
                          type="text"
                          :value="area.qmin"
                          @change="saveW26Data($event.target.value, area.id_w26_data, 'qmin')"
                        >
                      </td>
                      <td>
                        <input
                          id="qmed"
                          :readonly="readonly"
                          class="form-control"
                          :style="valuesValidity[area.id_w26_zone.id_w26_zone].qmed ? 'border: #FFBF00; border:5px solid #FFBF00;' : ''"
                          name="qmed"
                          type="text"
                          :value="area.qmed"
                          @change="saveW26Data($event.target.value, area.id_w26_data, 'qmed')"
                        >
                      </td>
                      <td>
                        <input
                          id="qmax"
                          :readonly="readonly"
                          class="form-control"
                          :style="valuesValidity[area.id_w26_zone.id_w26_zone].qmax ? 'border: #FFBF00; border:5px solid #FFBF00;' : ''"
                          name="qmax"
                          type="text"
                          :value="area.qmax"
                          @change="saveW26Data($event.target.value, area.id_w26_data, 'qmax')"
                        >
                      </td>
                      <td>
                        <div>
                          <div class="btn-group">
                            <input
                              id="idnota"
                              class="form-control"
                              name="idnota"
                              type="text"
                              :value="area.idnota"
                            >
                            <button
                              type="button"
                              :disabled="readonly"
                              class="btn btn-success"
                              @click="openNoteModal(area)"
                            >
                              <span>+</span>
                            </button>
                          </div>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import modalNoteSelect from './modalNoteSelect.vue'

  export default {
    name: 'BisBulletin',
    components: {
      modalNoteSelect
    }
  }
</script>

<script setup lang="ts">
import { Modal } from 'bootstrap'
import { Ref, ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vue-toast-notification'

import api from '../../src/api'
import store from '../../src/store'

import { components } from '../../src/types/weboll'

const router = useRouter()
const route = useRoute()
const toast = useToast()

type W26Full = components['schemas']['W26'] & { w26data_set: components['schemas']['W26Data'][] }
type W26Data = components['schemas']['W26Data']

// reactive properties
let bis_id = ref('')
let bis : Ref<W26Full> = ref({})
let yesterdaybis : Ref<W26Full> = ref({})
let state = ref(store.state)
let ready = ref(false)
let hasYesterday = ref(false)
let readonly = ref(true)
let actions = ref({
  sending: false,
  reopening: false,
})
let selectedarea : Ref<W26Data> = ref({})
let today = ref('')
const props = defineProps({
    id: {
        type: String,
        default: () => ''
    },
})
// TODO: CONVERT sending -> actions.sending
// let actions = ref({ sending: false })

const valuesValidity = computed(() => {
  const parametri = ["hmin", "hmed", "hmax", "qmin", "qmed", "qmax"]
  let valuesV = {}
  if(hasYesterday.value){
    bis.value.w26data_set.forEach(area => {
      const yesterdayArea = yesterdaybis.value.w26data_set.find(l => l.id_w26_zone.id_w26_zone === area.id_w26_zone.id_w26_zone)
      let areaValidity = {}
      parametri.forEach(p => {
        if(Math.abs(area[p] - yesterdayArea[p])/Math.abs(yesterdayArea[p])  >= 0.5){
          areaValidity[p] = true
        }else{
          areaValidity[p] = false
        }
      })
      valuesV[area.id_w26_zone.id_w26_zone] = areaValidity
    })
  }else{
    bis.value.w26data_set.forEach(area => {
      let areaValidity = {}
      parametri.forEach(p => {
        areaValidity[p] = false
      })
      valuesV[area.id_w26_zone.id_w26_zone] = areaValidity
    })
  }
  return valuesV
})

onMounted(() => {
  bis_id.value = props.id
  fetchData()
})

async function fetchData () {
  today.value = dateToString(new Date())
  ready.value = false
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  fetchBis(bis_id.value).then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero del bollettino`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(data => {
    bis.value = data
    // remove from w26_data record with id_w26_zone == null
    bis.value.w26data_set =  bis.value.w26data_set.filter(function(key) { return key.id_w26_zone !== null  })
    
    bis.value.w26data_set.sort((a, b) => a.id_w26_zone.numero - b.id_w26_zone.numero)
    readonly.value = (bis.value.status === '1' || bis.value.status === '2' || !state.value.username)

    const yesterday = new Date(new Date(bis.value.data_validita).setDate(new Date(bis.value.data_validita).getDate() - 1))
    const tomorrow = new Date(new Date(bis.value.data_validita).setDate(new Date(bis.value.data_validita).getDate()+1))

    const dataValiditaYesterday = dateToString(yesterday)
    const dataValiditaTomorrow = dateToString(tomorrow)

    fetchAllBis(dataValiditaYesterday, dataValiditaTomorrow).then(responseAll => {
      if (!responseAll.ok) {
        toast.open(
          {
            message: `Errore ${responseAll.status} nel recupero del bollettino`,
            type: 'error',
            position: 'top-left'
          }
        )
      }
      return responseAll.json()
    }).then(dataAll => {
      const yesterdayBis = dataAll.results.find(bulletin => new Date(bulletin.data_validita).getDay() === yesterday.getDay() 
      && new Date(bulletin.data_validita).getMonth() === yesterday.getMonth() 
      && new Date(bulletin.data_validita).getFullYear() === yesterday.getFullYear())
      if(yesterdayBis){
        fetchBis(yesterdayBis.id_w26).then(responseAll => {
          if (!responseAll.ok) {
            toast.open(
              {
                message: `Errore ${responseAll.status} nel recupero del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
          }
          return responseAll.json()
        }).then(yesterdayData => {
          yesterdaybis.value = yesterdayData
          ready.value = true
          hasYesterday.value = true
        }).catch(error => {
          toast.open(
            {
              message: error,
              type: 'error',
              position: 'top-left'
            }
          )
        })
      }else{
        ready.value = true
        hasYesterday.value = false
      }

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

async function fetchBis (id) {
  const response = await fetch('/api/w26/bulletins/' + id + '/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchAllBis (date_min, date_max) {
  const response = await fetch(`/api/w26/bulletins/?data_min=${date_min}&data_max=${date_max}`, {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

function getDateFormatted(rawString, time = true) {
  return api.getDateFormatted(rawString, time)
}

function openNoteModal(area){
  selectedarea.value = area
  const noteSelectModalElement = document.getElementById('modalNoteSelect')
  const noteSelectModal = new Modal(noteSelectModalElement)
  noteSelectModal.show()
  
}

function dateToString(date){
  const yy = date.getFullYear()
  const mm = date.getMonth() + 1
  const dd = date.getDate()
  return [yy, (mm>9 ? '' : '0') + mm, (dd>9 ? '' : '0') + dd].join('-')
}

function saveW26(newValue, id_w26, campo) {
  //data_validata
  if (campo==="data_validita") {
    let month = String(newValue.getMonth() + 1);
    let day = String(newValue.getDate());
    const year = String(newValue.getFullYear());

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    newValue=`${year}-${month}-${day}`;
    bis.value.data_validita = newValue;
  }

  const payload = { }
  payload['id_w26'] = id_w26
  payload['username'] = store.state.username
  bulkUpdateW26(payload).then((response) => {
    if (!response.ok) {
      toast.open(
        {
          message: 'Errore nel salvataggio',
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(data => {
    toast.open(
      {
        message: 'Dato salvato',
        type: 'success',
        position: 'top-left'
      }
    )
    bis.value.last_update = data.last_update
    bis.value.username = store.state.username
  }).catch((error) => {
    toast.open(
      {
        message: `Errore di comunicazione: ${error}`,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

function saveW26Data(newValue,id_w26_data,campo) {
  let myIdW26 = bis.value.w26data_set.find(w26data => {
    return w26data.id_w26_data === id_w26_data
  })

  const payload = { }
  if(campo === 'idnota'){
    myIdW26[campo] = newValue.idnota
    payload[campo] = newValue.idnota
    
    myIdW26['nota'] = newValue.nota
    payload['nota'] = newValue.nota
  }else{
    myIdW26[campo] = newValue
    payload[campo] = newValue
  }

  fetchPatch(myIdW26.id_w26_data, 'data', payload).then((response) => {
    if (!response.ok) {
      toast.open(
        {
          message: 'Errore nel salvataggio',
          type: 'error',
          position: 'top-left'
        }
      )
    } else {
      saveW26(null, bis.value.id_w26, null)
    }
  }).catch((error) => {
    toast.open(
      {
        message: `Errore di comunicazione: ${error}`,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

function remove() {
  if (
    confirm('Vuoi davvero cancellare questo bollettino?')
  ) {
    api.fetchBulletinDelete(bis_id.value, 'w26/bulletins', store).then(response => {
      if (response.ok) {
        toast.open(
          {
            message: 'Bollettino cancellato',
            type: 'success',
            position: 'top-left'
          }
        )
        router.back()
      } else {
        toast.open(
          {
            message: `Errore ${response.status} nella cancellazione del bollettino`,
            type: 'error',
            position: 'top-left'
          }
        )
      }
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
}

async function fetchBisAction (action) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w26/bulletins/${bis_id.value}/${action}/`
  )
  return response
}

function execute(action, reroute, message) {
  actions.value[action + 'ing']= true
  fetchBisAction(action).then(response => {
    actions.value[action + 'ing'] = false
    if (response.ok) {
      return response.json()
    } else {
      toast.open(
        {
          message: `Errore ${response.status} nell'esecuzione del comando ${action}`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
  }).then(data => {
    toast.open(
      {
        message: message,
        type: 'success',
        position: 'top-left'
      }
    )
    if (reroute) {
      router.push({ path: `/w26/${data.id_w26}`})
      bis_id.value = data.id_w26
      fetchData()
    } else {
      fetchData()
    }
  }).catch((error) => {
    this[action + 'ing'] = false
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

async function fetchPatch(id, endpoint, payload) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w26/${endpoint}/${id}/`,
    {
      method: 'PATCH',
      body: JSON.stringify(payload)
    }
  )
  return response
}

async function bulkUpdateW26(payload) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w26/bulletins/bulk_update/`,
    {
      method: 'POST',
      body: JSON.stringify(payload)
    }
  )
  return response
}
</script>
