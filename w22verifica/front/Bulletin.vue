// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
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
          v-if="verificapiene.status === '0' && state.username"
          :disabled="sending || (meta && !meta.valid) || verificapiene.id_numero_bollettino === '0_0'"
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
          v-if="verificapiene.status === '0' && state.username"
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
      <h1>Bollettino Verifica Piene {{ verificapiene.id_w22verifica }}</h1>
      <div
        v-if="verificapiene.id_numero_bollettino == '0_0'"
        class="alert alert-danger"
      >
      <h1>Manca il First guess del Piene numero {{ verificapiene.numero_bollettino.split("/")[0]+'_'+verificapiene.numero_bollettino.split("/")[1] }}</h1>
      </div>
      <div
        v-if="meta && !meta.valid"
        class="alert alert-danger"
      >
        Ci sono dei campi incompleti
      </div>
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato</label>
        <span v-if="verificapiene.status == 1">
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
          :value="getDateFormatted(verificapiene.data_emissione, time = false)"
        >
      </div>
      <div class="col-md-2 mb-3">
        <label for="ora_emissione">Num bollettino Piene</label>
        <input
          id="id_numero_bollettino"
          :readonly="readonly"
          class="form-control"
          name="id_numero_bollettino"
          type="text"
          :value="verificapiene.id_numero_bollettino"
          @change="saveW22verifica($event.target.value, verificapiene.id_w22verifica, 'id_numero_bollettino')"
        >
      </div>

      <div class="col-md-2 mb-3">
        <label for="last_update">Ultima modifica</label>
        <input
          id="last_update"
          disabled
          class="form-control"
          name="last_update"
          type="text"
          :value="getDateFormatted(verificapiene.last_update)"
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
          :value="verificapiene.username"
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
                id="pills-criteri-tab"
                class="nav-link"
                data-bs-toggle="pill"
                data-bs-target="#pills-criteri"
                type="button"
                role="tab"
                aria-controls="pills-criteri"
                aria-selected="false"
              >
                Criteri
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
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <table>
                      <tbody>
                        <tr>
                          <td>
                            <label for="situazione_evoluzione">Situazione ed evoluzione</label><br>
                            <textarea
                              id="situazione_evoluzione"
                              v-model="verificapiene.situazione_evoluzione"
                              class="form-control"
                              name="situazione_evoluzione"
                              rows="2"
                              cols="200"
                              :readonly="readonly"
                              @change="saveW22verifica(verificapiene.situazione_evoluzione, verificapiene.id_w22verifica, 'situazione_evoluzione')"
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
                        class="text-left"
                        colspan="1"
                      >
                        Criticità Osservata
                      </th>
                      <th
                        class="text-left"
                        colspan="1"
                      >
                        Criticità Prevista
                      </th>
                      <th
                        class="text-left"
                        colspan="1"
                      >
                        Severità
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="area in verificapiene.w22verificadata_set"
                      :key="area.id_w22verifica_data"
                    >
                      <th scope="row">
                        {{ area.id_w22_zone.corso_acqua }}
                      </th>
                      <th scope="row">
                        {{ area.id_w22_zone.denominazione_stazione }}
                      </th>
                      <th scope="row">
                      <td>
                        <CellCriticita
                          :area="area"
                          :campo="'oss_crit_tot'"
                          :criticita="criticita"
                          :readonly="readonly"
                          @changeCriticita="saveW22verificaDataSelect"
                        />
                      </td>
                      </th>
                      <th scope="row">
                      <td>
                        <CellCriticita
                          :area="area"
                          :campo="'prev_crit_tot'"
                          :criticita="criticita"
                          :readonly="readonly"
                          @changeCriticita="saveW22verificaDataSelect"
                        />
                      </td>
                      </th>
                      <th scope="row">
                      <CellSeverita
                        :area="area"
                        :campo="'err_crit_tot'"
                        :severita="severita"
                        :readonly="readonly"
                        @changeSeverita="saveW22verificaDataSelect"
                      />
                      </th>
                    </tr>
                  </tbody>
                </table>
                <div class="row">
                  <div class="col-md-12 mb-3">

                    <table>
                      <tbody>
                        <tr>
                          <td>
                            <label for="id_w22giudizio">Giudizio</label><br>
                            </td>
                            </tr>
                            <tr>
                            <CellGiudizio
                              :w22verifica="verificapiene"
                              :area="verificapiene"
                              :campo="'id_w22giudizio'"
                              :giudizio="giudizio"
                              :readonly="readonly"
                              @changeGiudizio="saveW22verifica"
                            />
                        </tr>
                      </tbody>
                    </table>
                    <table class="table table-striped">
                      <tbody>
                        <tr>
                          <th style="text-align:center;">
                            Numero Li
                          </th>
                          <th style="text-align:center;">
                            Numero Gr o MGr
                          </th>
                        </tr>
                        <tr>
                          <td style="text-align:center;">
                            {{ gr.num_li }}
                          </td>
                          <td style="text-align:center;">
                            {{ gr.num_mgr_gr }}
                          </td>
                        </tr>
                      </tbody>
                    </table>
