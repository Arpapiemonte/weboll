// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="row m-5">
    <div class="col-md-8 offset-md-2">
      <h1>ARPA Piemonte - weboll - bulletin back-office</h1>
      <h2>Bollettini disponibili:</h2>
      <div v-if="!ready" class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <div class="row">
        <div class="form-check form-switch mt-4">
          <input 
            id="viewMapCheck" 
            v-model="visualizzaDate" 
            class="form-check-input" 
            type="checkbox"
          >
          <label
            v-if="visualizzaDate"
            class="form-check-label" 
            for="viewMapCheck"
          >
            Non visualizzare le date degli ultimi Bollettini
          </label>
          <label
            v-else
            class="form-check-label" 
            for="viewMapCheck"
          >
            Visualizza le date degli ultimi Bollettini
          </label>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12 mb-3">
          <div
            id="accordianHomePage"
            class="accordion"
          >
            <div class="accordion-item">
              <h2
                id="heading1"
                class="accordion-header"
              >
                <button
                  class="accordion-button collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#collapse1"
                  aria-expanded="false"
                  aria-controls="collapse1"
                >
                  Meteo
                </button>
              </h2>
              <div
                id="collapse1"
                class="accordion-collapse collapse"
                aria-labelledby="heading1"
                data-bs-parent="#accordianHomePage"
              >
                <div class="accordion-body">
                  <div class="row row-cols-1 row-cols-sm-2 mt-5">
                    <div
                      v-for="bulletin in meteo_bulletins_list"
                      :key="bulletin.id"
                      class="col"
                    >
                      <router-link
                        v-slot="{ navigate }"
                        :to="'/' + bulletin.id"
                        custom
                      >
                        <div
                          class="alert d-flex align-items-center mb-1 pb-3 h-75"
                          :class="bulletin.readyForProduction?'alert-success':'alert-danger'"
                          role="button"
                          @click="navigate"
                        >
                          <img
                            :src="`/api/static/images/logo_${bulletin.id}.svg`"
                            width="80"
                            class="img-fluid rounded-start"
                            :alt="`Logo ${bulletin.name}`"
                          >
                          <div class="ms-3 h5 flex-grow-1">
                            {{ bulletin.name }}
                          </div>
                          <div class="float-end align-self-end text-nowrap" 
                            :style="bulletins[bulletin.id]==today?'color:green':'color:red'">
                            {{ bulletins[bulletin.id] }}
                          </div>
                        </div>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="accordion-item">
              <h2
                id="heading2"
                class="accordion-header"
              >
                <button
                  class="accordion-button collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#collapse2"
                  aria-expanded="false"
                  aria-controls="collapse2"
                >
                  Aria
                </button>
              </h2>
              <div
                id="collapse2"
                class="accordion-collapse collapse"
                aria-labelledby="heading2"
                data-bs-parent="#accordianHomePage"
              >
                <div class="accordion-body">
                  <div class="row row-cols-1 row-cols-sm-2 mt-5">
                    <div
                      v-for="bulletin in aria_bulletins_list"
                      :key="bulletin.id"
                      class="col"
                    >
                      <router-link
                        v-slot="{ navigate }"
                        :to="'/' + bulletin.id"
                        custom
                      >
                        <div
                          class="alert d-flex align-items-center mb-1 pb-3 h-75"
                          :class="bulletin.readyForProduction?'alert-success':'alert-danger'"
                          role="button"
                          @click="navigate"
                        >
                          <img
                            :src="`/api/static/images/logo_${bulletin.id}.svg`"
                            width="80"
                            class="img-fluid rounded-start"
                            :alt="`Logo ${bulletin.name}`"
                          >
                          <div class="ms-3 h5 flex-grow-1">
                            {{ bulletin.name }}
                          </div>
                          <div class="float-end align-self-end text-nowrap"
                            :style="bulletins[bulletin.id]==today?'color:green':'color:red'">
                            {{ bulletins[bulletin.id] }}
                          </div>
                        </div>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="accordion-item">
              <h2
                id="heading3"
                class="accordion-header"
              >
                <button
                  class="accordion-button collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#collapse3"
                  aria-expanded="false"
                  aria-controls="collapse3"
                >
                  Idro
                </button>
              </h2>
              <div
                id="collapse3"
                class="accordion-collapse collapse"
                aria-labelledby="heading3"
                data-bs-parent="#accordianHomePage"
              >
                <div class="accordion-body">
                  <div class="row row-cols-1 row-cols-sm-2 mt-5">
                    <div
                      v-for="bulletin in idro_bulletins_list"
                      :key="bulletin.id"
                      class="col"
                    >
                      <router-link
                        v-slot="{ navigate }"
                        :to="'/' + bulletin.id"
                        custom
                      >
                        <div
                          class="alert d-flex align-items-center mb-1 pb-3 h-75"
                          :class="bulletin.readyForProduction?'alert-success':'alert-danger'"
                          role="button"
                          @click="navigate"
                        >
                          <img
                            :src="`/api/static/images/logo_${bulletin.id}.svg`"
                            width="80"
                            class="img-fluid rounded-start"
                            :alt="`Logo ${bulletin.name}`"
                          >
                          <div class="ms-3 h5 flex-grow-1">
                            {{ bulletin.name }}
                          </div>
                          <div class="float-end align-self-end text-nowrap"
                            :style="bulletins[bulletin.id]==today?'color:green':'color:red'">
                            {{ bulletins[bulletin.id] }}
                          </div>
                        </div>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="accordion-item">
              <h2
                id="heading4"
                class="accordion-header"
              >
                <button
                  class="accordion-button collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#collapse4"
                  aria-expanded="false"
                  aria-controls="collapse4"
                >
                  Allerta
                </button>
              </h2>
              <div
                id="collapse4"
                class="accordion-collapse collapse"
                aria-labelledby="heading4"
                data-bs-parent="#accordianHomePage"
              >
                <div class="accordion-body">
                  <div class="row row-cols-1 row-cols-sm-2 mt-5">
                    <div
                      v-for="bulletin in allerta_bulletins_list"
                      :key="bulletin.id"
                      class="col"
                    >
                      <router-link
                        v-slot="{ navigate }"
                        :to="'/' + bulletin.id"
                        custom
                      >
                        <div
                          class="alert d-flex align-items-center mb-1 pb-3 h-75"
                          :class="bulletin.readyForProduction?'alert-success':'alert-danger'"
                          role="button"
                          @click="navigate"
                        >
                          <img
                            :src="`/api/static/images/logo_${bulletin.id}.svg`"
                            width="80"
                            class="img-fluid rounded-start"
                            :alt="`Logo ${bulletin.name}`"
                          >
                          <div class="ms-3 h5 flex-grow-1">
                            {{ bulletin.name }}
                          </div>
                          <div class="float-end align-self-end text-nowrap"
                            :style="bulletins[bulletin.id]==today?'color:green':'color:red'">
                            {{ bulletins[bulletin.id] }}
                          </div>
                        </div>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="accordion-item">
              <h2
                id="heading5"
                class="accordion-header"
              >
                <button
                  class="accordion-button collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#collapse5"
                  aria-expanded="false"
                  aria-controls="collapse5"
                >
                  Incendi
                </button>
              </h2>
              <div
                id="collapse5"
                class="accordion-collapse collapse"
                aria-labelledby="heading5"
                data-bs-parent="#accordianHomePage"
              >
                <div class="accordion-body">
                  <div class="row row-cols-1 row-cols-sm-2 mt-5">
                    <div
                      v-for="bulletin in incendi_bulletins_list"
                      :key="bulletin.id"
                      class="col"
                    >
                      <router-link
                        v-slot="{ navigate }"
                        :to="'/' + bulletin.id"
                        custom
                      >
                        <div
                          class="alert d-flex align-items-center mb-1 pb-3 h-75"
                          :class="bulletin.readyForProduction?'alert-success':'alert-danger'"
                          role="button"
                          @click="navigate"
                        >
                          <img
                            :src="`/api/static/images/logo_${bulletin.id}.svg`"
                            width="80"
                            class="img-fluid rounded-start"
                            :alt="`Logo ${bulletin.name}`"
                          >
                          <div class="ms-3 h5 flex-grow-1">
                            {{ bulletin.name }}
                          </div>
                          <div class="float-end align-self-end text-nowrap"
                            :style="bulletins[bulletin.id]==today?'color:green':'color:red'">
                            {{ bulletins[bulletin.id] }}
                          </div>
                        </div>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="accordion-item">
              <h2
                id="heading6"
                class="accordion-header"
              >
                <button
                  class="accordion-button collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#collapse6"
                  aria-expanded="false"
                  aria-controls="collapse6"
                >
                  Autostrade
                </button>
              </h2>
              <div
                id="collapse6"
                class="accordion-collapse collapse"
                aria-labelledby="heading6"
                data-bs-parent="#accordianHomePage"
              >
                <div class="accordion-body">
                  <div class="row row-cols-1 row-cols-sm-2 mt-5">
                    <div
                      v-for="bulletin in autostrade_bulletins_list"
                      :key="bulletin.id"
                      class="col"
                    >
                      <router-link
                        v-slot="{ navigate }"
                        :to="'/' + bulletin.id"
                        custom
                      >
                        <div
                          class="alert d-flex align-items-center mb-1 pb-3 h-75"
                          :class="bulletin.readyForProduction?'alert-success':'alert-danger'"
                          role="button"
                          @click="navigate"
                        >
                          <img
                            :src="`/api/static/images/logo_${bulletin.id}.svg`"
                            width="80"
                            class="img-fluid rounded-start"
                            :alt="`Logo ${bulletin.name}`"
                          >
                          <div class="ms-3 h5 flex-grow-1">
                            {{ bulletin.name }}
                          </div>
                          <div class="float-end align-self-end text-nowrap"
                            :style="bulletins[bulletin.id]==today?'color:green':'color:red'">
                            {{ bulletins[bulletin.id] }}
                          </div>
                        </div>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="accordion-item">
              <h2
                id="heading7"
                class="accordion-header"
              >
                <button
                  class="accordion-button collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#collapse7"
                  aria-expanded="false"
                  aria-controls="collapse7"
                >
                  Tools
                </button>
              </h2>
              <div
                id="collapse7"
                class="accordion-collapse collapse"
                aria-labelledby="heading7"
                data-bs-parent="#accordianHomePage"
              >
                <div class="accordion-body">
                  <div class="row row-cols-1 row-cols-sm-2 mt-5">
                    <div
                      v-for="bulletin in tools_bulletins_list"
                      :key="bulletin.id"
                      class="col"
                    >
                      <router-link
                        v-slot="{ navigate }"
                        :to="'/' + bulletin.id"
                        custom
                      >
                        <div
                          class="alert d-flex align-items-center mb-1 pb-3 h-75"
                          :class="bulletin.readyForProduction?'alert-success':'alert-danger'"
                          role="button"
                          @click="navigate"
                        >
                          <img
                            :src="`/api/static/images/logo_${bulletin.id}.svg`"
                            width="80"
                            class="img-fluid rounded-start"
                            :alt="`Logo ${bulletin.name}`"
                          >
                          <div class="ms-3 h5 flex-grow-1">
                            {{ bulletin.name }}
                          </div>
                          <div class="float-end align-self-end text-nowrap"
                            :style="bulletins[bulletin.id]==today?'color:green':'color:red'">
                            {{ bulletins[bulletin.id] }}
                          </div>
                        </div>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <hr>
      <a
        target="_blank"
        :href="repo_home"
      >Codice sorgente e issues per segnalare malfunzionamenti </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import api from '../../src/api'
