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
          :href="'/api/w32/pdf/' + defense.id_w32"
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
          v-if="defense.status === '0' && state.username"
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
        <button
          v-if="defense.status === '1' && state.username && defense.data_emissione.substring(0, 10) === today"
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
          v-if="defense.status === '0' && state.username"
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
      <h1>Bollettino Defense {{ defense.numero_bollettino }}</h1>
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="defense.status == 1">
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
            :value="getDateFormatted(defense.data_emissione, false)"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_validita">Data aggiornamento
          <Datepicker
            v-model="defense.data_validita"
            :disabled="readonly"
            :style="readonly ? '--dp-disabled-color: #e9ecef' : '--dp-background-color: white'"
            format="dd/MM/yyyy"
            auto-apply
            @update:model-value="saveW32(defense.data_validita, defense.id_w32, 'data_validita')"
          />
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_simulazione">data previsione
          <Datepicker
            v-model="defense.data_simulazione"
            :disabled="readonly"
            :style="readonly ? '--dp-disabled-color: #e9ecef' : '--dp-background-color: white'"
            format="dd/MM/yyyy"
            auto-apply
            @update:model-value="saveW32(defense.data_simulazione, defense.id_w32, 'data_simulazione')"
          />
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="ora_simulazione">ora previsione
          <input
            id="ora_simulazione"
            :readonly="readonly"
            class="form-control"
            name="ora_simulazione"
            type="text"
            :value="defense.ora_simulazione"
            @change="saveW32($event.target.value, defense.id_w32, 'ora_simulazione')"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_osservazione">data osservazione
          <Datepicker
            v-model="defense.data_osservazione"
            :disabled="readonly"
            :style="readonly ? '--dp-disabled-color: #e9ecef' : '--dp-background-color: white'"
            format="dd/MM/yyyy"
            auto-apply
            @update:model-value="saveW32(defense.data_osservazione, defense.id_w32, 'data_osservazione')"
          />
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="ora_osservazione">ora osservazione
          <input
            id="ora_osservazione"
            :readonly="readonly"
            class="form-control"
            name="ora_osservazione"
            type="text"
            :value="defense.ora_osservazione"
            @change="saveW32($event.target.value, defense.id_w32, 'ora_osservazione')"
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
            :value="getDateFormatted(defense.last_update)"
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
            :value="defense.username"
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
              id="pills-mbacini-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-mbacini"
              type="button"
              role="tab"
              aria-controls="pills-mbacini"
              aria-selected="false"
            >
              Macro Bacini
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
              Mappe
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-mappembacini-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-mappembacini"
              type="button"
              role="tab"
              aria-controls="pills-mappembacini"
              aria-selected="false"
            >
              Mappe Macro Bacini
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
              <table class="table">
                <thead>
                  <tr>
                    <th scope="col">
                      Aree di <br>allertamento<br> Regionale
                    </th>
                    <th scope="col">
                      Scenario ultime 24 ore
                    </th>
                    <th scope="col">
                      Scenario oggi
                    </th>
                    <th scope="col">
                      Scenario domani
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="area in defense.w32data_set"
                    :key="area.id_w32"
                  >
                    <th scope="row">
                      {{ area.id_w32_zone.descrizione }}
                    </th>
                    <CellPericolo
                      :area="area"
                      :campo="'livello_criticita_oss'"
                      :pericolo="pericolo"
                      :readonly="readonly"
                      @change-pericolo="saveW32DataPericolo"
                    />
                    <CellPericolo
                      :area="area"
                      :campo="'livello_criticita_prev_oggi'"
                      :pericolo="pericolo"
                      :readonly="readonly"
                      @change-pericolo="saveW32DataPericolo"
                    />
                    <CellPericolo
                      :area="area"
                      :campo="'livello_criticita_prev_domani'"
                      :pericolo="pericolo"
                      :readonly="readonly"
                      @change-pericolo="saveW32DataPericolo"
                    />
                  </tr>
                  <tr>
                    <td colspan="5">
                      <label for="situazione_evoluzione">situazione evoluzione</label><br>
                      <textarea
                        id="situazione_evoluzione"
                        v-model="defense.situazione_evoluzione"
                        name="situazione_evoluzione"
                        rows="3"
                        cols="100"
                        :readonly="readonly"
                        @change="saveW32(defense.situazione_evoluzione, defense.id_w32, 'situazione_evoluzione')"
                      />
                    </td>
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
            id="pills-mbacini"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-mbacini-tab"
          >
            <div class="col-md-12 mb-3">
              <table class="table">
                <thead>
                  <tr>
                    <th scope="col">
                      N°
                    </th>
                    <th scope="col">
                      Area d'allerta
                    </th>
                    <th scope="col">
                      Macrobacino
                    </th>
                    <th scope="col">
                      Scenario ultime 24 ore
                    </th>
                    <th scope="col">
                      Scenario oggi
                    </th>
                    <th scope="col">
                      Scenario domani
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="area in defense.w32mbacinidata_set"
                    :key="area.id_w32"
                  >
                    <th scope="row">
                      {{ area.id_w32_mbacini.id_w32_mbacini }}
                    </th>
                    <th scope="row">
                      {{ area.id_w32_mbacini.area }}
                    </th>
                    <th scope="row">
                      {{ area.id_w32_mbacini.descrizione }}
                    </th>
                    <CellPericoloMbacini
                      :area="area"
                      :campo="'livello_criticita_oss_mbacini'"
                      :pericolombacini="pericolombacini"
                      :readonly="readonly"
                      @change-pericolombacini="saveW32MbaciniDataPericolo"
                    />
                    <CellPericoloMbacini
                      :area="area"
                      :campo="'livello_criticita_prev_oggi_mbacini'"
                      :pericolombacini="pericolombacini"
                      :readonly="readonly"
                      @change-pericolombacini="saveW32MbaciniDataPericolo"
                    />
                    <CellPericoloMbacini
                      :area="area"
                      :campo="'livello_criticita_prev_domani_mbacini'"
                      :pericolombacini="pericolombacini"
                      :readonly="readonly"
                      @change-pericolombacini="saveW32MbaciniDataPericolo"
                    />
                  </tr>
                </tbody>
              </table>
            </div>  <!--col-->
          </div>

          <div
            id="pills-annotazione"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-annotazione-tab"
          >
            <div class="col-md-12 mb-3">
              <label for="note">Note</label><br>
              <textarea
                id="note"
                v-model="defense.note"
                name="note"
                rows="3"
                cols="100"
                :readonly="readonly"
                @change="saveW32(defense.note, defense.id_w32, 'note')"
              />
            </div>
          </div>
          <div
            id="pills-mappembacini"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-mappembacini-tab"
          >
            <div class="col-md-12 mb-3">
              <div>
                <div class="row">
                  <div class="col-sm">
                    SCENARIO PEGGIORE
                  </div>
                  <div class="col-sm">
                    SCENARIO ULTIME 24 ORE
                  </div>
                  <div class="col-sm">
                    SCENARIO OGGI
                  </div>
                  <div class="col-sm">
                    SCENARIO DOMANI
                  </div>
                </div>
                <div class="row">
                  <div class="col-sm">
                    <MapDefenseMacrobacini
                      :orography="true"
                      :rivers="false"
                      :provinces="false"
                      :capitals="false"
                      :layer="true"
                      :venue-data="max_livello_criticita_prev_mbacini"
                      :defensedata="defensembacini_prev_max"
                    />
                  </div>
                  <div class="col-sm">
                    <MapDefenseMacrobacini
                      :orography="true"
                      :rivers="false"
                      :provinces="false"
                      :capitals="false"
                      :layer="true"
                      :venue-data="livello_criticita_oss_mbacini"
                      :defensedata="defensembacini_oss"
                    />
                  </div>
                  <div class="col-sm">
                    <MapDefenseMacrobacini
                      :orography="true"
                      :rivers="false"
                      :provinces="false"
                      :capitals="false"
                      :layer="true"
                      :venue-data="livello_criticita_prev_oggi_mbacini"
                      :defensedata="defensembacini_prev_oggi"
                    />
                  </div>
                  <div class="col-sm">
                    <MapDefenseMacrobacini
                      :orography="true"
                      :rivers="false"
                      :provinces="false"
                      :capitals="false"
                      :layer="true"
                      :venue-data="livello_criticita_prev_domani_mbacini"
                      :defensedata="defensembacini_prev_domani"
                    />
                  </div>
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
              <div>
                <div class="row">
                  <div class="col-sm">
                    SCENARIO ULTIME 24 ORE
                  </div>
                  <div class="col-sm">
                    SCENARIO OGGI
                  </div>
                  <div class="col-sm">
                    SCENARIO DOMANI
                  </div>
                </div>
                <div class="row">
                  <div class="col-sm">
                    <MapDefense
                      :orography="true"
                      :rivers="false"
                      :provinces="false"
                      :capitals="false"
                      :layer="true"
                      :venue-data="livello_criticita_oss"
                      :defensedata="defense_oss"
                    />
                  </div>
                  <div class="col-sm">
                    <MapDefense
                      :orography="true"
                      :rivers="false"
                      :provinces="false"
                      :capitals="false"
                      :layer="true"
                      :venue-data="livello_criticita_prev_oggi"
                      :defensedata="defense_prev_oggi"
                    />
                  </div>
                  <div class="col-sm">
                    <MapDefense
                      :orography="true"
                      :rivers="false"
                      :provinces="false"
                      :capitals="false"
                      :layer="true"
                      :venue-data="livello_criticita_prev_domani"
                      :defensedata="defense_prev_domani"
                    />
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
import CellPericoloMbacini from './CellPericoloMbacini.vue'
import MapDefense from './MapDefense.vue'
import MapDefenseMacrobacini from './MapDefenseMacrobacini.vue'