</div>
</div>
                    <div class="row">
                      <div class="col-md-12 mb-3">
                    <label>Legenda Giudizio</label>
                    <table border=1>
                    <tbody>
                      <tr>
                        <th>
                          Giudizio
                        </th>
                        <th>
                          Valore
                        </th>
                      </tr>
                    <tr>
                      <td bgcolor="#6EBB00">
                        Ottimo
                      </td>
                      <td bgcolor="#6EBB00">
                        1
                      </td>
                    </tr>
                    <tr>
                      <td bgcolor="#6EBB00">
                        Buono
                      </td>
                      <td bgcolor="#6EBB00">
                        2
                      </td>
                      </tr>
                      <tr>
                      <td bgcolor="#ffff00">
                        Sufficiente
                      </td>
                      <td bgcolor="#ffff00">
                        3
                      </td>
                      </tr>
                      <tr>
                      <td bgcolor="#FF0000">
                        Insufficiente
                      </td>
                      <td bgcolor="#FF0000">
                        4
                      </td>
                      </tr>
                      <tr>
                      <td bgcolor="#8f00ff">
                        Pessimo
                      </td>
                      <td bgcolor="#8f00ff">
                        5
                      </td>
                    </tr>
                    </tbody>
                    </table>
                    <label>Legenda Severità</label>
                    <table border=1>
                    <tbody>
                      <tr>
                      <th>
                        Severità
                      </th>
                        <th>
                          Sigla
                        </th>
                        <th>
                          Valore
                        </th>
                      </tr>
                    <tr>
                      <td bgcolor="#6EBB00">
                        1
                      </td>
                      <td bgcolor="#6EBB00">
                        Ok
                      </td>
                      <td bgcolor="#6EBB00">
                      	Assenza di errore
                      </td>
                    </tr>
                    <tr>
                      <td bgcolor="#ffff00">
                        2
                      </td>
                      <td bgcolor="#ffff00">
                        Li
                      </td>
                      <td bgcolor="#ffff00">
                        Errore lieve
                      </td>
                      </tr>
                      <tr>
                      <td bgcolor="#FF0000">
                        3
                      </td>
                      <td bgcolor="#FF0000">
                        Gr
                      </td>
                      <td bgcolor="#FF0000">
                        Errore grave
                      </td>
                      </tr>
                      <tr>
                      <td bgcolor="#8f00ff">
                        4
                      </td>
                      <td bgcolor="#8f00ff">
                        MGr
                      </td>
                      <td bgcolor="#8f00ff">
                        Errore molto grave
                      </td>
                      </tr>

                    </tbody>
                    </table>
                  </div>
                </div>
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
                              v-model="verificapiene.annotazione"
                              class="form-control"
                              name="annotazione"
                              rows="2"
                              cols="200"
                              :readonly="readonly"
                              @change="saveW22verifica(verificapiene.annotazione, verificapiene.id_w22verifica, 'annotazione')"
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
              id="pills-criteri"
              class="tab-pane fade"
              role="tabpanel"
              aria-labelledby="pills-criteri-tab"
            >
              <div class="col-md-12 mb-3">
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <table>
                      <tr>
                        <th style="text-align:center;" colspan=5>Severità</th>
                      </tr>
                      <tr>
                        <th colspan=5>Valutazione gravità Errore</th>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE;"></td>
                        <td style="background-color: #D6EEEE;">Aoss</td>
                        <td style="background-color: #D6EEEE;">Ooss</td>
                        <td style="background-color: #D6EEEE;">Moss</td>
                        <td style="background-color: #D6EEEE;">Eoss</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE;">Aprev</td>
                        <td bgcolor="#6EBB00">Ok</td>
                        <td bgcolor="#ffff00">Li</td>
                        <td bgcolor="#8f00ff">MGr</td>
                        <td bgcolor="#8f00ff">MGr</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE;">Oprev</td>
                        <td bgcolor="#ffff00">Li</td>
                        <td bgcolor="#6EBB00">Ok</td>
                        <td bgcolor="#FF0000">Gr</td>
                        <td bgcolor="#8f00ff">MGr</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE;">Mprev</td>
                        <td bgcolor="#FF0000">Gr</td>
                        <td bgcolor="#ffff00">Li</td>
                        <td bgcolor="#6EBB00">Ok</td>
                        <td bgcolor="#FF0000">Gr</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE;">Eprev</td>
                        <td bgcolor="#8f00ff">MGr</td>
                        <td bgcolor="#8f00ff">MGr</td>
                        <td bgcolor="#FF0000">Gr</td>
                        <td bgcolor="#6EBB00">Ok</td>
                      </tr>
                    </table> 
                    <table>
                      <tr>
                        <th style="text-align:center;" colspan=7>Giudizio</th>
                      </tr>
                      <tr>
                        <th></th>
                        <th></th>
                        <th colspan=5>Numero di errori gravi (Gr-MGr)</th>
                      </tr>
                      <tr>
                        <td></td>
                        <td></td>
                        <td style="background-color: #D6EEEE; text-align:center;">0</td>
                        <td style="background-color: #D6EEEE; text-align:center;">1-2</td>
                        <td style="background-color: #D6EEEE; text-align:center;">3-4</td>
                        <td style="background-color: #D6EEEE; text-align:center;">5-10</td>
                        <td style="background-color: #D6EEEE; text-align:center;">11-27</td>
                      </tr>
                      <tr>
                        <td rowspan=4 style="writing-mode: vertical-lr;width: 23px;"><b>Numero di errori lievi (Li)</b></td>
                        <td style="background-color: #D6EEEE; text-align:center;">0</td>
                        <td style="background-color: #6EBB00; text-align:center;">Buono</td>
                        <td style="background-color: #6EBB00; text-align:center;">Buono</td>
                        <td style="background-color: #ffff00; text-align:center;">Sufficiente</td>
                        <td style="background-color: #FF0000; text-align:center;">Insufficiente</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE; text-align:center;">1-5</td>
                        <td style="background-color: #6EBB00; text-align:center;">Buono</td>
                        <td style="background-color: #6EBB00; text-align:center;">Buono</td>
                        <td style="background-color: #FF0000; text-align:center;">Insufficiente</td>
                        <td style="background-color: #FF0000; text-align:center;">Insufficiente</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE; text-align:center;">1-5</td>
                        <td style="background-color: #ffff00; text-align:center;">Sufficiente</td>
                        <td style="background-color: #ffff00; text-align:center;">Sufficiente</td>
                        <td style="background-color: #FF0000; text-align:center;">Insufficiente</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE; text-align:center;">11-27</td>
                        <td style="background-color: #FF0000; text-align:center;">Insufficiente</td>
                        <td style="background-color: #FF0000; text-align:center;">Insufficiente</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                      </tr>
                    </table> 
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
import CellGiudizio from './CellGiudizio.vue'
import CellSeverita from './CellSeverita.vue'
import CellCriticita from './CellCriticita.vue'