import { useToast } from 'vue-toast-notification'
import { watch, ref, computed } from 'vue'

let bulletins = ref({})
const toast = useToast()
let ready = ref(true)
let fetchCount = ref(0)
let visualizzaDate = ref(false)

const filtered_bulletins_list = computed(() => {
  if (appmode.value === 'development') {
    return window.bulletins_list
  } else {
    return window.bulletins_list.filter(bulletin => bulletin.readyForProduction)
  }
})

const meteo_bulletins_list = computed(() => {
  let my_bull = window.bulletins_list.filter(bulletin => bulletin.menu == 'Meteo')
  // return my_bull.filter(bulletin => bulletin.readyForProduction)
  return my_bull
})

const aria_bulletins_list = computed(() => {
  let my_bull = window.bulletins_list.filter(bulletin => bulletin.menu == 'Aria')
  // return my_bull.filter(bulletin => bulletin.readyForProduction)
  return my_bull
})

const idro_bulletins_list = computed(() => {
  let my_bull = window.bulletins_list.filter(bulletin => bulletin.menu == 'Idro')
  // return my_bull.filter(bulletin => bulletin.readyForProduction)
  return my_bull
})

const allerta_bulletins_list = computed(() => {
  let my_bull = window.bulletins_list.filter(bulletin => bulletin.menu == 'Allerta')
  // return my_bull.filter(bulletin => bulletin.readyForProduction)
  return my_bull
})

