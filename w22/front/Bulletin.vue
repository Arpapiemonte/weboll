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
        <a
          class="btn btn-outline-primary"
          :href="'/api/w22/pdf/' + piene.id_w22"
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
        <a
          class="btn btn-outline-primary"
          :href="'/api/w22/comunicazione_png/' + piene.id_w22"
          target="_blank"
          role="button"
        >
          <img
            src="~bootstrap-icons/icons/file-earmark-image.svg"
            alt="PDF icon"
            width="18"
            height="18"
          > COMUNICAZIONE
        </a>
        <button
          v-if="piene.status === '0' && state.username"
          :disabled="sending"
          type="button"
          class="btn btn-outline-success"
          @click="execute_timeout('send', false, 'Bollettino inviato')"
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
        <!-- <button
          v-if="piene.status === '1' && state.username"
          :disabled="reopening"
          type="button"
          class="btn btn-outline-success"
          @click="execute('reopen', true, 'Bollettino inviato')"
        >
          <span v-if="reopening">
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
        </button>-->
        <button
          v-if="piene.status === '1' && state.username && piene.data_emissione.substring(0, 10) === today"
          type="button"
          class="btn btn-outline-warning"
          @click="execute('reopen', true, 'Bollettino riaperto')"
        >
          <span v-if="reopening">
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
          v-if="piene.status === '0' && state.username"
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
      <h1>Bollettino Piene {{ piene.numero_bollettino }}</h1>
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato</label>
        <span v-if="piene.status == 1">
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
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_emissione">Data emissione</label>
        <input
          id="data_emissione"
          disabled
          class="form-control"
          name="data_emissione"
          type="text"
          :value="piene.data_emissione"
        >
      </div>
      <div class="col-md-2 mb-3">
        <label for="ora_emissione">ora emissione</label>
        <input
          id="ora_emissione"
          :readonly="readonly"
          class="form-control"
          name="ora_emissione"
          type="text"
          :value="piene.ora_emissione"
          @change="saveW22($event.target.value, piene.id_w22, 'ora_emissione')"
        >
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_validita">Data Aggiornamento</label>
        <Datepicker
          v-model="piene.data_validita"
          :disabled="readonly"
          :style="readonly ? '--dp-disabled-color: #e9ecef' : '--dp-background-color: white'"
          format="dd/MM/yyyy"
          auto-apply
          @update:model-value="saveW22(piene.data_validita, piene.id_w22, 'data_validita')"
        />
      </div>
      <div class="col-md-2 mb-3">
        <label for="last_update">Ultima modifica</label>
        <input
          id="last_update"
          disabled
          class="form-control"
          name="last_update"
          type="text"
          :value="getDateFormatted(piene.last_update)"
        >
      </div>
      <div class="col-md-2 mb-3">
        <label for="username">Autore</label>
        <input
          id="username"
          disabled
          class="form-control"
          name="username"
          type="text"
          :value="piene.username"
        >
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
                id="pills-annotazione-tab"
                class="nav-link"
                data-bs-toggle="pill"
                data-bs-target="#pills-annotazione"
                type="button"
                role="tab"
                aria-controls="pills-annotazione"
                aria-selected="false"
              >
                Annotazione
              </button>
            </li>

            <li
              class="nav-item"
              role="presentation"
            >
              <button
                id="pills-mappa-tab"
                class="nav-link"
                data-bs-toggle="pill"
                data-bs-target="#pills-mappa"
                type="button"
                role="tab"
                aria-controls="pills-mappa"
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
                id="pills-mappa_dettaglio-tab"
                class="nav-link"
                data-bs-toggle="pill"
                data-bs-target="#pills-mappa_dettaglio"
                type="button"
                role="tab"
                aria-controls="pills-mappa_dettaglio"
                aria-selected="false"
              >
                Mappa Dettaglio
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
              <div class="col-xl-12 col-md-12 mb-3">
                <div class="form-check, col-md-12 mb-3">
                  <input
                    id="0"
                    v-model="piene.pdf_ordinario"
                    :disabled="readonly"
                    type="radio"
                    value="0"
                    @change="saveW22('0', piene.id_w22, 'pdf_ordinario')"
                  >
                  <label for="one">Bollettino straordinario</label>
                  <br>
                  <input
                    id="1"
                    v-model="piene.pdf_ordinario"
                    :disabled="readonly"
                    type="radio"
                    value="1"
                    @change="saveW22('1', piene.id_w22, 'pdf_ordinario')"
                  >
                  <label for="two">Bollettino classico</label>
                </div>
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <table>
                      <tbody>
                        <tr>
                          <td>
                            <label for="situazione_evoluzione">Situazione ed evoluzione</label><br>
                            <textarea
                              id="situazione_evoluzione"
                              v-model="piene.situazione_evoluzione"
                              class="form-control"
                              name="situazione_evoluzione"
                              rows="2"
                              cols="200"
                              :readonly="readonly"
                              @change="saveW22(piene.situazione_evoluzione, piene.id_w22, 'situazione_evoluzione')"
                            />
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>


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
                        VALORI OSSERVATI
                      </th>
                      <th
                        class="text-center"
                        colspan="4"
                      >
                        PREVISIONE DI CRITICITA'
                      </th>
                      <th
                        class="text-center"
                        colspan="3"
                      >
                        PORTATE DI RIFERIMENTO (mc/s)
                      </th>
                      <th
                        class="text-center"
                        colspan="2"
                      >
                        MASSIMO STORICO
                      </th>
                    </tr>
                    <tr>
                      <th scope="col">
                        Corso d'acqua
                      </th>
                      <th scope="col">
                        Stazione
                      </th>
                      <th scope="col">
                        Tendenza 6h
                      </th>
                      <th scope="col">
                        Portata
                      </th>
                      <th scope="col">
                        Criticità<br>attuale
                      </th>
                      <th scope="col">
                        00-12h
                      </th>
                      <th scope="col">
                        12-24h
                      </th>
                      <th scope="col">
                        24-36h
                      </th>
                      <th scope="col">
                        Tendenza dopodomani
                      </th>
                      <th scope="col">
                        Liv 1
                      </th>
                      <th scope="col">
                        Liv 2
                      </th>
                      <th scope="col">
                        Liv 3
                      </th>
                      <th scope="col">
                        data
                      </th>
                      <th scope="col">
                        valore
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="area in piene.w22data_set"
                      :key="area.id_w22_data"
                    >
                      <th scope="row">
                        {{ area.id_w22_zone.corso_acqua }}
                      </th>
                      <th scope="row">
                        {{ area.id_w22_zone.denominazione_stazione }}
                      </th>
                      <td>
                        <CellTendenza
                          :area="area"
                          :campo="'tendenza6hprecedenti'"
                          :tendenza="tendenza"
                          :readonly="readonly"
                          @change-tendenza="saveW22DataSelect"
                        />
                      </td>
                      <td>
                        <input
                          id="portata_attesa"
                          :readonly="readonly"
                          class="form-control"
                          name="portata_attesa"
                          type="text"
                          :value="area.portata_attesa"
                          @change="saveW22DataSelect($event.target.value,area.id_w22_data, area.id_w22_zone.id_w22_zone, 'portata_attesa')"
                        >
                      </td>
                      <td>
                        <CellCriticita
                          :area="area"
                          :campo="'criticita_attesa'"
                          :criticita="criticita"
                          :readonly="readonly"
                          @change-criticita="saveW22DataSelect"
                        />
                      </td>
                      <td>
                        <CellCriticita
                          :area="area"
                          :campo="'prev_crit12h'"
                          :criticita="criticita"
                          :readonly="readonly"
                          @change-criticita="saveW22DataSelect"
                        />
                      </td>
                      <td>
                        <CellCriticita
                          :area="area"
                          :campo="'prev_crit24h'"
                          :criticita="criticita"
                          :readonly="readonly"
                          @change-criticita="saveW22DataSelect"
                        />
                      </td>
                      <td>
                        <CellCriticita
                          :area="area"
                          :campo="'prev_crit36h'"
                          :criticita="criticita"
                          :readonly="readonly"
                          @change-criticita="saveW22DataSelect"
                        />
                      </td>
                      <td>
                        <CellTendenza
                          :area="area"
                          :campo="'tend48h'"
                          :tendenza="tendenza"
                          :readonly="readonly"
                          @change-tendenza="saveW22DataSelect"
                        />
                      </td>
                      <td>{{ area.codice1 }}</td>
                      <td>{{ area.codice2 }}</td>
                      <td>{{ area.codice3 }}</td>
                      <td>{{ area.data_massimo_storico }}</td>
                      <td>{{ area.valore_massimo_storico }}</td>
                    </tr>
                  </tbody>
                </table>
                <div class="col-xl-9 col-md-14 mb-3">
                  <div
                    class="sticky-top pt-5"
                    style="z-index: 0;"
                  />
                </div> <!-- col -->
              </div>  <!--col-->
            </div>

            <div
              id="pills-annotazione"
              class="tab-pane fade"
              role="tabpanel"
              aria-labelledby="pills-annotazione-tab"
            >
              <div class="col-md-12 mb-3">
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <table>
                      <tbody>
                        <tr>
                          <td>
                            <label for="annotazione">Annotazione</label><br>
                            <textarea
                              id="annotazione"
                              v-model="piene.annotazione"
                              class="form-control"
                              name="annotazione"
                              rows="2"
                              cols="200"
                              :readonly="readonly"
                              @change="saveW22(piene.annotazione, piene.id_w22, 'annotazione')"
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
              id="pills-mappa"
              class="tab-pane fade"
              role="tabpanel"
              aria-labelledby="pills-mappa-tab"
            >
              <div class="col-md-12 mb-3">
                <div class="row">
                  <div class="col-md-8 mb-3">
                    <h3>Criticità massima</h3>
                    <MapPiene
                      :venue-data="criticita_massima"
                      :pienedata="criticita_tot"
                    />
                  </div>
                </div>
              </div>
            </div>
            <div
              id="pills-mappa_dettaglio"
              class="tab-pane fade"
              role="tabpanel"
              aria-labelledby="pills-mappa_dettaglio-tab"
            >
              <div class="col-md-12 mb-3">
                <div class="row">
                  <div class="col-md-3 mb-3">
                    <h3>Criticità attuale</h3>
                    <MapPieneDettaglio
                      :venue-data="criticita_attuale"
                      :pienedata="criticita_attuale_val"
                    />
                  </div>
                  <div class="col-md-3 mb-3">
                    <h3>Criticità 12h</h3>
                    <MapPieneDettaglio
                      :venue-data="criticita_prev_crit12h"
                      :pienedata="criticita_prev_crit12h_val"
                    />
                  </div>

                  <div class="col-md-3 mb-3">
                    <h3>Criticità 24h</h3>
                    <MapPieneDettaglio
                      :venue-data="criticita_prev_crit24h"
                      :pienedata="criticita_prev_crit24h_val"
                    />
                  </div>
                  <div class="col-md-3 mb-3">
                    <h3>Criticità 36h</h3>
                    <MapPieneDettaglio
                      :venue-data="criticita_prev_crit36h"
                      :pienedata="criticita_prev_crit36h_val"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div> <!-- row -->
    </div> <!-- end row -->
  </div>
