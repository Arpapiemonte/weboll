// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
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
        <button
          v-if="aggiornamento.status === '0' && state.username"
          :disabled="actions.sending"
          type="button"
          class="btn btn-outline-dark"
          @click="execute('reload_data', false, 'Ricarica immagini e dati del bollettino di aggiornamento completata')"
        >
          <span>
            <img
              src="~bootstrap-icons/icons/repeat.svg"
              alt="calc icon"
              width="18"
              height="18"
            > Ricarica immagini e dati
          </span>
        </button>
        <a
          class="btn btn-outline-primary"
          :href="'/api/w37/pdf/' + aggiornamento.id_w37"
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
          v-if="aggiornamento.status === '0' && state.username"
          :disabled="actions.sending"
          type="button"
          class="btn btn-outline-success"
          @click="execute_timeout('send', false, 'Bollettino inviato')"
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
          v-if="aggiornamento.status === '1' && state.username && aggiornamento.data_emissione.substring(0, 10) === today"
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
          v-if="aggiornamento.status === '0' && state.username"
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
      <h1>Aggiornamento Allerta {{ aggiornamento.id_w37 }} </h1>
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="aggiornamento.status === '1'">
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
            :value="getDateFormatted(aggiornamento.data_emissione, false)"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="ora_emissione">ora emissione
          <input
            id="ora_emissione"
            v-model="aggiornamento.ora_emissione"
            class="form-control"
            name="ora_emissione"
            :readonly="readonly"
            @change="saveW37(aggiornamento.ora_emissione, aggiornamento.id_w37, 'ora_emissione')"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_aggiornamento">Data Aggiornamento</label>
        <Datepicker
          v-model="aggiornamento.data_aggiornamento"
          :disabled="readonly"
          :style="readonly ? '--dp-disabled-color: #e9ecef' : '--dp-background-color: white'"
          format="dd/MM/yyyy"
          auto-apply
          @update:model-value="saveW37(aggiornamento.data_aggiornamento, aggiornamento.id_w37, 'data_aggiornamento')"
        />
      </div>
      <div class="col-md-2 mb-3">
        <label for="ora_aggiornamento">ora aggiornamento
          <input
            id="ora_aggiornamento"
            v-model="aggiornamento.ora_aggiornamento"
            class="form-control"
            name="ora_aggiornamento"
            :readonly="readonly"
            @change="saveW37(aggiornamento.ora_aggiornamento, aggiornamento.id_w37, 'ora_aggiornamento')"
          >
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
            :value="getDateFormatted(aggiornamento.last_update)"
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
            :value="aggiornamento.username"
          >
        </label>
      </div>
    </div>

    <div class="row mt-3">
      <div class="col-xl-12 col-md-12 mb-3">
        <ul
          id="pills-tab"
          class="nav nav-pills mb-3"
          role="tablist"
        >
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-situazione_attuale-tab"
              class="nav-link active"
              data-bs-toggle="pill"
              data-bs-target="#pills-situazione_attuale"
              type="button"
              role="tab"
              aria-controls="pills-situazione_attuale"
              aria-selected="true"
            >
              Situazione attuale
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-previsione_meteo-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-previsione_meteo"
              type="button"
              role="tab"
              aria-controls="pills-previsione_meteo"
              aria-selected="false"
            >
              Previsione meteorologica
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-previsione_idro-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-previsione_idro"
              type="button"
              role="tab"
              aria-controls="pills-previsione_idro"
              aria-selected="false"
            >
              Previsione idrologica
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-mappe-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-mappe"
              type="button"
              role="tab"
              aria-controls="pills-mappe"
              aria-selected="false"
            >
              Mappe pericolo
            </button>
          </li>
        </ul>
        <div
          id="pills-tabContent"
          class="tab-content"
        >
          <div
            id="pills-situazione_attuale"
            class="tab-pane fade show active"
            role="tabpanel"
            aria-labelledby="pills-situazione_attuale-tab"
          >
            <div class="col-md-12 mb-3">
              <div class="row">
                <div class="col-md-12 mb-3">
                  <table>
                    <tbody>
                      <tr>
                        <td>
                          <label for="situazione_attuale">Commento alla situazione</label><br>
                          <textarea
                            id="situazione_attuale"
                            v-model="aggiornamento.situazione_attuale"
                            class="form-control"
                            name="situazione_attuale"
                            rows="14"
                            cols="80"
                            :readonly="readonly"
                            @change="saveW37(aggiornamento.situazione_attuale, aggiornamento.id_w37, 'situazione_attuale')"
                          />
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          <div
            id="pills-previsione_meteo"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-previsione_meteo-tab"
          >
            <div class="col-md-12 mb-3">
              <div class="row">
                <div class="col-md-12 mb-3">
                  <table>
                    <tbody>
                      <tr>
                        <td>
                          <label for="previsione_meteo">Previsione meteo prossime ore</label><br>
                          <textarea
                            id="previsione_meteo"
                            v-model="aggiornamento.previsione_meteo"
                            class="form-control"
                            name="previsione_meteo"
                            rows="15"
                            cols="100"
                            :readonly="readonly"
                            @change="saveW37(aggiornamento.previsione_meteo, aggiornamento.id_w37, 'previsione_meteo')"
                          />
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          <div
            id="pills-previsione_idro"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-previsione_idro-tab"
          >
            <div class="col-md-12 mb-3">
              <div class="row">
                <div class="col-md-12 mb-3">
                  <table>
                    <tbody>
                      <tr>
                        <td>
                          <label for="previsione_idro">Evoluzione corsi d'acqua prossime ore</label><br>
                          <textarea
                            id="previsione_idro"
                            v-model="aggiornamento.previsione_idro"
                            class="form-control"
                            name="previsione_idro"
                            rows="14"
                            cols="102"
                            :readonly="readonly"
                            @change="saveW37(aggiornamento.previsione_idro, aggiornamento.id_w37, 'previsione_idro')"
                          />
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          <div
            id="pills-mappe"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-mappe-tab"
          >
            <div class="col-md-12 mb-3">
              <div class="row">
                <div class="col-md-12 mb-3">
                  <table>
                    <tbody>
                      <tr>
                        <td>
                          <label for="situazione_attuale">Mappa 3h</label><br>
                          <img
                            v-if="aggiornamento.mappa_3h==null"
                            src="../back/static/images/empty.png"
                            class="img-fluid"
                            alt="Anteprima immagine"
                            style="max-width: 500px; max-height: 500px;"
                          >
                          <img
                            v-else
                            :src="`data:image/png;base64,${aggiornamento.mappa_3h}`"
                            alt="Mappa 3h"
                            style="max-width: 500px; max-height: 500px;"
                          >
                        </td>
                        <td>
                          <label for="situazione_attuale">Mappa 24h</label><br>
                          <img
                            v-if="aggiornamento.mappa_24h==null"
                            src="../back/static/images/empty.png"
                            class="img-fluid"
                            alt="Anteprima immagine"
                            style="max-width: 500px; max-height: 500px;"
                          >
                          <img
                            v-else
                            :src="`data:image/png;base64,${aggiornamento.mappa_24h}`"
                            alt="Mappa 24h"
                            style="max-width: 500px; max-height: 500px;"
                          >
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
  </div>