export default {

  name: 'DefenseBulletin',
  components: {
    CellPericolo,
    CellPericoloMbacini,
    MapDefense,
    MapDefenseMacrobacini,
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
      defense: {},
      pericolo: [],
      pericolombacini: [],
      defensedata: {},
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
    livello_criticita_oss(){
      let vd = { }
      if (this.defense.w32data_set !== undefined) {
        this.defense.w32data_set.forEach(area => {
          vd[area.id_w32_zone.id_w32_zone] = this.coloreHtml(area.livello_criticita_oss)
        })
      }
      return vd
    },
    livello_criticita_prev_oggi(){
      let vd = { }
      if (this.defense.w32data_set !== undefined) {
        this.defense.w32data_set.forEach(area => {
          vd[area.id_w32_zone.id_w32_zone] = this.coloreHtml(area.livello_criticita_prev_oggi)
        })
      }
      return vd
    },
    livello_criticita_prev_domani(){
      let vd = { }
      if (this.defense.w32data_set !== undefined) {
        this.defense.w32data_set.forEach(area => {
          vd[area.id_w32_zone.id_w32_zone] = this.coloreHtml(area.livello_criticita_prev_domani)
        })
      }
      return vd
    },
    livello_criticita_oss_mbacini(){
      let vd = { }
      if (this.defense.w32mbacinidata_set !== undefined) {
        this.defense.w32mbacinidata_set.forEach(area => {
          vd[area.id_w32_mbacini.id_w32_mbacini] = this.coloreHtmlMbacini(area.livello_criticita_oss)
        })
      }
      return vd
    },
    livello_criticita_prev_oggi_mbacini(){
      let vd = { }
      if (this.defense.w32mbacinidata_set !== undefined) {
        this.defense.w32mbacinidata_set.forEach(area => {
          vd[area.id_w32_mbacini.id_w32_mbacini] = this.coloreHtmlMbacini(area.livello_criticita_prev_oggi)
        })
      }
      return vd
    },
    livello_criticita_prev_domani_mbacini(){
      let vd = { }
      if (this.defense.w32mbacinidata_set !== undefined) {
        this.defense.w32mbacinidata_set.forEach(area => {
          vd[area.id_w32_mbacini.id_w32_mbacini] = this.coloreHtmlMbacini(area.livello_criticita_prev_domani)
        })
      }
      return vd
    },
    max_livello_criticita_prev_mbacini(){
      let vd = { }
      if (this.defense.w32mbacinidata_set !== undefined) {
        this.defense.w32mbacinidata_set.forEach(area => {
          if(area.livello_criticita_oss==='S' || area.livello_criticita_prev_oggi==='S' || area.livello_criticita_prev_domani==='S'){
            vd[area.id_w32_mbacini.id_w32_mbacini] = this.coloreHtmlMbacini("S")
          }else if(area.livello_criticita_oss==='np' && area.livello_criticita_prev_oggi==='np' && area.livello_criticita_prev_domani==='np'){
            vd[area.id_w32_mbacini.id_w32_mbacini] = this.coloreHtmlMbacini("np")
          }else{ 
            vd[area.id_w32_mbacini.id_w32_mbacini] = this.coloreHtmlMbacini("-")
          }
        })
      }
      return vd
    },
    defense_oss(){
      let vd = { }
      if (this.defense.w32data_set !== undefined) {
        this.defense.w32data_set.forEach(area => {
          let data = { }
          data['criticita'] = area.livello_criticita_oss
          data['criticita_color'] = this.coloreHtml(area.livello_criticita_oss)
          vd[area.id_w32_zone.id_w32_zone] = data
        })
      }
      return vd
    },
    defense_prev_oggi(){
      let vd = { }
      if (this.defense.w32data_set !== undefined) {
        this.defense.w32data_set.forEach(area => {
          let data = { }
          data['criticita'] = area.livello_criticita_prev_oggi
          data['criticita_color'] = this.coloreHtml(area.livello_criticita_prev_oggi)
          vd[area.id_w32_zone.id_w32_zone] = data
        })
      }
      return vd
    },
    defense_prev_domani(){
      let vd = { }
      if (this.defense.w32data_set !== undefined) {
        this.defense.w32data_set.forEach(area => {
          let data = { }
          data['criticita'] = area.livello_criticita_prev_domani
          data['criticita_color'] = this.coloreHtml(area.livello_criticita_prev_domani)
          vd[area.id_w32_zone.id_w32_zone] = data
        })
      }
      return vd
    },
    defensembacini_prev_domani(){
      let vd = { }
      if (this.defense.w32mbacinidata_set !== undefined) {
        this.defense.w32mbacinidata_set.forEach(area => {
          let data = { }
          data['criticita'] = area.livello_criticita_prev_domani
          data['criticita_color'] = this.coloreHtmlMbacini(area.livello_criticita_prev_domani)
          vd[area.id_w32_mbacini.id_w32_mbacini] = data
        })
      }
      return vd
    },
    defensembacini_oss(){
      let vd = { }
      if (this.defense.w32mbacinidata_set !== undefined) {
        this.defense.w32mbacinidata_set.forEach(area => {
          let data = { }
          data['criticita'] = area.livello_criticita_oss
          data['criticita_color'] = this.coloreHtmlMbacini(area.livello_criticita_oss)
          vd[area.id_w32_mbacini.id_w32_mbacini] = data
        })
      }
      return vd
    },
    defensembacini_prev_oggi(){
      let vd = { }
      if (this.defense.w32mbacinidata_set !== undefined) {
        this.defense.w32mbacinidata_set.forEach(area => {
          let data = { }
          data['criticita'] = area.livello_criticita_prev_oggi
          data['criticita_color'] = this.coloreHtmlMbacini(area.livello_criticita_prev_oggi)
          vd[area.id_w32_mbacini.id_w32_mbacini] = data
        })
      }
      return vd
    },
    defensembacini_prev_max(){
      let vd = { }
      if (this.defense.w32mbacinidata_set !== undefined) {
        this.defense.w32mbacinidata_set.forEach(area => {
          let data = { }
          if(area.livello_criticita_oss==='S' || area.livello_criticita_prev_oggi==='S' || area.livello_criticita_prev_domani==='S'){
            data['criticita'] = "S"
            data['criticita_color'] = this.coloreHtmlMbacini("S")
            vd[area.id_w32_mbacini.id_w32_mbacini] = data
          }else if(area.livello_criticita_oss==='np' && area.livello_criticita_prev_oggi==='np' && area.livello_criticita_prev_domani==='np'){
            data['criticita'] = "np"
            data['criticita_color'] = this.coloreHtmlMbacini("np")
            vd[area.id_w32_mbacini.id_w32_mbacini] = data
          }else{ 
            data['criticita'] = "-"
            data['criticita_color'] = this.coloreHtmlMbacini("-")
            vd[area.id_w32_mbacini.id_w32_mbacini] = data
          }
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
      if (parametro == 'np')
        colore = '#FFFFFF'
      else if (parametro == 'A')
        colore = '#A6A6A6'
      else if (parametro == 'I')
        colore = '#99CCFF'
      else if (parametro == 'P')
        colore = '#9999FF'
      else if (parametro == 'D')
        colore = '#9900FF'
      return colore
    },
    coloreHtmlMbacini(parametro) {
      var colore = 'red'
      if (parametro == 'np')
        colore = '#FFFFFF'
      else if (parametro == '-')
        colore = '#A6A6A6'
      else if (parametro == 'S')
        colore = '#4999CE'
      return colore
    },
    async fetchData () {
      this.defense_id = this.id
      this.pericolo  = await this.fetchPericolo()
      this.pericolombacini  = await this.fetchPericolombacini()
      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
      this.fetchDefense().then(response => {
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
        this.defense = data
        this.readonly = (this.defense.status === '1'  || this.defense.status === '2' || !this.state.username)
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
    async fetchDefense () {
      // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
      const response = await fetch('/api/w32/bulletins/' + this.defense_id + '/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    async fetchPericolo () {
      try {
        const response = await fetch('/api/w32/pericolo/', {
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
    async fetchPericolombacini () {
      try {
        const response = await fetch('/api/w32/pericolombacini/', {
          headers: {
            accept: 'application/json'
          }
        })
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero del Pericolombacini`,
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
    saveW32(newValue, id_w32, campo) {
      this.saving = true
      //data_validata
      if (campo==="data_validita") {
        let month = String(newValue.getMonth() + 1);
        let day = String(newValue.getDate());
        const year = String(newValue.getFullYear());

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        newValue=`${year}-${month}-${day}`;
        this.defense.data_validita=newValue;
      }
      //data_simulazione
      if (campo==="data_simulazione") {
        if(newValue!=null){
          let month = String(newValue.getMonth() + 1);
          let day = String(newValue.getDate());
          const year = String(newValue.getFullYear());

          if (month.length < 2) month = '0' + month;
          if (day.length < 2) day = '0' + day;

          newValue=`${year}-${month}-${day}`;
        }else{
          newValue='n.d.'
        }
        this.defense.data_simulazione=newValue;
      }
      //data_osservazione
      if (campo==="data_osservazione") {
        if(newValue!=null){
          //console.log('newValue   ',newValue)
          let month = String(newValue.getMonth() + 1);
          let day = String(newValue.getDate());
          const year = String(newValue.getFullYear());

          if (month.length < 2) month = '0' + month;
          if (day.length < 2) day = '0' + day;

          newValue=`${year}-${month}-${day}`;
        }else{
          newValue='n.d.'
        }
        this.defense.data_osservazione=newValue;
      }
      //ora_simulazione
      if(campo==="ora_simulazione"){
        this.defense.ora_simulazione=newValue;
      }
      //ora_osservazione
      if(campo==="ora_osservazione"){
        this.defense.ora_osservazione=newValue;
      }
      var today = new Date();
      let ore_emissione = today.getHours();
      if(today.getMinutes()>0) {
        ore_emissione = today.getHours()+1;
      }
      const payload = { }
      if (campo) {
        payload[campo] = newValue
      }
      payload['ora_emissione'] = ore_emissione + ":00"
      payload['id_w32'] = id_w32
      payload['username'] = store.state.username
      this.bulkUpdateW32(payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio',
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
        this.defense.last_update = data.last_update
        this.defense.username = store.state.username
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
    saveW32DataPericolo(newValue, id_w32_zone, campo) {
      let myW32zone = this.defense.w32data_set.find(w32data => {
        return w32data.id_w32_zone.id_w32_zone === id_w32_zone
      })
      myW32zone[campo] = newValue
      const payload = { }
      payload[campo] = newValue
      this.fetchPatch(myW32zone.id_w32_data, 'data', payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio',
              type: 'error',
              position: 'top-left'
            }
          )
        } else {
          this.saveW32(null, this.defense.id_w32, null)
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
    saveW32MbaciniDataPericolo(newValue, id_w32_mbacini, campo) {
      let myW32mbacini = this.defense.w32mbacinidata_set.find(w32mbacinidata => {
        return w32mbacinidata.id_w32_mbacini.id_w32_mbacini === id_w32_mbacini
      })
      myW32mbacini[campo] = newValue
      const payload = { }
      payload[campo] = newValue
      //console.log('payload[campo]===',payload[campo])
      this.fetchPatch(myW32mbacini.id_w32_mbacini_data, 'datambacini', payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio',
              type: 'error',
              position: 'top-left'
            }
          )
        } else {
          this.saveW32(null, this.defense.id_w32, null)
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
        api.fetchBulletinDelete(this.defense_id, 'w32/bulletins', store).then(response => {
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
    async fetchDefenseAction (action) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w32/bulletins/${this.defense_id}/${action}/`
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
      this.fetchDefenseAction(action).then(response => {
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
          //this.$router.push({ path: `/w32/${data.id_w32}`})
          this.$router.push({ path: `/w32/`})
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
      //console.log('id?',id)
      //console.log('endpoint?',endpoint)
      //console.log('id?',id)
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w32/${endpoint}/${id}/`,
        {
          method: 'PATCH',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    async bulkUpdateW32(payload) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w32/bulletins/bulk_update/`,
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