</template>

<script>
import api from '@/api'
import store from '@/store'
import CellTendenza from './CellTendenza.vue'
import MapPiene from './MapPiene.vue'
import MapPieneDettaglio from './MapPieneDettaglio.vue'
import CellCriticita from './CellCriticita.vue'

export default {
  name: 'PieneBulletin',
  components: {
    CellTendenza,
    CellCriticita,
    MapPiene,
    MapPieneDettaglio
  },
  props: {
    id: {
      type: String,
      default: () => ''
    },
  },
  data () {
  // non reactive properties
    return {
      // reactive properties
      piene: {
        numero_bollettino: "aaaaaaaa"
      },
      tendenza: [],
      criticita: [],
      state: store.state,
      readonly: true,
      sending: false,
      saving: false,
      reopening: false
   }
 },
 computed: {
   today() {
      // returns today in 2021-04-22 format
      let d = new Date()
      return d.toISOString().substring(0, 10)
    },
   criticita_tot() {
      let vd = { }
      if (this.piene.w22data_set !== undefined) {
        this.piene.w22data_set.forEach(area => {
          let data = { }
          data['prev_crit12h'] = area.prev_crit12h
          data['prev_crit24h'] = area.prev_crit24h
          data['prev_crit36h'] = area.prev_crit36h
          data['criticita'] = area.criticita_attesa
          data['criticita_color'] = this.coloreHtml(area.criticita_attesa)
          data['prev_crit12h_color'] = this.coloreHtml(area.prev_crit12h)
          data['prev_crit24h_color'] = this.coloreHtml(area.prev_crit24h)
          data['prev_crit36h_color'] = this.coloreHtml(area.prev_crit36h)
          vd[area.id_w22_zone.id_w22_zone] = data
        })
      }
      return vd
   },
   criticita_massima () {
      let vd = { }
      if (this.piene.w22data_set !== undefined) {
        this.piene.w22data_set.forEach(area => {
          vd[area.id_w22_zone.id_w22_zone] = this.coloreHtml(this.massimo_crit(area, ['criticita_attesa','prev_crit12h', 'prev_crit24h','prev_crit36h']))
          area.massimo_previsione=this.massimo_crit(area, ['criticita_attesa','prev_crit12h', 'prev_crit24h','prev_crit36h'])
        })
      }
      return vd
   },
   criticita_attuale_val () {
      let vd = { }
      if (this.piene.w22data_set !== undefined) {
        this.piene.w22data_set.forEach(area => {
          vd[area.id_w22_zone.id_w22_zone] = area.criticita_attesa
        })
      }
      return vd
   },
   criticita_prev_crit12h_val () {
      let vd = { }
      if (this.piene.w22data_set !== undefined) {
        this.piene.w22data_set.forEach(area => {
          vd[area.id_w22_zone.id_w22_zone] = area.prev_crit12h
        })
      }
      return vd
   },
   criticita_prev_crit24h_val () {
      let vd = { }
      if (this.piene.w22data_set !== undefined) {
        this.piene.w22data_set.forEach(area => {
          vd[area.id_w22_zone.id_w22_zone] = area.prev_crit24h
        })
      }
      return vd
   },
   criticita_prev_crit36h_val () {
      let vd = { }
      if (this.piene.w22data_set !== undefined) {
        this.piene.w22data_set.forEach(area => {
          vd[area.id_w22_zone.id_w22_zone] = area.prev_crit36h
        })
      }
      return vd
   },
   criticita_attuale () {
      let vd = { }
      if (this.piene.w22data_set !== undefined) {
        this.piene.w22data_set.forEach(area => {
          vd[area.id_w22_zone.id_w22_zone] = this.coloreHtml(area.criticita_attesa)
        })
      }
      return vd
   },
   criticita_prev_crit12h () {
      let vd = { }
      if (this.piene.w22data_set !== undefined) {
        this.piene.w22data_set.forEach(area => {
          vd[area.id_w22_zone.id_w22_zone] = this.coloreHtml(area.prev_crit12h)
        })
      }
      return vd
   },
   criticita_prev_crit24h () {
      let vd = { }
      if (this.piene.w22data_set !== undefined) {
        this.piene.w22data_set.forEach(area => {
          vd[area.id_w22_zone.id_w22_zone] = this.coloreHtml(area.prev_crit24h)
        })
      }
      return vd
   },
   criticita_prev_crit36h () {
      let vd = { }
      if (this.piene.w22data_set !== undefined) {
        this.piene.w22data_set.forEach(area => {
          vd[area.id_w22_zone.id_w22_zone] = this.coloreHtml(area.prev_crit36h)
        })
      }
      return vd
   },
 },
  watch: {
    '$route': 'fetchData',
  },
 created() {
  // https://vuejs.org/v2/guide/instance.html
    this.fetchData()
  },
  methods: {
    coloreHtml(parametro) {
      var colore = 'red'
      if (parametro == 'A')
        colore = '#6EBB00'
      else if (parametro == 'E')
        colore = '#FF0000'
      else if (parametro == 'M')
        colore = '#FFA500'
      else if (parametro == 'O')
        colore = '#FFFF00'
      return colore
    },

    async fetchData () {
      this.piene_id = this.id
      this.tendenza  =  await this.fetchTendenza()
      this.criticita  =  await this.fetchCriticita()
      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
      this.fetchPiene().then(response => {
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
        data['pippo'] = 'pluto'
        this.piene = data
        this.readonly = (this.piene.status === '1' || this.piene.status === '2' ||!this.state.username)
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
    async fetchPiene () {
      // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
      const response = await fetch('/api/w22/bulletins/' + this.piene_id + '/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    async fetchTendenza () {
      try {
        const response = await fetch('/api/w22/tendenza/', {
          headers: {
            accept: 'application/json'
          }
        })
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero del Tendenza`,
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
    async fetchCriticita () {
      try {
        const response = await fetch('/api/w22/criticita/', {
          headers: {
            accept: 'application/json'
          }
        })
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero del Criticità`,
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
    async fetchPatch(id, endpoint, payload) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w22/${endpoint}/${id}/`,
        {
          method: 'PATCH',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    massimo_crit(area, parametri) {
      let m = undefined
      parametri.forEach(parametro => {
        if (!m) {
          m = area[parametro]
        } else {
          if (area[parametro]=='E'){
              m = 'E'
          }
          else if (area[parametro]=='M'){
              if (m=='E'){
                  m='E'
              }
              else{
                  m='M'
              }
          }
          else if (area[parametro]=='O'){
              if (m=='E'){
                    m='E'
              }
              else if (m=='M'){
                  m='M'
              }
              else{
                  m='O'
              }
          }
          else if (area[parametro]=='A'){
              if (m=='E'){
                  m='E'
              }
              else if (m=='M'){
                  m='M'
              }
              else if (m=='O'){
                  m='O'
              }
              else{
                  m='A'
              }
          }
        }
      })
      return m
    },
    saveW22(newValue, id_w22, campo) {
      this.saving = true
      if (campo==="data_validita") {
        let month = String(newValue.getMonth() + 1);
        let day = String(newValue.getDate());
        const year = String(newValue.getFullYear());

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        newValue=`${year}-${month}-${day}`;
        this.piene.data_validita=newValue;

      }else if(campo==="ora_emissione"){
        this.piene.ora_emissione=newValue;
      }

      const payload = { }
      if (campo) {
        payload[campo] = newValue
      }
      payload['id_w22'] = id_w22
      payload['username'] = store.state.username
      this.bulkUpdateW22(payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio bulk',
              type: 'error',
              position: 'top-left'
            }
          )
          this.saving = false
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
        this.piene.last_update = data.last_update
        this.piene.username = store.state.username
        this.saving = false
      }).catch((error) => {
        this.$toast.open(
          {
            message: `Errore di comunicazione: ${error}`,
            type: 'error',
            position: 'top-left'
          }
        )
        this.saving = false
      })
    },
    getDateFormatted(rawString, time = true) {
      return api.getDateFormatted(rawString, time)
    },
    classe_criticita(codice_str){
      var codice_num = -1
      switch (codice_str){
        case "A":
          codice_num = 0
          break;
        case "O":
          codice_num = 1
          break;
        case "M":
          codice_num = 2
          break;
        case "E":
          codice_num = 3
          break;
        default: 
            console.log('classe_criticita classe non trovata ' + codice_str);
      }
      return codice_num
    },
    classe_criticita_reverse(codice_num){
      var codice_str = "X"
      switch (codice_num){
        case 0:
        codice_str = "A"
          break;
        case 1:
        codice_str = "O"
          break;
        case 2:
        codice_str = "M"
          break;
        case 3:
        codice_str = "E"
          break;
        default: 
            console.log('classe_criticita_reverse classe non trovata ' + codice_num);
      }
      return codice_str
    },
    // Metodo generico per salvare i dati delle select di criticita e tendenza
    saveW22DataSelect(newValue,id_w22_data, id_w22_zone, campo) {
      let myW22zone = this.piene.w22data_set.find(w22data => {
        return w22data.id_w22_zone.id_w22_zone === id_w22_zone
      })
      myW22zone[campo] = newValue
      const payload = { }
      payload[campo] = newValue
      // confronta se il valore è maggiore di massimo_previsione aggiorna anche massimo_previsione
      let max = -1
      if (this.classe_criticita(myW22zone.criticita_attesa) > max) max = this.classe_criticita(myW22zone.criticita_attesa)
      if (this.classe_criticita(myW22zone.prev_crit12h) > max) max = this.classe_criticita(myW22zone.prev_crit12h)
      if (this.classe_criticita(myW22zone.prev_crit24h) > max) max = this.classe_criticita(myW22zone.prev_crit24h)
      if (this.classe_criticita(myW22zone.prev_crit36h) > max) max = this.classe_criticita(myW22zone.prev_crit36h)
      if (this.classe_criticita(newValue) > max) max = this.classe_criticita(newValue)
      payload['massimo_previsione'] = this.classe_criticita_reverse(max)
      this.fetchPatch(myW22zone.id_w22_data, 'data', payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio',
              type: 'error',
              position: 'top-left'
            }
          )
        } else {
          this.saveW22(null, this.piene.id_w22, null)
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
        api.fetchBulletinDelete(this.piene_id, 'w22/bulletins', store).then(response => {
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
    async fetchPieneAction (action) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w22/bulletins/${this.piene_id}/${action}/`
      )
      return response
    },
    execute_timeout(action, reroute, message){
      // console.log("inizio execute_timeout")
      if (this.saving){
        console.log("saving è true faccio partire timeout")
        setTimeout(() => {
          console.log("aspetto 1 secondo finchè non finisce il salvataggio in corso")
          this.execute_timeout(action, reroute, message)
        }, 1000);
      }else{
        console.log("saving è false lancio execute")
        this.execute(action, reroute, message)
      }
      // console.log("fine execute_timeout")
    },
    execute(action, reroute, message) {
      this[action + 'ing'] = true
      console.log('action',action,reroute,message)
      this.fetchPieneAction(action).then(response => {
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
        console.log('data',data)
        this.$toast.open(
          {
            message: message,
            type: 'success',
            position: 'top-left'
          }
        )
        if (reroute) {
          this.$router.push({ path: `/w22/${data.id_w22}`})
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
    async bulkUpdateW22(payload) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w22/bulletins/bulk_update/`,
        {
          method: 'POST',
          body: JSON.stringify(payload)
        }
      )
      return response
    }
  }
}
</script>
