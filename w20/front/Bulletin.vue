// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
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
        <a
          class="btn btn-outline-primary"
          :href="'/api/w20/pdf/' + traps.id_w20"
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
          v-if="traps.status === '0' && state.username"
          :disabled="sending"
          type="button"
          class="btn btn-outline-success"
          @click="execute('send', false, 'Bollettino inviato')"
        >
          <span v-if="sending">
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
          v-if="traps.status === '0' && state.username"
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
      <h1>Bollettino Traps {{ traps.numero_bollettino }}</h1>
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="traps.status == 1">
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
            :value="getDateFormatted(traps.data_emissione, false)"
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
            :value="getDateFormatted(traps.last_update)"
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
            :value="traps.username"
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
              id="pills-bollettino_emesso-tab"
              class="nav-link active"
              data-bs-toggle="pill"
              data-bs-target="#pills-bollettino_emesso"
              type="button"
              role="tab"
              aria-controls="pills-bollettino_emesso"
              aria-selected="true"
            >
              Bollettino emesso
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
              Mappa
            </button>
          </li> 
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-immagini-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-immagini"
              type="button"
              role="tab"
              aria-controls="pills-immagini"
              aria-selected="false"
            >
              Immagini
            </button>
          </li> 
        </ul>
        <div
          id="pills-tabContent"
          class="tab-content"
        >
          <div
            id="pills-bollettino_emesso"
            class="tab-pane fade show active"
            role="tabpanel"
            aria-labelledby="pills-bollettino_emesso-tab"
          >
            <div class="col-xl-7 col-md-7 mb-3">
              <table class="table">
                <thead>
                  <tr>
                    <th scope="col">
                      Comune
                    </th>
                    <th scope="col">
                      provincia
                    </th>
                    <th scope="col">
                      if_perc
                    </th>
                    <th scope="col">
                      Probabilità<br> Innesco
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="area in traps.w20data_set"
                    :key="area.id_w20"
                  >
                    <th scope="row">
                      {{ area.comune }}
                    </th>
                    <th scope="row">
                      {{ area.provincia }}
                    </th>
                    <th scope="row">
                      {{ area.if_perc }}
                    </th>
                    <CellPericolo
                      :area="area"
                      :campo="'prob_innesco'"
                      :pericolo="pericolo"
                      :readonly="readonly"
                      :required="true"
                      @change-pericolo="saveW20DataPericolo"
                    />
                  </tr>
                </tbody>
              </table>
            </div>  <!--col-->
            <div class="col-xl-5 col-md-12 mb-3">
              <div
                class="sticky-top pt-5"
                style="z-index: 0;"
              />
            </div> <!-- col -->
          </div>
          <div
            id="pills-mappe"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-mappe-tab"
          >
            <div class="col-md-12 mb-3">
              <div>
                <div class="row">
                  <div class="col-sm">
                    Visualizzazione Mappa
                  </div>
                </div>
                <div class="row">
                  <div class="col-sm">
                    <MapTraps
                      :orography="true"
                      :rivers="false"
                      :provinces="false"
                      :capitals="false"
                      :layer="true"
                      :venue-data="livello_innesco"
                      :trapsdata="traps_innesco"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div
            id="pills-immagini"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-immagini-tab"
          >
            <div class="col-md-12 mb-3">
              <div>
                <div class="row">
                  <div class="col-sm">
                    <table>
                      <tbody>
                        <tr>
                          <td>
                            <label for="situazione_attuale">Pioggia cumulata 60 gg</label><br>
                            <img
                              v-if="traps.pioggia_infiltrata==null"
                              src="../back/static/images/empty.png"
                              class="img-fluid"
                              alt="Anteprima immagine"
                              style="max-width: 500px; max-height: 500px;"
                            >
                            <img
                              v-else
                              :src="`data:image/png;base64,${traps.pioggia_infiltrata}`"
                              alt="Mappa 3h"
                              style="max-width: 500px; max-height: 500px;"
                            >
                          </td>
                          <td>
                            <label for="situazione_attuale">Neve al suolo</label><br>
                            <img
                              v-if="traps.neve_equivalente==null"
                              src="../back/static/images/empty.png"
                              class="img-fluid"
                              alt="Anteprima immagine"
                              style="max-width: 500px; max-height: 500px;"
                            >
                            <img
                              v-else
                              :src="`data:image/png;base64,${traps.neve_equivalente}`"
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
      </div> <!-- row -->
      <div class="row" />
    </div>
  </div>
</template>

<script>
import api from '@/api'
import store from '@/store'
import CellPericolo from './CellPericolo.vue'
import MapTraps from './MapTraps.vue'