const incendi_bulletins_list = computed(() => {
  let my_bull = window.bulletins_list.filter(bulletin => bulletin.menu == 'Incendi')
  // return my_bull.filter(bulletin => bulletin.readyForProduction)
  return my_bull
})

const autostrade_bulletins_list = computed(() => {
  let my_bull = window.bulletins_list.filter(bulletin => bulletin.menu == 'Autostrade')
  // return my_bull.filter(bulletin => bulletin.readyForProduction)
  return my_bull
})

const tools_bulletins_list = computed(() => {
  let my_bull = window.bulletins_list.filter(bulletin => bulletin.menu == 'Tools')
  // return my_bull.filter(bulletin => bulletin.readyForProduction)
  return my_bull
})

const appmode = computed(() => {
  return import.meta.env.MODE
})

const repo_home = computed(() => {
  return import.meta.env.VITE_REPO_HOME || 'https://github.com/Arpapiemonte/weboll'
})

async function fetchBulletin(endpoint, element){
  // console.log("fetchBulletin start", endpoint, ready.value, fetchCount.value)
  await api.fetchBulletins(endpoint, 0).then(response => {
    if (!response.ok) {
      console.log("Errore response", response)
    }else{
      console.log("Restituisco il json")
      return response.json()
    }
  }).then(data => {
    console.log("Entro nel then", data)
    if (data){
      if ("results" in data){
        if (data.results.length>0){ 
          let found = -1
          let i = 0
          while (found == -1 && i < data.results.length){
            if ("status" in data.results[i])
              if (!(data.results[i].status == '0')) found = i
            i = i + 1 
            //console.log("in while", element.id, i)
          }
          if (found > -1){
            if ("last_update" in data.results[found]){
              bulletins.value[element.id] = data.results[found].last_update.substring(0, 10)
            }
          }
        }
      }
    }
  }).catch((error) => {
    console.log("Entro nel catch")
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
  fetchCount.value = fetchCount.value + 1
  // console.log("fetchBulletin end", endpoint, ready.value, fetchCount.value)
  // console.log(fetchCount.value, window.bulletins_list.length)
  if (fetchCount.value == window.bulletins_list.length) ready.value=true
}

function fetchBulletins(){
  window.bulletins_list.forEach(element => {
    bulletins.value[element.id] = ""
    let endpoint = element.id + "/bulletins"
    //console.log("fetchBulletins", endpoint)
    fetchBulletin(endpoint, element)
  })
}

const today = computed(() => {
  let d = new Date()
  return d.toISOString().substring(0, 10)
})


watch(() => visualizzaDate.value, (new_value) => {
  if (new_value){
    ready.value=false
    fetchBulletins()
  }else{
    fetchCount.value = 1
    bulletins.value = {}
  }
})
</script>