</template>

<script lang="ts">
export default {
  name: 'AggiornamentoBulletin',
}
</script>

<script setup lang="ts">
import { Ref, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toast-notification'

import api from '../../src/api'
import store from '../../src/store'

import { components } from '../../src/types/weboll'
import type { W37_data } from "../types"

const router = useRouter()
const toast = useToast()

type W37Full = components['schemas']['W37'] & { w37_data: W37_data } & { w37data_set: components['schemas']['W37Data'][] } 

// reactive properties
let aggiornamento_id = ref('')
let aggiornamento: Ref<W37Full> = ref({"id_w37":238,"w37data_set":[{"id_w37_data":198003,"codice_comune":"096043","numeric_value":2,"id_w37":238,"id_time_layouts":49,"id_parametro":"PLUV"},{"id_w37_data":198004,"codice_comune":"096043","numeric_value":3,"id_w37":238,"id_time_layouts":49,"id_parametro":"IDRO"},{"id_w37_data":198005,"codice_comune":"096043","numeric_value":4,"id_w37":238,"id_time_layouts":49,"id_parametro":"STORM"},{"id_w37_data":198006,"codice_comune":"096043","numeric_value":4,"id_w37":238,"id_time_layouts":49,"id_parametro":"DANGER24"},{"id_w37_data":198007,"codice_comune":"001201","numeric_value":2,"id_w37":238,"id_time_layouts":49,"id_parametro":"PLUV"},{"id_w37_data":198008,"codice_comune":"001201","numeric_value":3,"id_w37":238,"id_time_layouts":49,"id_parametro":"IDRO"},{"id_w37_data":198009,"codice_comune":"001201","numeric_value":4,"id_w37":238,"id_time_layouts":49,"id_parametro":"STORM"},{"id_w37_data":198010,"codice_comune":"001201","numeric_value":4,"id_w37":238,"id_time_layouts":49,"id_parametro":"DANGER24"},{"id_w37_data":198011,"codice_comune":"001272","numeric_value":2,"id_w37":238,"id_time_layouts":49,"id_parametro":"PLUV"},{"id_w37_data":198012,"codice_comune":"001272","numeric_value":3,"id_w37":238,"id_time_layouts":49,"id_parametro":"IDRO"},{"id_w37_data":198013,"codice_comune":"001272","numeric_value":4,"id_w37":238,"id_time_layouts":49,"id_parametro":"STORM"},{"id_w37_data":198014,"codice_comune":"001272","numeric_value":4,"id_w37":238,"id_time_layouts":49,"id_parametro":"DANGER24"}],"numero_bollettino":2,"data_emissione":"2024-02-17T01:00:00","ora_emissione":"01:00","situazione_attuale":"situazione 2","previsione_meteo":"meteo 2","previsione_idro":"idro 2","status":"1","last_update":"2023-02-17T08:32:10.579337","username":"weboll","id_w37_parent":null,"mappa_3h":"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... (10025 total length)","mappa_24h":"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... (10025 total length)","w37_data":{"PLUV":{"49":{"096043":[{"id_w37_data":198003,"codice_comune":"096043","numeric_value":2,"id_w37":238,"id_time_layouts":49,"id_parametro":"PLUV"}],"001201":[{"id_w37_data":198007,"codice_comune":"001201","numeric_value":2,"id_w37":238,"id_time_layouts":49,"id_parametro":"PLUV"}],"001272":[{"id_w37_data":198011,"codice_comune":"001272","numeric_value":2,"id_w37":238,"id_time_layouts":49,"id_parametro":"PLUV"}]}},"IDRO":{"49":{"096043":[{"id_w37_data":198004,"codice_comune":"096043","numeric_value":3,"id_w37":238,"id_time_layouts":49,"id_parametro":"IDRO"}],"001201":[{"id_w37_data":198008,"codice_comune":"001201","numeric_value":3,"id_w37":238,"id_time_layouts":49,"id_parametro":"IDRO"}],"001272":[{"id_w37_data":198012,"codice_comune":"001272","numeric_value":3,"id_w37":238,"id_time_layouts":49,"id_parametro":"IDRO"}]}},"STORM":{"49":{"096043":[{"id_w37_data":198005,"codice_comune":"096043","numeric_value":4,"id_w37":238,"id_time_layouts":49,"id_parametro":"STORM"}],"001201":[{"id_w37_data":198009,"codice_comune":"001201","numeric_value":4,"id_w37":238,"id_time_layouts":49,"id_parametro":"STORM"}],"001272":[{"id_w37_data":198013,"codice_comune":"001272","numeric_value":4,"id_w37":238,"id_time_layouts":49,"id_parametro":"STORM"}]}},"DANGER24":{"49":{"096043":[{"id_w37_data":198006,"codice_comune":"096043","numeric_value":4,"id_w37":238,"id_time_layouts":49,"id_parametro":"DANGER24"}],"001201":[{"id_w37_data":198010,"codice_comune":"001201","numeric_value":4,"id_w37":238,"id_time_layouts":49,"id_parametro":"DANGER24"}],"001272":[{"id_w37_data":198014,"codice_comune":"001272","numeric_value":4,"id_w37":238,"id_time_layouts":49,"id_parametro":"DANGER24"}]}}}})
let state = ref(store.state)
let ready = ref(false)
let saving = ref(false)
let readonly = ref(true)
let today = ref('')

const props = defineProps({
    id: {
        type: String,
        default: () => ''
    },
})


let actions = ref({
  sending:false,
  reopening: false,
})

onMounted(() => {
  aggiornamento_id.value = props.id
  fetchData()
})

async function fetchData() {
  today.value = dateToString(new Date())
  ready.value = false
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  fetchAggiornamento(aggiornamento_id.value).then(response => {
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
  }).then(async data => {
    
    aggiornamento.value = data
    readonly.value = (aggiornamento.value.status === '1' || aggiornamento.value.status === '2' || !state.value.username)
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

async function fetchAggiornamento(id: string | number) {
  const response = await fetch('/api/w37/bulletins/' + id + '/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}


function getDateFormatted(rawString: string, time = true) {
  return api.getDateFormatted(rawString, time)
}

function saveW37(newValue: null, id_w37: any, campo: null) {
  saving.value = true
  //console.log(newValue,campo)
  const payload = { }
  payload['id_w37'] = id_w37
  payload['username'] = store.state.username
  if (campo=='ora_aggiornamento')
    payload['ora_aggiornamento'] = newValue
  if (campo=='ora_emissione')
    payload['ora_emissione'] = newValue
  if (campo=='situazione_attuale')
    payload['situazione_attuale'] = newValue
  if (campo=='previsione_meteo')
    payload['previsione_meteo'] = newValue
  if (campo=='previsione_idro')
    payload['previsione_idro'] = newValue

  if (campo==="data_aggiornamento") {
    if(newValue!=null){
      let month = String(newValue.getMonth() + 1);
      let day = String(newValue.getDate());
      const year = String(newValue.getFullYear());

      if (month.length < 2) month = '0' + month;
      if (day.length < 2) day = '0' + day;

      newValue=`${year}-${month}-${day}`;
      payload['data_aggiornamento']=newValue;
    }else{
      payload['data_aggiornamento']=null
    }
      
  }
  bulkUpdateW37(payload).then((response) => {
    if (!response.ok) {
      toast.open(
        {
          message: 'Errore nel salvataggio',
          type: 'error',
          position: 'top-left'
        }
      )
      saving.value = false
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
    saving.value = false
    aggiornamento.value.last_update = data.last_update
    aggiornamento.value.username = (store.state.username || "")
  }).catch((error) => {
    toast.open(
      {
        message: `Errore di comunicazione: ${error}`,
        type: 'error',
        position: 'top-left'
      }
    )
    saving.value = false
  })
}


function remove() {
  if (
    confirm('Vuoi davvero cancellare questo bollettino?')
  ) {
    api.fetchBulletinDelete(aggiornamento_id.value, 'w37/bulletins', store).then(response => {
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

async function fetchAggiornamentoAction(action: any) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w37/bulletins/${aggiornamento_id.value}/${action}/`
  )
  return response
}

function execute_timeout(action, reroute, message){
  // console.log("inizio execute_timeout")
  if (saving.value){
    console.log("saving è true faccio partire timeout")
    setTimeout(() => {
      console.log("aspetto 1 secondo finchè non finisce il salvataggio in corso")
      execute_timeout(action, reroute, message)
    }, 1000);
  }else{
    console.log("saving è false lancio execute")
    execute(action, reroute, message)
  }
  // console.log("fine execute_timeout")
}

function execute(action: string, reroute: any, message: any) {
  actions.value[action + 'ing'] = true
  fetchAggiornamentoAction(action).then(response => {
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
      router.push({ path: `/w37/${data.id_w37}` })
      aggiornamento_id.value = data.id_w37
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

async function bulkUpdateW37(payload: {}) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w37/bulletins/bulk_update/`,
    {
      method: 'POST',
      body: JSON.stringify(payload)
    }
  )
  return response
}

function dateToString(date){
  const yy = date.getFullYear()
  const mm = date.getMonth() + 1
  const dd = date.getDate()
  return [yy, (mm>9 ? '' : '0') + mm, (dd>9 ? '' : '0') + dd].join('-')
}

</script>