export default {

  name: 'TrapsBulletin',
  components: {
    CellPericolo,
    MapTraps,
  },
  data () {
    // non reactive properties
    return {
      // reactive properties
      traps: {},
      pericolo: [],
      trapsdata: {},
      state: store.state,
      readonly: true,
      sending: false
    }
  },
  computed: {
    livello_innesco(){
      let vd = { }
      if (this.traps.w20data_set !== undefined) {
        this.traps.w20data_set.forEach(area => {
          vd[area.comune] = this.coloreHtml(area.prob_innesco)
        })
      }
      return vd
    },
    traps_innesco(){
      let vd = { }
      if (this.traps.w20data_set !== undefined) {
        this.traps.w20data_set.forEach(area => {
          let data = { }
          data['prob_innesco'] = area.prob_innesco
          data['prob_innesco_color'] = this.coloreHtml(area.prob_innesco)
          vd[area.comune] = data
        })
      }
      return vd
    },
  },
  created() {
    // https://vuejs.org/v2/guide/instance.html
    this.fetchData()
  },
  methods: {
    coloreHtml(parametro) {
      var colore = 'red'
      if (parametro == 'A')
        colore = '#A6A6A6'
      else if (parametro == 'B')
        colore = '#9999FF'
      else if (parametro == 'E')
        colore = '#9900FF'
      return colore
    },
    async fetchData () {
      this.traps_id = this.$route.params.id
      this.pericolo  = await this.fetchPericolo()
      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
      this.fetchTraps().then(response => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero del bollettino`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json()
      }).then(data => {
        this.traps = data
        this.readonly = (this.traps.status === '1' || !this.state.username)
      }).catch(error => {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    async fetchTraps () {
      // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
      const response = await fetch('/api/w20/bulletins/' + this.traps_id + '/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
     async fetchPericolo () {
      try {
        const response = await fetch('/api/w20/pericolo/', {
          headers: {
            accept: 'application/json'
          }
        })
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero del Pericolo`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return await response.json()
      } catch(error) {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      }
    },
    getDateFormatted(rawString, time = true) {
      return api.getDateFormatted(rawString, time)
    },
    saveW20(newValue, id_w20, campo) {
        const payload = { }
        if (campo) 
        {
          payload[campo] = newValue
        }
        payload['id_w20'] = id_w20
        payload['username'] = store.state.username
        //console.log('SAVE-----',payload)
        //console.log('SAVE--campo ---',campo)
        this.bulkUpdateW20(payload).then((response) => {
            if (!response.ok) {
            this.$toast.open(
                {
                message: 'Errore nel salvataggio',
                type: 'error',
                position: 'top-left'
                }
            )
            }
            return response.json()
        }).then(data => {
            this.$toast.open(
            {
                message: 'Dato salvato',
                type: 'success',
                position: 'top-left'
            }
            )
            this.traps.last_update = data.last_update
            this.traps.username = store.state.username
        }).catch((error) => {
            this.$toast.open(
            {
                message: `Errore di comunicazione: ${error}`,
                type: 'error',
                position: 'top-left'
            }
            )
        })
    },
    saveW20DataPericolo(newValue, comune, campo) {
      let myW20zone = this.traps.w20data_set.find(w20data => {
        return w20data.comune === comune
      })
      myW20zone[campo] = newValue
      
      const payload = { }
      payload[campo] = newValue
      //console.log('saveW20DataPericolo paylod',payload)
      this.fetchPatch(myW20zone.id_w20_data, 'data', payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio',
              type: 'error',
              position: 'top-left'
            }
          )
        } else {
          this.saveW20(newValue, this.traps.id_w20, null)
        }
      }).catch((error) => {
        this.$toast.open(
          {
            message: `Errore di comunicazione: ${error}`,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    remove() {
      if (
        confirm('Vuoi davvero cancellare questo bollettino?')
      ) {
        api.fetchBulletinDelete(this.traps_id, 'w20/bulletins', store).then(response => {
          if (response.ok) {
            this.$toast.open(
              {
                message: 'Bollettino cancellato',
                type: 'success',
                position: 'top-left'
              }
            )
            this.$router.back()
          } else {
            this.$toast.open(
              {
                message: `Errore ${response.status} nella cancellazione del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
          }
        }).catch(error => {
          this.$toast.open(
            {
              message: error,
              type: 'error',
              position: 'top-left'
            }
          )
        })
      }
    },
    async fetchTrapsAction (action) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w20/bulletins/${this.traps_id}/${action}/`
      )
      return response
    },
    execute(action, reroute, message) {
      this[action + 'ing'] = true
      this.fetchTrapsAction(action).then(response => {
        this[action + 'ing'] = false
        if (response.ok) {
          return response.json()
        } else {
          this.$toast.open(
            {
              message: `Errore ${response.status} nell'esecuzione del comando ${action}`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
      }).then(data => {
        this.$toast.open(
          {
            message: message,
            type: 'success',
            position: 'top-left'
          }
        )
        if (reroute) {
          this.$router.push({ path: `/w20/${data.id_w20}`})
        } else {
          this.fetchData()
        }
      }).catch((error) => {
        this[action + 'ing'] = false
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    async fetchPatch(id, endpoint, payload) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w20/${endpoint}/${id}/`,
        {
          method: 'PATCH',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    async bulkUpdateW20(payload) {
        //console.log('bulkUpdateW20--',payload)
        const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w20/bulletins/bulk_update/`,
        {
          method: 'POST',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
  }
}
</script>