export default {
  name: 'VerificaPieneBulletin',
  components: {
  CellGiudizio,
  CellSeverita,
  CellCriticita,
  },
  data () {
  // non reactive properties
    return {
      // reactive properties
      verificapiene: {
        id_w22verifica: "aaaaaaaa"
      },
      giudizio: [],
      severita: [],
      criticita: [],
      state: store.state,
      readonly: true,
      sending: false
   }
 },
 mounted() {
   console.log(`the component is now mounted.`)
 },
 computed: {
   //calcolo della severita
   Verificaseverita() {
      let vd = { }
      if (this.verificapiene.w22verificadata_set !== undefined) {
        this.verificapiene.w22verificadata_set.forEach(area => {
          let data = { }
          if(area.oss_crit_tot==area.prev_crit_tot){ 
            data['severita'] = '1'
          }else if((area.oss_crit_tot==='A' && area.prev_crit_tot==='O') || (area.oss_crit_tot==='O' && area.prev_crit_tot==='A') || (area.oss_crit_tot==='O' && area.prev_crit_tot==='M')){ 
            data['severita'] = '2'
          }else if((area.oss_crit_tot==='A' && area.prev_crit_tot==='M') || (area.oss_crit_tot==='M' && area.prev_crit_tot==='O') || (area.oss_crit_tot==='M' && area.prev_crit_tot==='E') || (area.oss_crit_tot==='E' && area.prev_crit_tot==='M')){ 
            data['severita'] = '3'
          }else{ 
            data['severita'] = '4'
          }
          data['area'] = area.id_w22_zone.id_w22_zone
          vd[area.id_w22_zone.id_w22_zone] = data
        })
      }
      return vd
   },
   //calcolo del giudizio
   gr() {
     let vd = { }
     let giudizio = 0
     let li = 0
     let mgr_gr = 0
      if (this.verificapiene.w22verificadata_set !== undefined) {
        this.verificapiene.w22verificadata_set.forEach(area => {
          vd['num_li']=li
          vd['num_mgr_gr']=mgr_gr
          if(area.err_crit_tot==2) {
            li=li+1
            vd['num_li']=li
          }else if(area.err_crit_tot==3) {
            mgr_gr=mgr_gr+1
            vd['num_mgr_gr']=mgr_gr
          }else if(area.err_crit_tot==4) {
            mgr_gr=mgr_gr+1
            vd['num_mgr_gr']=mgr_gr
          }
        })
        //costruzione giudizio
        if(mgr_gr<=2 && li<=5){
          //Buono
          giudizio = 2
        }else if(mgr_gr<=0 && li<=0){
          //Buono
          giudizio = 1
        }else if(mgr_gr>=11){
          //pessimo
          giudizio = 5
        }else if(mgr_gr>=3 && mgr_gr<=4 && li==0){
          //sufficiente
          giudizio = 3
        }else if(mgr_gr>=3 && mgr_gr<=4 && li>=1 && li<=5){
          //Insufficiente
          giudizio = 4
        }else if(mgr_gr>=5 && mgr_gr<=10 && li<=5){
          //Insufficiente
          giudizio = 4
        }else if(mgr_gr<=2 && li>=6 && li<=10){
          //sufficiente
          giudizio = 3
        }else if(mgr_gr<=2 && li>=11 && li<=27){
          //sufficiente
          giudizio = 3
        }else if(mgr_gr>=3 && mgr_gr<=4 && li>=6 && li<=10){
          //Insufficiente
          giudizio = 4
        }else{
          //pessimo
          giudizio = 5
        }
        //fine costruzione giudizio
        vd['giudizio']=giudizio
      }
      return vd
   },
 },
 created() {
  // https://vuejs.org/v2/guide/instance.html
    this.fetchData()
  },
  methods: {
    async fetchData () {
      this.verificapiene_id = this.$route.params.id
      this.giudizio  =  await this.fetchGiudizio()
      this.severita  =  await this.fetchSeverita()
      this.criticita  =  await this.fetchCriticita()

      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
      this.fetchVerificaPiene().then(response => {
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
        this.verificapiene = data
        this.readonly = (this.verificapiene.status === '1' || !this.state.username)
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
    async fetchVerificaPiene () {
      // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
      const response = await fetch('/api/w22verifica/bulletins/' + this.verificapiene_id + '/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    async fetchGiudizio () {
      try {
        const response = await fetch('/api/w22verifica/giudizio/', {
          headers: {
            accept: 'application/json'
          }
        })
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero del Giudizio`,
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
    async fetchSeverita () {
      try {
        const response = await fetch('/api/w22verifica/severita/', {
          headers: {
            accept: 'application/json'
          }
        })
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero del Severita`,
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
        `/api/w22verifica/${endpoint}/${id}/`,
        {
          method: 'PATCH',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    saveW22verifica(newValue, id_w22verifica, campo) {
      //se sto calcolando il giudizio in automatico
      if(campo==null){
        campo='id_w22giudizio'
        newValue=this.gr.giudizio
      }
      if(campo==="id_numero_bollettino"){
        this.verificapiene.id_numero_bollettino=newValue;
        this.verificapiene.numero_bollettino=newValue.split("_")[0]+'/'+newValue.split("_")[1];
      }
      const payload = { }
      if (campo) {
        payload[campo] = newValue
      }
      if(campo==="id_numero_bollettino"){
        payload['numero_bollettino'] = newValue.split("_")[0]+'/'+newValue.split("_")[1];
      }
      payload['id_w22verifica'] = id_w22verifica
      payload['username'] = store.state.username
      this.bulkUpdateW22verifica(payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio bulk',
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
        this.verificapiene.last_update = data.last_update
        this.verificapiene.username = store.state.username
        if(campo==="id_w22giudizio"){
          this.verificapiene.id_w22giudizio=newValue;
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
    getDateFormatted(rawString, time = true) {
      return api.getDateFormatted(rawString, time)
    },
    // Metodo generico per salvare i dati delle select di criticita e tendenza
    saveW22verificaDataSelect(newValue,id_w22verifica_data, id_w22_zone, campo) {
      let myW22zone = this.verificapiene.w22verificadata_set.find(w22verificadata => {
        return w22verificadata.id_w22_zone.id_w22_zone === id_w22_zone
      })
      myW22zone[campo] = newValue
      const payload = { }
      if(campo=='prev_crit_tot' || campo=='oss_crit_tot'){ 
        //sto assegando e salvando il calcolo della criticità in automatico
        this.verificapiene.w22verificadata_set[id_w22_zone-1].err_crit_tot=this.Verificaseverita[id_w22_zone].severita
        payload['err_crit_tot']=this.Verificaseverita[id_w22_zone].Severita
        //sto salvando il calcolo del giudizio automatico
        this.saveW22verifica(this.gr.giudizio, this.verificapiene.id_w22verifica, 'id_w22giudizio')
      }
      payload[campo] = newValue

      this.fetchPatch(myW22zone.id_w22verifica_data, 'data', payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio',
              type: 'error',
              position: 'top-left'
            }
          )
        } else {
          this.saveW22verifica(null, this.verificapiene.id_w22verifica, null)
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
        api.fetchBulletinDelete(this.verificapiene_id, 'w22verifica/bulletins', store).then(response => {
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
    async fetchVerificaPieneAction (action) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w22verifica/bulletins/${this.verificapiene_id}/${action}/`
      )
      return response
    },
    execute(action, reroute, message) {
      this[action + 'ing'] = true
      this.fetchVerificaPieneAction(action).then(response => {
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
          this.$router.push({ path: `/w22verifica/${data.id_w22verifica}`})
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
    async bulkUpdateW22verifica(payload) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w22verifica/bulletins/bulk_update/`,
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
