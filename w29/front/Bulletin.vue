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
          :href="'/api/w29/pdf/' + slops.id_w29"
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
          v-if="slops.status === '0' && state.username"
          :disabled="sending || !validity.all"
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
          v-if="slops.status === '1' && state.username && slops.data_emissione.substring(0, 10) === today"
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
          v-if="slops.status === '0' && state.username"
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
      <h1>Bollettino Slops {{ slops.numero_bollettino }}</h1>
      <div
        v-if="!validity.all"
        class="alert alert-danger"
      >
        Ci sono dei campi incompleti
      </div>
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="slops.status == 1">
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
            :value="getDateFormatted(slops.data_emissione, false)"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_validita">Data aggiornamento
          <Datepicker
            v-model="slops.data_validita"
            :disabled="readonly"
            :style="readonly ? '--dp-disabled-color: #e9ecef' : '--dp-background-color: white'"
            format="dd/MM/yyyy"
            auto-apply
            @update:model-value="saveW29(slops.data_validita, slops.id_w29, 'data_validita')"
          />
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_simulazione">data previsione
          <Datepicker
            v-model="slops.data_simulazione"
            :disabled="readonly"
            :style="readonly ? '--dp-disabled-color: #e9ecef' : '--dp-background-color: white'"
            format="dd/MM/yyyy"
            auto-apply
            @update:model-value="saveW29(slops.data_simulazione, slops.id_w29, 'data_simulazione')"
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
            :value="slops.ora_simulazione"
            @change="saveW29($event.target.value, slops.id_w29, 'ora_simulazione')"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_osservazione">data osservazione
          <Datepicker
            v-model="slops.data_osservazione"
            :disabled="readonly"
            :style="readonly ? '--dp-disabled-color: #e9ecef' : '--dp-background-color: white'"
            format="dd/MM/yyyy"
            auto-apply
            @update:model-value="saveW29(slops.data_osservazione, slops.id_w29, 'data_osservazione')"
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
            :value="slops.ora_osservazione"
            @change="saveW29($event.target.value, slops.id_w29, 'ora_osservazione')"
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
            :value="getDateFormatted(slops.last_update)"
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
            :value="slops.username"
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
              Mappe
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
                      Livello<br> Criticità ultime 24 ore
                    </th>
                    <th scope="col">
                      Probabilità<br> Criticità ultime 24 ore
                    </th>
                    <th scope="col">
                      Livello<br> Criticità oggi
                    </th>
                    <th scope="col">
                      Probabilità<br> Criticità oggi
                    </th>
                    <th scope="col">
                      Livello<br> Criticità domani
                    </th>
                    <th scope="col">
                      Probabilità<br> Criticità domani
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="area in slops.w29data_set"
                    :key="area.id_w29"
                  >
                    <th scope="row">
                      {{ area.id_w29_zone.descrizione }}
                    </th>
                    <CellPericolo
                      :area="area"
                      :campo="'livello_criticita_oss'"
                      :pericolo="pericolo"
                      :readonly="readonly"
                      :required="true"
                      :validity="validity"
                      @change-pericolo="saveW29DataPericolo"
                    />
                    <CellProbabilita
                      :area="area"
                      :campo="'probabilita_criticita_oss'"
                      :probabilita="probabilita"
                      :readonly="readonly"
                      @change-probabilita="saveW29DataPericolo"
                    />
                    <CellPericolo
                      :area="area"
                      :campo="'livello_criticita_prev_oggi'"
                      :pericolo="pericolo"
                      :readonly="readonly"
                      :required="true"
                      :validity="validity"
                      @change-pericolo="saveW29DataPericolo"
                    />
                    <CellProbabilita
                      :area="area"
                      :campo="'probabilita_criticita_prev_oggi'"
                      :probabilita="probabilita"
                      :readonly="readonly"
                      @change-probabilita="saveW29DataPericolo"
                    />
                    <CellPericolo
                      :area="area"
                      :campo="'livello_criticita_prev_domani'"
                      :pericolo="pericolo"
                      :readonly="readonly"
                      :required="true"
                      :validity="validity"
                      @change-pericolo="saveW29DataPericolo"
                    />
                    <CellProbabilita
                      :area="area"
                      :campo="'probabilita_criticita_prev_domani'"
                      :probabilita="probabilita"
                      :readonly="readonly"
                      @change-probabilita="saveW29DataPericolo"
                    />
                  </tr>
                  <tr>
                    <td colspan="5">
                      <label for="situazione_evoluzione">situazione evoluzione</label><br>
                      <textarea
                        id="situazione_evoluzione"
                        v-model="slops.situazione_evoluzione"
                        name="situazione_evoluzione"
                        rows="3"
                        cols="100"
                        :readonly="readonly"
                        @change="saveW29(slops.situazione_evoluzione, slops.id_w29, 'situazione_evoluzione')"
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
            id="pills-annotazione"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-annotazione-tab"
          >
            <div class="col-md-12 mb-3">
              <label for="note">Note</label><br>
              <textarea
                id="note"
                v-model="slops.note"
                name="note"
                rows="3"
                cols="100"
                :readonly="readonly"
                @change="saveW29(slops.note, slops.id_w29, 'note')"
              />
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
                    CRITICITA' ULTIME 24 ORE
                  </div>
                  <div class="col-sm">
                    CRITICITA' OGGI
                  </div>
                  <div class="col-sm">
                    CRITICITA' DOMANI
                  </div>
                </div>
                <div class="row">
                  <div class="col-sm">
                    <MapSlops
                      :orography="true"
                      :rivers="false"
                      :provinces="false"
                      :capitals="false"
                      :layer="true"
                      :venue-data="livello_criticita_oss"
                      :slopsdata="slops_oss"
                    />
                  </div>
                  <div class="col-sm">
                    <MapSlops
                      :orography="true"
                      :rivers="false"
                      :provinces="false"
                      :capitals="false"
                      :layer="true"
                      :venue-data="livello_criticita_prev_oggi"
                      :slopsdata="slops_prev_oggi"
                    />
                  </div>
                  <div class="col-sm">
                    <MapSlops
                      :orography="true"
                      :rivers="false"
                      :provinces="false"
                      :capitals="false"
                      :layer="true"
                      :venue-data="livello_criticita_prev_domani"
                      :slopsdata="slops_prev_domani"
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
import MapSlops from './MapSlops.vue'
import CellProbabilita from './CellProbabilita.vue'

export default {

  name: 'SlopsBulletin',
  components: {
    CellPericolo,
    CellProbabilita,
    MapSlops,
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
      slops: {},
      pericolo: [],
      slopsdata: {},
      state: store.state,
      readonly: true,
      sending: false,
      reopening: false,
      saving: false
    }
  },
  computed: {
    today() {
      // returns today in 2021-04-22 format
      let d = new Date()
      return d.toISOString().substring(0, 10)
    },
    validity(){
      let result = {all: true}
      if (this.slops.w29data_set){
        this.slops.w29data_set.forEach(area=>{
          if (!(area.id_w29_data in result)){
            result[area.id_w29_data] = {}
          }
          if (area['livello_criticita_oss'] == 'np'){
            result[area.id_w29_data]['livello_criticita_oss'] = false
            result.all = false
          }else{
            result[area.id_w29_data]['livello_criticita_oss'] = true
          }
          if (area['livello_criticita_prev_oggi'] == 'np'){
            result[area.id_w29_data]['livello_criticita_prev_oggi'] = false
            result.all = false
          }else{
            result[area.id_w29_data]['livello_criticita_prev_oggi'] = true
          }
          if (area['livello_criticita_prev_domani'] == 'np'){
            result[area.id_w29_data]['livello_criticita_prev_domani'] = false
            result.all = false
          }else{
            result[area.id_w29_data]['livello_criticita_prev_domani'] = true
          }
        })
      }
      return result
    },
    livello_criticita_oss(){
      let vd = { }
      if (this.slops.w29data_set !== undefined) {
        this.slops.w29data_set.forEach(area => {
          vd[area.id_w29_zone.id_w29_zone] = this.coloreHtml(area.livello_criticita_oss)
        })
      }
      return vd
    },
    livello_criticita_prev_oggi(){
      let vd = { }
      if (this.slops.w29data_set !== undefined) {
        this.slops.w29data_set.forEach(area => {
          vd[area.id_w29_zone.id_w29_zone] = this.coloreHtml(area.livello_criticita_prev_oggi)
        })
      }
      return vd
    },
    livello_criticita_prev_domani(){
      let vd = { }
      if (this.slops.w29data_set !== undefined) {
        this.slops.w29data_set.forEach(area => {
          vd[area.id_w29_zone.id_w29_zone] = this.coloreHtml(area.livello_criticita_prev_domani)
        })
      }
      return vd
    },
    slops_oss(){
      let vd = { }
      if (this.slops.w29data_set !== undefined) {
        this.slops.w29data_set.forEach(area => {
          let data = { }
          data['probabilita'] = area.probabilita_criticita_oss
          data['criticita'] = area.livello_criticita_oss
          data['criticita_color'] = this.coloreHtml(area.livello_criticita_oss)
          vd[area.id_w29_zone.id_w29_zone] = data
        })
      }
      return vd
    },
    slops_prev_oggi(){
      let vd = { }
      if (this.slops.w29data_set !== undefined) {
        this.slops.w29data_set.forEach(area => {
          let data = { }
          data['probabilita'] = area.probabilita_criticita_prev_oggi
          data['criticita'] = area.livello_criticita_prev_oggi
          data['criticita_color'] = this.coloreHtml(area.livello_criticita_prev_oggi)
          vd[area.id_w29_zone.id_w29_zone] = data
        })
      }
      return vd
    },
    slops_prev_domani(){
      let vd = { }
      if (this.slops.w29data_set !== undefined) {
        this.slops.w29data_set.forEach(area => {
          let data = { }
          data['probabilita'] = area.probabilita_criticita_prev_domani
          data['criticita'] = area.livello_criticita_prev_domani
          data['criticita_color'] = this.coloreHtml(area.livello_criticita_prev_domani)
          vd[area.id_w29_zone.id_w29_zone] = data
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
        colore = 'black'
      else if (parametro == '-')
        colore = '#A6A6A6'
      else if (parametro == '1')
        colore = '#99CCFF'
      else if (parametro == '2')
        colore = '#9999FF'
      else if (parametro == '3')
        colore = '#9900FF'
      return colore
    },
    async fetchData () {
      this.slops_id = this.id
      this.pericolo  = await this.fetchPericolo()
      this.probabilita  = await this.fetchProbabilita()
      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
      this.fetchSlops().then(response => {
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
        this.slops = data
        this.readonly = (this.slops.status === '1' || this.slops.status === '2' || !this.state.username)
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
    async fetchSlops () {
      // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
      const response = await fetch('/api/w29/bulletins/' + this.slops_id + '/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
     async fetchPericolo () {
      try {
        const response = await fetch('/api/w29/pericolo/', {
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
    async fetchProbabilita () {
      try {
        const response = await fetch('/api/w29/probabilita/', {
          headers: {
            accept: 'application/json'
          }
        })
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero del Probabilita`,
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
    saveW29(newValue, id_w29, campo) {
      this.saving = true
      //data_validata
      if (campo==="data_validita") {
        let month = String(newValue.getMonth() + 1);
        let day = String(newValue.getDate());
        const year = String(newValue.getFullYear());

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        newValue=`${year}-${month}-${day}`;
        this.slops.data_validita=newValue;
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
        this.slops.data_simulazione=newValue;
      }
      //data_osservazione
      if (campo==="data_osservazione") {
        if(newValue!=null){
          console.log('newValue   ',newValue)
          let month = String(newValue.getMonth() + 1);
          let day = String(newValue.getDate());
          const year = String(newValue.getFullYear());

          if (month.length < 2) month = '0' + month;
          if (day.length < 2) day = '0' + day;

          newValue=`${year}-${month}-${day}`;
        }else{
          newValue='n.d.'
        }
        this.slops.data_osservazione=newValue;
      }
      //ora_simulazione
      if(campo==="ora_simulazione"){
        this.slops.ora_simulazione=newValue;
      }
      //ora_osservazione
      if(campo==="ora_osservazione"){
        this.slops.ora_osservazione=newValue;
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
      payload['id_w29'] = id_w29
      payload['username'] = store.state.username
      this.bulkUpdateW29(payload).then((response) => {
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
        this.slops.last_update = data.last_update
        this.slops.username = store.state.username
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
    saveW29DataPericolo(newValue, id_w29_zone, campo) {
      let myW29zone = this.slops.w29data_set.find(w29data => {
        return w29data.id_w29_zone.id_w29_zone === id_w29_zone
      })
      myW29zone[campo] = newValue
      const payload = { }
      payload[campo] = newValue
      this.fetchPatch(myW29zone.id_w29_data, 'data', payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio',
              type: 'error',
              position: 'top-left'
            }
          )
        } else {
          this.saveW29(null, this.slops.id_w29, null)
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
        api.fetchBulletinDelete(this.slops_id, 'w29/bulletins', store).then(response => {
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
    async fetchSlopsAction (action) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w29/bulletins/${this.slops_id}/${action}/`
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
      this.fetchSlopsAction(action).then(response => {
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
          this.$router.push({ path: `/w29/`})
          //this.$router.push({ path: `/w29/${data.id_w29}`})
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
        `/api/w29/${endpoint}/${id}/`,
        {
          method: 'PATCH',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    async bulkUpdateW29(payload) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w29/bulletins/bulk_update/`,
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
