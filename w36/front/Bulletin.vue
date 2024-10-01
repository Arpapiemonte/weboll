// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="container-fluid">
    <div
      class="row justify-content-end sticky-top py-1"
      style="background-color: #f8f9fa; z-index: 200;"
    >
      <div
        v-if="loading"
        class="spinner-border"
        role="status"
      >
        <span class="visually-hidden">Loading...</span>
      </div>
      <!-- https://getbootstrap.com/docs/5.1/components/button-group/ -->
      <div
        class="btn-group w-auto h-100"
        role="group"
        aria-label="Basic outlined example"
      >
        <button
          v-if="caldo.status === '0' && caldo.data_emissione === today && state.username && state.username !== owner"
          :disabled="actions.sending || actions.userchanging"
          type="button"
          class="btn btn-danger"
          @click="setOwner()"
        >
          <span v-if="actions.userchanging">
            <span
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
            />
            Sto diventando proprietario ...
          </span>
          <span v-else>
            <img
              src="~bootstrap-icons/icons/save2.svg"
              alt="calc icon"
              width="18"
              height="18"
            > Diventa proprietario
          </span>
        </button>
        <button
          v-if="caldo.status === '0' && caldo.data_emissione === today && state.username"
          :disabled="actions.sending || actions.tempreloading || readonly"
          type="button"
          class="btn btn-outline-dark"
          @click="execute('bollmeteo_terma', false, 'Ricarica temperature del bollettino meteo completata')"
        >
          <span v-if="actions.tempreloading">
            <span
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
            />
            Sto ricaricando le temperature del bollettino meteo ...
          </span>
          <span v-else>
            <img
              src="~bootstrap-icons/icons/repeat.svg"
              alt="calc icon"
              width="18"
              height="18"
            > Ricarica temperature bollettino meteo
          </span>
        </button>
        <a
          class="btn btn-outline-primary"
          :href="'/api/w36/pdf_regione/' + caldo.id_w36"
          target="_blank"
          role="button"
        >
          <img
            src="~bootstrap-icons/icons/file-earmark-pdf-fill.svg"
            alt="PDF icon"
            width="18"
            height="18"
          > PDF Regione
        </a>
        <a
          class="btn btn-outline-primary"
          :href="'/api/w36/pdf_torino/' + caldo.id_w36"
          target="_blank"
          role="button"
        >
          <img
            src="~bootstrap-icons/icons/file-earmark-pdf-fill.svg"
            alt="PDF icon"
            width="18"
            height="18"
          > PDF Torino
        </a>
        <button
          v-if="caldo.status === '0' && state.username"
          :disabled="actions.sending || !validity['global'] || readonly"
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
          v-if="caldo.status === '0' && state.username"
          :disabled="actions.sending || readonly"
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
        <button
          v-if="caldo.status === '1' && state.username && caldo.data_emissione.substring(0, 10) === today"
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
      </div>
    </div>

    <div class="row mb-3">
      <h1>Ondate di calore {{ caldo.id_w36 }}</h1>
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="caldo.status === '1'">
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
            :value="getDateFormatted(caldo.data_emissione, false)"
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
            :value="getDateFormatted(caldo.last_update)"
          >
        </label>
      </div>
      <div class="col-md-1 mb-3">
        <label for="username">Autore
          <input
            id="username"
            disabled
            class="form-control"
            name="username"
            type="text"
            :value="caldo.username"
          >
        </label>
      </div>
      <div
        class="row sticky-top bg-light pt-5"
      >
        <div class="col-md-12">
          <ul
            class="nav nav-tabs nav-justified sticky-top bg-light"
            role="tablist"
            style="top:40px;"
          >
            <!-- tab Capoluoghi-->
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                class="nav-link"
                :class="{active: selectedTab == 'Capoluoghi' ,'text-danger' : !validity['capoluoghi']['tab']}"
                type="button"
                role="tab"
                @click="setTab('Capoluoghi')"
              >
                Capoluoghi
              </button>
            </li>
            <!-- tab Torino-->
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                class="nav-link"
                :class="{active: selectedTab == 'Torino' ,'text-danger' : !validity['torino']['tab']}"
                type="button"
                role="tab"
                @click="setTab('Torino')"
              >
                Torino
              </button>
            </li>
            <!-- tab Parametri-->
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                class="nav-link"
                :class="{active: selectedTab == 'Parametri' ,'text-danger' : !validity['parametri']['tab']}"
                type="button"
                role="tab"
                @click="setTab('Parametri')"
              >
                Parametri
              </button>
            </li>
            <!-- tab Epidemiologia-->
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                class="nav-link"
                :class="{active: selectedTab == 'Epidemiologia' ,'text-danger' : !validity['epidemiologia']['tab']}"
                type="button"
                role="tab"
                @click="setTab('Epidemiologia')"
              >
                Epidemiologia
              </button>
            </li>
            <!-- tab Osservati-->
            <li
              class="nav-item"
              role="presentation"
            >
              <button
                class="nav-link"
                type="button"
                role="tab"
                @click="setTab('Osservati')"
              >
                Osservati
              </button>
            </li>
          </ul>
          <!--  contenuto tab Capoluoghi-->
          <div
            v-show="selectedTab == 'Capoluoghi'"
            role="tabpanel"
          >
            <!-- ancore di navigazione sui capoluoghi -->
            <nav
              class="navbar justify-content-center sticky-top bg-light border-bottom"
              style="top: 80px;margin-top:-9px;height:40px;"
            >
              <ul class="nav">
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('idTO')"
                  >
                    TO
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('idBI')"
                  >
                    BI
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('idAL')"
                  >
                    AL
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('idAT')"
                  >
                    AT
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('idCN')"
                  >
                    CN
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('idNO')"
                  >
                    NO
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('idVB')"
                  >
                    VB
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('idVC')"
                  >
                    VC
                  </a>
                </li>
              </ul>
            </nav>
            <br>
            <div class="row">
              <label for="internal_note">NOTA INTERNA</label>
              <textarea
                id="internal_note"
                rows="1"
                :readonly="readonly"
                :value="caldo.internal_note"
                name="internal_note"
                :style="validity.capoluoghi.internal_note ? '':'border:2px solid red;'"
                class="form-control small-width"
                @change="saveField('internal_note')"
              />
            </div>
            <br>
            <div class="row">
              <label for="note">NOTA EMISSIONE</label>
              <textarea
                id="note"
                rows="1"
                :readonly="readonly"
                :value="caldo.note"
                name="note"
                class="form-control small-width"
                @change="saveField('note')"
              />
            </div> <!-- row -->
            
            
            <div v-if="ready">
              <div class="row">
                <div
                  id="idtop"
                  class="col-10"
                  style="scroll-margin-top: 120px;"
                >
                  <!--  Costruisco 1 tabella per ogni venue -->
                  <div
                    v-for="(v, id_venue) in myVenues"
                    :key="id_venue"
                  >       
                    <div class="row">
                      <!--  Tabella dati previsionali -->
                      <div class="col">
                        <table class="table table-bordered">
                          <caption style="caption-side:top">
                            Dati previsionali
                          </caption>
                          <tbody>
                            <tr 
                              :id="`id${myVenues[id_venue]}`"
                              style="scroll-margin-top: 120px;"
                            >
                              <th
                                rowspan="8"
                                class="text-center"
                              >
                                {{ myVenues[id_venue] }}  
                              </th>
                              <th />
                              <th
                                v-for="(v, tl) in myDate"
                                :key="tl"
                              >
                                {{ myDate[tl] }}
                              </th>
                            </tr>
                            <tr
                              v-for="(d, j) in configCaldo.variabili"
                              :key="j"
                              :value="d.label"
                            >
                              <td>
                                {{ d.label }}
                              </td>
                              <td
                                v-for="(v, tl) in myDate"
                                :key="tl"
                              >
                                <input
                                  type="Number"
                                  :value="caldo.w36_data[tl][id_venue][d.parametro][d.aggregazione].numeric_value"
                                  class="form-control"
                                  :style="validity.capoluoghi.values[tl][id_venue][d.parametro][d.aggregazione] ? '':'border:2px solid red;'"
                                  :disabled="readonly"
                                  @focus="evidenziaPercentili(tl,id_venue,d.parametro)"
                                  @focusout="rilasciaPercentili(tl,id_venue,d.parametro)"
                                  @change="setMeasure(caldo.w36_data[tl][id_venue][d.parametro][d.aggregazione].id_w36_data,d.parametro,tl,d.aggregazione,caldo.w36_data[tl][id_venue][d.parametro][d.aggregazione].id_venue);
                                           calcolaSalvaAT(tl,id_venue,d.parametro,d.aggregazione);
                                           updateAllVenue(id_venue, tl)"
                                >
                              </td>
                            </tr>
                            <tr>
                              <td>
                                GG consecutivi
                              </td>
                              <td
                                v-for="(v, tl) in myDate"
                                :key="tl"
                              >
                                <input
                                  :value="caldo.w36_data[tl][id_venue]['GGCONS'][0].numeric_value"
                                  :disabled="!gg_cons_modificabili"
                                  :style="{
                                    'border': (
                                      validity.capoluoghi.values[tl][id_venue]['GGCONS'][0] ? '':'2px solid red'
                                    ),
                                    'box-shadow': (caldo.w36_data[tl][id_venue]['GGCONS'][0].locked ? '0px 0px 15px black': '')
                                  }"
                                  class="form-select col"
                                  @change="setMeasure(caldo.w36_data[tl][id_venue]['GGCONS'][0].id_w36_data,'GGCONS',tl,0,caldo.w36_data[tl][id_venue]['GGCONS'][0].id_venue)"
                                >
                              </td>
                            </tr>
                            <tr>
                              <td>
                                LIVELLO ORIGINALE
                              </td>
                              <td 
                                v-for="(v, tl) in myDate"
                                :key="tl"
                              >
                                <select
                                  :disabled="true"
                                  :value="caldo.w36_data[tl][id_venue]['COD_COLORE_ORIG'][0].numeric_value"
                                  :style="caldo.w36_data[tl][id_venue]['COD_COLORE_ORIG'][0].numeric_value == 0 ? 'border: #008000; border:3px solid #008000;' :
                                    ( 
                                      caldo.w36_data[tl][id_venue]['COD_COLORE_ORIG'][0].numeric_value == 1 ? 'border: #ffd700; border:3px solid #ffd700;' : 
                                      ( 
                                        caldo.w36_data[tl][id_venue]['COD_COLORE_ORIG'][0].numeric_value == 2 ? 'border: #ffa500; border:3px solid #ffa500;' : 
                                        ( 
                                          caldo.w36_data[tl][id_venue]['COD_COLORE_ORIG'][0].numeric_value == 3 ? 'border: #ff0000; border:3px solid #ff0000;' : ''
                                        )))"
                                  class="form-select col"
                                  @change="setMeasure(caldo.w36_data[tl][id_venue]['COD_COLORE_ORIG'][0].id_w36_data,'COD_COLORE_ORIG',tl,0,caldo.w36_data[tl][id_venue]['COD_COLORE_ORIG'][0].id_venue, false)"
                                >
                                  <option
                                    v-for="(value, key) in codiceColore"
                                    :key="key"
                                    :value="key"
                                  >
                                    {{ value }}
                                  </option>
                                </select>
                              </td>
                            </tr>
                            <tr>
                              <td>
                                LIVELLO EMESSO
                              </td>
                              <td 
                                v-for="(v, tl) in myDate"
                                :key="tl"
                              >
                                <select
                                  :disabled="readonly"
                                  :value="caldo.w36_data[tl][id_venue]['COD_COLORE'][0].numeric_value"
                                  :style="{
                                    'border': (
                                      caldo.w36_data[tl][id_venue]['COD_COLORE'][0].numeric_value == 0 ? '3px solid #008000' :
                                      ( 
                                        caldo.w36_data[tl][id_venue]['COD_COLORE'][0].numeric_value == 1 ? '3px solid #ffd700' : 
                                        ( 
                                          caldo.w36_data[tl][id_venue]['COD_COLORE'][0].numeric_value == 2 ? '3px solid #ffa500' : 
                                          ( 
                                            caldo.w36_data[tl][id_venue]['COD_COLORE'][0].numeric_value == 3 ? '3px solid #ff0000' : ''
                                          )
                                        )
                                      )
                                    ),
                                    'box-shadow': (caldo.w36_data[tl][id_venue]['COD_COLORE'][0].locked ? '0px 0px 15px black': '')
                                  }"
                                  class="form-select col"
                                  @change="setMeasure(caldo.w36_data[tl][id_venue]['COD_COLORE'][0].id_w36_data,'COD_COLORE',tl,0,caldo.w36_data[tl][id_venue]['COD_COLORE'][0].id_venue, true)"
                                >
                                  <option
                                    v-for="(value, key) in codiceColore"
                                    :key="key"
                                    :value="key"
                                  >
                                    {{ value }}
                                  </option>
                                </select>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <!--  Tabella percentili -->
                      <div class="col">
                        <table class="table table-bordered">
                          <caption style="caption-side:top">
                            Percentili di riferimento
                          </caption>
                          <tbody>
                            <tr>
                              <th />
                              <th
                                v-for="(v, tl) in myDate"
                                :key="tl"
                              >
                                {{ myDate[tl] }}
                              </th>
                            </tr>
                            <!--  Nella tabella dati previsionali creo 1 riga per ogni variabile contenuta nell'array variabili
                              specificato in configCaldo. Il livello è diverso perchè è una select e non un input  -->
                            <tr
                              v-for="(d, j) in configCaldo.percentili"
                              :key="j"
                              :value="d.label"
                            >
                              <td>
                                {{ d.label }}
                              </td>
                              <td
                                v-for="(v, tl) in myDate"
                                :key="tl"
                              >
                                <input
                                  :id="`${tl}_${id_venue}_${d.parametro}_${d.aggregazione}`"
                                  type="Number"
                                  :value="caldo.w36_data[tl][id_venue][d.parametro][d.aggregazione].numeric_value"
                                  :disabled="true"
                                >
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <!--  Tabella wda -->
                      <div class="col">
                        <table class="table table-bordered">
                          <caption style="caption-side:top">
                            WDA previsto
                          </caption>
                          <tbody>
                            <tr>
                              <th
                                v-for="(v, tl) in myDate"
                                :key="tl"
                              >
                                {{ myDate[tl] }}
                              </th>
                            </tr>
                            <tr
                              v-for="(d, j) in configCaldo.wda"
                              :key="j"
                              :value="d.label"
                            > 
                              <td
                                v-for="(v, tl) in myDate"
                                :key="tl"
                              >
                                <input
                                  type="Number"
                                  :value="wda[id_venue][tl][d.aggregazione].numeric_value"
                                  class="form-control"
                                  :disabled="true"
                                >
                              </td>
                              <td>
                                {{ d.label }}
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-2">
                  <div 
                    class="sticky-top"
                    style="top:130px;"
                  >
                    <div
                      :id="`mappa-${id}`"
                      style="scroll-margin-top: 40px;"
                    >
                      <MapCaldo 
                        :tl="48"
                        :caldo="caldo"
                      />
                    </div>
                    <br>
                    <div
                      :id="`mappa-${id}`"
                      style="scroll-margin-top: 40px;"
                    >
                      <MapCaldo 
                        :tl="66"
                        :caldo="caldo"
                      />
                    </div>
                    <br>
                    <div
                      :id="`mappa-${id}`"
                      style="scroll-margin-top: 40px;"
                    >
                      <MapCaldo 
                        :tl="83"
                        :caldo="caldo"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div> 
            <div
              v-if="isTop"
              class="d-flex justify-content-end"
              style="height:100px;position: fixed;bottom: 10px;right: 0px;"
            >
              <button
                type="button"
                class="btn btn-outline-dark h-50"
                @click="goto('idtop')"
              >
                TOP
              </button>
            </div> 
          </div>
            

          <!--  contenuto tab Torino-->
          <div
            v-show="selectedTab == 'Torino'"
            role="tabpanel"
          >
            <div v-if="ready">
              <br>
              <div class="row">
                <div class="col">
                  <table class="table table-bordered">
                    <tbody>
                      <tr>
                        <td>Data</td> 
                        <td>Tmax (°C)</td>
                        <td>ATmax (°C)</td>
                        <td>Tmin (°C)</td>
                        <td>ATmin (°C)</td>
                      </tr>
                      <tr
                        v-for="(tl, index) in myDateTorino"
                        :key="index"
                        :value="tl"
                      >
                        <th>{{ tl[1] }}</th>
                        <td
                          v-for="(d, j) in configCaldo.temperature_torino"
                          :key="j"
                        >
                          <input
                            type="Number"
                            :value="caldo.w36_data[tl[0]][59][d.parametro][d.aggregazione].numeric_value"
                            class="form-control"
                            :style="validity.torino.values[tl[0]][59][d.parametro][d.aggregazione] ? 'background-color: #b3d9ff;':'border:2px solid red;background-color: #b3d9ff;'"
                            :disabled="readonly"
                            @change="setMeasure(caldo.w36_data[tl[0]][59][d.parametro][d.aggregazione].id_w36_data,d.parametro,tl[0],d.aggregazione,59, false)"
                          >
                        </td>
                      </tr>
                      <tr
                        v-for="(k, tl) in myDate"
                        :key="tl"
                      >
                        <th>{{ myDate[tl] }}</th>
                        <td
                          v-for="(d, j) in configCaldo.temperature_torino"
                          :key="j"
                        >
                          <input
                            type="Number"
                            :value="caldo.w36_data[tl][59][d.parametro][d.aggregazione].numeric_value"
                            class="form-control"
                            :style="validity.torino.values[tl][59][d.parametro][d.aggregazione] ? '':'border:2px solid red;'"
                            :disabled="readonly"
                            @change="setMeasure(caldo.w36_data[tl][59][d.parametro][d.aggregazione].id_w36_data,d.parametro,tl,d.aggregazione,59, false);
                                     calcolaSalvaAT(tl,59,d.parametro,d.aggregazione);
                                     updateAllVenue(59, tl)"
                          >
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="col">
                  <img :src="'data:image/png;base64, ' + image_max">
                </div>
                <div class="col">
                  <img :src="'data:image/png;base64, ' + image_min">
                </div>
              </div>
            </div>
          </div>
          <!--  contenuto tab Parametri-->
          <div
            v-show="selectedTab == 'Parametri'"
            role="tabpanel"
          >
            <!-- ancore di navigazione sui capoluoghi -->
            <nav
              class="navbar justify-content-center sticky-top bg-light border-bottom"
              style="top: 80px;margin-top:-9px;height:40px;"
            >
              <ul class="nav">
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('id_TO')"
                  >
                    TO
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('id_BI')"
                  >
                    BI
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('id_AL')"
                  >
                    AL
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('id_AT')"
                  >
                    AT
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('id_CN')"
                  >
                    CN
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('id_NO')"
                  >
                    NO
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('id_VB')"
                  >
                    VB
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('id_VC')"
                  >
                    VC
                  </a>
                </li>
              </ul>
            </nav>
            <br>
            <div v-if="ready">
              <div class="row">
                <div class="col-3">
                  <th> Osservati IERI </th>
                </div>
                <div
                  v-for="(v, tl) in myDate"
                  :key="tl"
                  class="col-3"
                > 
                  <div>
                    <th> {{ myDate[tl] }}</th>
                  </div>
                </div>
              </div> <!-- chiusura row -->
              <div
                v-for="(v, id_venue) in myVenues"
                :key="id_venue"
              > 
                <div class="row">
                  <!--  Tabella AT cod_colore e cons osservati di ieri -->
                  <div class="col-3">
                    <table class="table table-bordered table-info">
                      <tbody>
                        <tr 
                          :id="`id_${myVenues[id_venue]}`"
                          style="scroll-margin-top: 120px;"
                        >
                          <th> {{ myVenues[id_venue] }}</th>
                          <td>AT (°C)</td>
                          <td>cod.colore</td>
                          <td>CONS</td> 
                        </tr>
                        <tr>
                          <td>MIN</td>
                          <td>
                            <input
                              type="Number"
                              style="background-color:  #EAECEE"
                              :value="caldo.w36_data[32][id_venue]['ATMIN'][0].numeric_value"
                              :style="validity.parametri.values[32][id_venue]['ATMIN'][0] ? '':'border:2px solid red;'"
                              class="form-control"
                              :disabled="readonly"
                              @change="setMeasure(caldo.w36_data[32][id_venue]['ATMIN'][0].id_w36_data,'ATMIN',32,0,caldo.w36_data[32][id_venue]['ATMIN'][0].id_venue, false);
                                       updateAllVenue(id_venue, 32)"
                            >
                          </td>
                          <td
                            rowspan="2"
                            style="vertical-align : middle"
                          >
                            {{ codiceColore[caldo.w36_data[32][id_venue]['COD_COLORE'][0].numeric_value] }}
                          </td>
                          <td
                            rowspan="2"
                            style="vertical-align : middle"
                          >
                            <input
                              type="Number"
                              style="background-color:  #EAECEE"
                              :value="caldo.w36_data[32][id_venue]['GGCONS'][0].numeric_value"
                              :style="validity.parametri.values[32][id_venue]['GGCONS'][0] ? '':'border:2px solid red;'"
                              class="form-control"
                              :disabled="readonly"
                              @change="setMeasure(caldo.w36_data[32][id_venue]['GGCONS'][0].id_w36_data,'GGCONS',32,0,caldo.w36_data[32][id_venue]['GGCONS'][0].id_venue, false);
                                       updateAllVenue(id_venue, 32)"
                            >
                          </td>
                        </tr> 
                        <tr>
                          <td>MAX</td>
                          <td>
                            <input
                              type="Number"
                              style="background-color:  #EAECEE"
                              :value="caldo.w36_data[32][id_venue]['ATMAX'][0].numeric_value"
                              :style="validity.parametri.values[32][id_venue]['ATMAX'][0] ? '':'border:2px solid red;'"
                              class="form-control"
                              :disabled="readonly"
                              @change="setMeasure(caldo.w36_data[32][id_venue]['ATMAX'][0].id_w36_data,'ATMAX',32,0,caldo.w36_data[32][id_venue]['ATMAX'][0].id_venue, false);
                                       updateAllVenue(id_venue, 32)"
                            >
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>     
                  <!--  Tabella T-RH-V e AT -->
                  <div
                    v-for="(v, tl) in myDate"
                    :key="tl"
                    class="col-3"
                  >
                    <table class="table table-bordered">
                      <tbody>
                        <tr>
                          <th> {{ myVenues[id_venue] }}</th>
                          <td>T (°C)</td>
                          <td>RH (%)</td>
                          <td>Wind (m/s)</td> 
                          <td>AT (°C)</td>
                        </tr>
                        <tr>
                          <td>MIN</td>
                          <td
                            v-for="param in myParam"
                            :key="param"
                          >
                            <input
                              type="Number"
                              :value="caldo.w36_data[tl][id_venue][param][327].numeric_value"
                              :style="validity.parametri.values[tl][id_venue][param][327] ? '':'border:2px solid red;'"
                              class="form-control"
                              :disabled="readonly"
                              @change="setMeasure(caldo.w36_data[tl][id_venue][param][327].id_w36_data,param,tl,327,caldo.w36_data[tl][id_venue][param][327].id_venue, false);
                                       calcolaSalvaAT(tl,id_venue,param,327);
                                       updateAllVenue(id_venue, tl)"
                            >
                          </td>
                          <td>
                            <input
                              type="Number"
                              :value="caldo.w36_data[tl][id_venue]['ATMIN'][0].numeric_value"
                              :style="validity.parametri.values[tl][id_venue]['ATMIN'][0] ? '':'border:2px solid red;'"
                              class="form-control"
                              :disabled="true" 
                            >
                          </td>
                        </tr> 
                        <tr>
                          <td>MAX</td>
                          <td
                            v-for="param in myParam"
                            :key="param"
                          >
                            <input
                              type="Number"
                              :value="caldo.w36_data[tl][id_venue][param][328].numeric_value"
                              :style="validity.parametri.values[tl][id_venue][param][328] ? '':'border:2px solid red;'"
                              class="form-control"
                              :disabled="readonly"
                              @change="setMeasure(caldo.w36_data[tl][id_venue][param][328].id_w36_data,param,tl,328,caldo.w36_data[tl][id_venue][param][328].id_venue, false);
                                       calcolaSalvaAT(tl,id_venue,param,328);
                                       updateAllVenue(id_venue, tl)"
                            >
                          </td>
                          <td>
                            <input
                              type="Number"
                              :value="caldo.w36_data[tl][id_venue]['ATMAX'][0].numeric_value"
                              :style="validity.parametri.values[tl][id_venue]['ATMAX'][0] ? '':'border:2px solid red;'"
                              class="form-control"
                              :disabled="true"
                            >
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div><!-- chiusura row -->
              </div>
            </div>
          </div>
          <!--  contenuto tab Epidemiologia-->
          <div
            v-show="selectedTab == 'Epidemiologia'"
            role="tabpanel"
          >
            <div v-if="ready">
              <br>
              <div class="row">
                <!-- tabella dati osservati ieri e l'altro ieri + previsti-->
                <div class="col">
                  <table class="table table-bordered">
                    <tbody>
                      <tr>
                        <th />
                        <th
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          {{ myDate[tl] }}
                        </th>
                        <th
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          {{ myDate[tl] }}
                        </th>
                        <th
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          {{ myDate[tl] }}
                        </th>
                      </tr>
                      <tr>
                        <td />
                        <th colspan="3">
                          valori variabili meteo/epidemiologiche
                        </th>
                        <th colspan="3">
                          classe di riferimento
                        </th>
                        <th colspan="3">
                          valore stima per equazione
                        </th>
                      </tr>
                      <!-- prime 3 righe con wda -->
                      <tr
                        v-for="(d, j) in configCaldo.wda"
                        :key="j"
                        :value="d.label"
                      >
                        <td>
                          {{ d.label }}
                        </td>
                        <td 
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          <input
                            type="Number"
                            style="background-color:  #e9f6fb"
                            :value="wda[59][tl][d.aggregazione].numeric_value"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>

                        <td
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          <input
                            type="Number"
                            style="background-color:  #e6fff9"
                            :value="valoreClasse(d.label,tl)"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>
                        <td
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          <input 
                            type="Number"
                            style="background-color:  #e9f6fb"
                            :value="valoreStima(d.label, valoreClasse(d.label,tl))"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>
                      </tr>
                      <!-- successive righe con gg cons e Atmin -->
                      <tr
                        v-for="(d, j) in configCaldo.param_equazione"
                        :key="j"
                        :value="d.label"
                      >
                        <td>
                          {{ d.label }}
                        </td>
                        <td
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          <input
                            type="Number"
                            style="background-color:  #e9f6fb"
                            :value="caldo.w36_data[ricavatl(d.id,tl)][59][d.parametro][d.aggregazione].numeric_value"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>
                        <td
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          <input
                            type="Number"
                            style="background-color:  #e6fff9"
                            :value="valoreClasse(d.label,tl)"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>
                        <td
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          <input
                            type="Number"
                            style="background-color:  #e9f6fb"
                            :value="valoreStima(d.label, valoreClasse(d.label, tl))"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>
                      </tr>
                      <tr>
                        <td>popday2 - decr.estivo</td>
                        <td
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          <input
                            style="background-color:  #e9f6fb"
                            type="Number"
                            :value="popday2[tl].numeric_value"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>
                        <td
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          <input
                            type="Number"
                            style="background-color:  #e6fff9"
                            :value="popday2[tl].numeric_value"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>
                        <td
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          <input
                            style="background-color:  #e9f6fb"
                            type="Number"
                            :value="valoreStima('popday2 - decr.estivo', popday2[tl].numeric_value)"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>
                      </tr>
                      <tr>
                        <td>dow - day of week</td>
                        <td
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          <input
                            style="background-color:  #e9f6fb"
                            type="Number"
                            :value="dayofweek[tl].numeric_value"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>
                        <td
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          <input
                            type="Number"
                            style="background-color:  #e6fff9"
                            :value="dayofweek[tl].numeric_value"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>
                        <td
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          <input
                            style="background-color:  #e9f6fb"
                            type="Number"
                            :value="valoreStima('dow - day of week', dayofweek[tl].numeric_value)"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>
                      </tr>
                      <tr>
                        <td
                          colspan="7"
                          style="border:3px solid #008000;' "
                        >
                          <b>Esponente k: Decessi previsti = decessi attesi * exp(k) </b>
                        </td>
                        <td
                          v-for="(v, tl) in myDate"
                          :key="tl"
                          style="border:3px solid #008000;' "
                        >
                          <input
                            type="Number"
                            :value="calcolaEsponente(tl)"
                            class="form-control"
                            :disabled="true"
                          >
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <!--  TABELLA DI EPIDEMIOLOGIA -->
                <div class="col">
                  <tr>
                    <table class="table table-bordered">
                      <tr>
                        <th
                          v-for="(v, tl) in myDate"
                          :key="tl"
                        >
                          {{ myDate[tl] }}
                        </th>
                      </tr>
                    </table>
                    <table class="table table-bordered">
                      <caption style="caption-side:top">
                        <b> Decessi attesi </b> 
                      </caption>
                      <tbody>
                        <tr>
                          <td
                            v-for="(v, tl) in myDate"
                            :key="tl"
                          > 
                            <input
                              type="Number"
                              :value="caldo.w36_data[tl][59]['ATTESI'][0].numeric_value"
                              class="form-control"
                              :disabled="true"
                            >
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </tr>
                  <!-- Decessi previsti = attesi * exp(k) -->
                  <tr>
                    <table class="table table-bordered">
                      <caption style="caption-side:top">
                        <b>Decessi PREVISTI = attesi * exp(k) </b>
                      </caption>
                      <tbody>
                        <tr>
                          <td
                            v-for="(v, tl) in myDate"
                            :key="tl"
                          > 
                            <input
                              type="Number" 
                              :value="calcolaPrevisti(tl)"
                              class="form-control"
                              :disabled="true"
                            >
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </tr>
                  <!-- Eccesso = previsti - attesi  -->
                  <tr>
                    <table class="table table-bordered">
                      <caption style="caption-side:top">
                        <b> ECCESSI = previsti - attesi</b>
                      </caption>
                      <tbody>
                        <tr />
                      
                        <tr>
                          <td
                            v-for="(v, tl) in myDate"
                            :key="tl"
                          > 
                            <input
                              type="Number" 
                              :value="calcolaEccessi(tl)"
                              class="form-control"
                              :disabled="true"
                            >
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </tr>
                  <!--CODICE SALUTE  -->
                  <tr>
                    <table class="table table-bordered">
                      <caption style="caption-side:top">
                        <b> CODICE SALUTE</b>
                      </caption>
                      <tbody>
                        <tr>
                          <td
                            v-for="(v, tl) in myDate"
                            :key="tl"
                          > 
                            {{ livelloEventi(caldo.w36_data[tl][59]['COD_SALUTE'][0].numeric_value) }}
                            <input
                              type="Number" 
                              :value="caldo.w36_data[tl][59]['COD_SALUTE'][0].numeric_value"
                              :style="validity.epidemiologia.values[tl][59]['COD_SALUTE'][0] ? '':'border:2px solid red;'"
                              class="form-control"
                              :disabled="readonly"
                              @change="setMeasure(caldo.w36_data[tl][59]['COD_SALUTE'][0].id_w36_data,'COD_SALUTE',tl,0,caldo.w36_data[tl][59]['COD_SALUTE'][0].id_venue, false)"
                            >
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </tr>
                  <tr>
                    <table class="table table-bordered">
                      <tbody>
                        <tr>
                          <td
                            v-for="(v, tl) in myDate"
                            :key="tl"
                          > 
                            <span v-if="caldo.w36_data[tl][59]['COD_SALUTE'][0].numeric_value===1">
                              <img
                                src="../templates/cod_salute_1.png"
                                class="img-fluid"
                                alt="Responsive image"
                              >
                            </span>
                            <span v-else-if="caldo.w36_data[tl][59]['COD_SALUTE'][0].numeric_value===2">
                              <img
                                src="../templates/cod_salute_2.png"
                                class="img-fluid"
                                alt="Responsive image"
                              >
                            </span>
                            <span v-else-if="caldo.w36_data[tl][59]['COD_SALUTE'][0].numeric_value===3">
                              <img
                                src="../templates/cod_salute_3.png"
                                class="img-fluid"
                                alt="Responsive image"
                              >
                            </span>
                            <span v-else>
                              <img
                                src="../templates/cod_salute_0.png"
                                class="img-fluid"
                                alt="Responsive image"
                              >
                            </span>
                          </td>
                        </tr>
                        <br>
                        <tr>
                          <td colspan="2">
                            solo se nei 3 gg precedenti il sistema era acceso almeno un gg
                          </td>
                        </tr>
                        <tr>
                          <td><b>eccessi</b></td>
                          <td><b>codice salute</b></td>
                        </tr>
                        <tr>
                          <td>eccesso &le; 2 </td>
                          <td>assente</td>
                        </tr>
                        <tr>
                          <td>2 &lt; eccesso &le; 5 </td>
                          <td>basso</td>
                        </tr>
                        <tr>
                          <td>5 &lt; eccesso &le; 10 </td>
                          <td>medio</td>
                        </tr>
                        <tr>
                          <td>eccesso &gt; 10 </td>
                          <td>alto </td>
                        </tr>
                      </tbody>
                    </table>
                  </tr>
                </div>
              </div>
            </div>
          </div>
          <!--  contenuto tab Osservati-->
          <div
            v-show="selectedTab == 'Osservati'"
            role="tabpanel"
          >
            <!-- ancore di navigazione sugli osservati -->
            <nav
              class="navbar justify-content-center sticky-top bg-light border-bottom"
              style="top: 80px;margin-top:-9px;height:40px;"
            >
              <ul class="nav">
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('osservati_table_torino')"
                  >
                    TO
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('osservati_table_biella')"
                  >
                    BI
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('osservati_table_alessandria')"
                  >
                    AL
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('osservati_table_asti')"
                  >
                    AT
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('osservati_table_cuneo')"
                  >
                    CN
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('osservati_table_novara')"
                  >
                    NO
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('osservati_table_verbania')"
                  >
                    VB
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('osservati_table_vercelli')"
                  >
                    VC
                  </a>
                </li>
                <li class="nav-item px-1">
                  <a
                    class="nav-link"
                    @click="goto('debug')"
                  >
                    DEBUG
                  </a>
                </li>
              </ul>
            </nav>
            <div
              v-if="ready"
              id="table_top"
              style="scroll-margin-top: 120px;"
            >
              <div class="d-flex justify-content-end">
                <button @click="downloadCsv">
                  Download CSV
                </button>
              </div>
              <ag-grid-vue
                :row-data="rowData"
                :column-defs="colDefs"
                style="height: 500px"
                class="ag-theme-quartz"
                @gridReady="onGridReady"
              />
              <br>
              <div
                id="osservati_table_biella"
                style="scroll-margin-top: 120px;"
                class="row"
              >
                <h6>Biella</h6>
                <div class="col">
                  <LineChart
                    :data="chartBiella"
                    :options="chartOptions"
                    style="height:70px;"
                  />
                  <div
                    v-html="osservati_table_biella"
                  />
                </div>
              </div>
              <div
                id="osservati_table_alessandria"
                style="scroll-margin-top: 120px;" 
                class="row"
              >
                <h6>Alessandria</h6>
                <div class="col">
                  <LineChart
                    :data="chartAlessandria"
                    :options="chartOptions"
                    style="height:70px;"
                  />
                  <div
                    v-html="osservati_table_alessandria"
                  />
                </div>
              </div>
              <div
                id="osservati_table_asti"
                style="scroll-margin-top: 120px;"
                class="row"
              >
                <h6>Asti</h6>
                <div class="col">
                  <LineChart
                    :data="chartAsti"
                    :options="chartOptions"
                    style="height:70px;"
                  />
                  <div
                    v-html="osservati_table_asti"
                  />
                </div>
              </div>
              <div
                id="osservati_table_cuneo"
                style="scroll-margin-top: 120px;"
                class="row"
              >
                <h6>Cuneo</h6>
                <div class="col">
                  <LineChart
                    :data="chartCuneo"
                    :options="chartOptions"
                    style="height:70px;"
                  />
                  <div
                    v-html="osservati_table_cuneo"
                  />
                </div>
              </div>
              <div
                id="osservati_table_novara"
                style="scroll-margin-top: 120px;"
                class="row"
              >
                <h6>Novara</h6>
                <div class="col">
                  <LineChart
                    :data="chartNovara"
                    :options="chartOptions"
                    style="height:70px;"
                  />
                  <div
                    v-html="osservati_table_novara"
                  />
                </div>
              </div>
              <div
                id="osservati_table_torino"
                style="scroll-margin-top: 120px;"
                class="row"
              >
                <h6>Torino</h6>
                <div class="col">
                  <LineChart
                    :data="chartTorino"
                    :options="chartOptions"
                    style="height:70px;"
                  />
                  <div
                    v-html="osservati_table_torino"
                  />
                </div>
              </div>
              <div
                id="osservati_table_verbania"
                style="scroll-margin-top: 120px;"
                class="row"
              >
                <h6>Verbania</h6>
                <div class="col">
                  <LineChart
                    :data="chartVerbania"
                    :options="chartOptions"
                    style="height:70px;"
                  />
                  <div
                    v-html="osservati_table_verbania"
                  />
                </div>
              </div>
              <div
                id="osservati_table_vercelli"
                style="scroll-margin-top: 120px;"
                class="row"
              >
                <h6>Vercelli</h6>
                <div class="col">
                  <LineChart
                    :data="chartVercelli"
                    :options="chartOptions"
                    style="height:70px;"
                  />
                  <div
                    v-html="osservati_table_vercelli"
                  />
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <div
                    id="debug"
                    style="scroll-margin-top: 120px;"
                    v-html="debug_text"
                  />
                </div>
              </div>
              <div
                v-if="isTop"
                class="d-flex justify-content-end"
                style="height:100px;position: fixed;bottom: 10px;right: 0px;"
              >
                <button
                  type="button"
                  class="btn btn-outline-dark h-50"
                  @click="goto('table_top')"
                >
                  TOP
                </button>
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
    name: 'MyCaldo',
    components: {
      MapCaldo,
      AgGridVue,
      LineChart
    }
  }
  
</script>

<script setup lang="ts">
import { Ref, ref, onMounted, computed, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vue-toast-notification'

import Modal from 'bootstrap/js/dist/modal'

import api from '../../src/api'
import store from '../../src/store'

import 'leaflet/dist/leaflet.css'
import MapCaldo from './MapCaldo.vue'

import { components } from '../../src/types/weboll'
import { configCaldo } from "../config";
import exp from 'constants'

import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the Data Grid
import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the Data Grid
import { AgGridVue } from "ag-grid-vue3"; // Vue Data Grid Component

import { Line as LineChart } from 'vue-chartjs';
import 'chartjs-adapter-date-fns';
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
  TimeScale
)

const router = useRouter()
const route = useRoute()
const toast = useToast()
const divMap = ref("")

const myVenues = {
  1:	'BI',
  9:	'AL',
  11:	'AT',
  28:	'CN',
  33:	'NO',
  59:	'TO',
  63:	'VB',
  64:	'VC'
}

const idVenue2Name = {
  1:	'Biella',
  9:	'Alessandria',
  11:	'Asti',
  28:	'Cuneo',
  33:	'Novara',
  59:	'Torino',
  63:	'Verbania',
  64:	'Vercelli'
}

const idAggreg2Name = {
  940: "75° percentile",
  941: "90° percentile",
  942: "95° percentile"
}

const codiceColore = {
  0: 'VERDE',
  1: 'GIALLO',
  2: 'ARANCIONE',
  3: 'ROSSO'
}

const myParam = ['TERMA', 'IGRO', 'VELV']

const owner = ref("")
let loading = ref(true)

onMounted(() => {
  if(typeof route.params.id === 'string'){
    caldo_id.value = parseInt(route.params.id)
  }
  // console.log("store.state.caldo_first", store.state.caldo_first)
  fetchData()
})

//reactive properties
let caldo_id = ref(NaN)
let caldo = ref({
  id_w36: 0,
  data_emissione: '',
  status: '',
  note: '',
  internal_note: '',
  osservati: '',
  debug: '',
  last_update: '',
  username: '',
  w36_data: {},
	w36data_set: {}
})
let image_max = ref({})
let image_min = ref({})
let parametri = ref({})

let state = ref(store.state)
let ready = ref(false)
let readonly = ref(false)
let actions = ref({
  sending: false,
  saving: false,
  reopening: false,
  tempreloading: false,
  userchanging: false
})

let countdown = ref(0)
let selectedTab = ref('Capoluoghi')
const props = defineProps({
    id: {
        type: String,
        default: () => ''
    },
})

let myDate = ref({
  48: '',
  66: '',
  83: ''
})

let myDateEpidem = ref({
  15: '',
  32: '',
  48: ''
})

// definisco degli indici altrimenti non visualizza
// l'ordine corretto temporale nel ciclo for ma ordina crescente
let myDateTorino = ref({
  0: [301,''],  // 4 giorni fa
  1: [300,''], // 3 gg fa
  2: [15,''], // l'altroieri
  3: [32,''] // ieri
})

let tl_ieri = {
  48: 32,
  66: 48,
  83: 66
}
let tl_altroieri = {
  48: 15,
  66: 32,
  83: 48
}

function livelloEventi(livello) {
  let result = "NON CODIFICATO!"
  if (livello === 0) result = "Assente"
  if (livello === 1) result = "Basso"
  if (livello === 2) result = "Medio"
  if (livello === 3) result = "Alto"
  return result
}

let isTop = ref(false)

let wda = ref({})
let colore = ref({})
let gg_cons_modificabili = ref(false)

const today = computed(() => {
  let d = new Date()
  return d.toISOString().substring(0, 10)
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
      },
      y1: {
        position: "right",
        title: {
          display: true,
          text: "Umidità %"
        },
      },
      y2: {
        position: "right",
        title: {
          display: true,
          text: "Velocità vento m/s"
        },
      }
    }
  }
  return result
})

function getData(venue){
  let result = {labels: [], datasets: []}
  let perc75_ds = {label: '75%', backgroundColor: 'yellow', borderColor: 'yellow', pointRadius: 0, yAxisID: 'y'}
  let perc90_ds = {label: '90%', backgroundColor: 'orange', borderColor: 'orange', pointRadius: 0, yAxisID: 'y'}
  let perc95_ds = {label: '95%', backgroundColor: 'red', borderColor: 'red', pointRadius: 0, yAxisID: 'y'}
  let velv_ds = {label: 'velv', backgroundColor: '#80df78', borderColor: '#80df78', yAxisID: 'y2', hidden: true}
  let igro_ds = {label: 'igro', backgroundColor: '#76b7e7', borderColor: '#76b7e7', yAxisID: 'y1', hidden: true}
  let terma_ds = {label: 'terma', backgroundColor: '#f28f9c', borderColor: '#f28f9c', yAxisID: 'y'}
  let at_ds = {label: 'at', backgroundColor: '#901726', borderColor: '#901726', yAxisID: 'y'}
  var separateLines = caldo.value.osservati.split(/\r?\n|\r|\n/g);
  let skip_header = true
  separateLines.forEach(element => {
    if (!(skip_header)){
      element = element.replaceAll("nan", "null")
      let valori = element.split(";")
      if (valori[0] == venue){
        if (result["labels"].indexOf(valori[1]) == -1 )
          result["labels"].push(valori[1])
      }
    }else{
      skip_header = false
    }
  })
  result["labels"].sort(function(a,b){
    return new Date(a) - new Date(b);
  });
  // console.log(result["labels"])
  terma_ds["data"] = Array.apply(null, Array(result["labels"].length)).map(function () {})
  igro_ds["data"] = Array.apply(null, Array(result["labels"].length)).map(function () {})
  velv_ds["data"] = Array.apply(null, Array(result["labels"].length)).map(function () {})
  at_ds["data"] = Array.apply(null, Array(result["labels"].length)).map(function () {})
  perc75_ds["data"] = Array.apply(null, Array(result["labels"].length)).map(function () {})
  perc90_ds["data"] = Array.apply(null, Array(result["labels"].length)).map(function () {})
  perc95_ds["data"] = Array.apply(null, Array(result["labels"].length)).map(function () {})
  separateLines.forEach(element => {
    if (!(skip_header)){
      element = element.replaceAll("nan", "null")
      let valori = element.split(";")
      if (valori[0] == venue){
        let terma = valori[3]
        let igro = valori[4]
        let velv = valori[5]
        let at = valori[6]
        let perc75 = valori[7]
        let perc90 = valori[8]
        let perc95 = valori[9]
        let index = result["labels"].indexOf(valori[1])
        terma_ds["data"][index] = terma
        igro_ds["data"][index] = igro
        velv_ds["data"][index] = velv
        at_ds["data"][index] = at
        perc75_ds["data"][index] = perc75
        perc90_ds["data"][index] = perc90
        perc95_ds["data"][index] = perc95
      }
    }else{
      skip_header = false
    }
  })
  result["datasets"].push(at_ds)
  result["datasets"].push(terma_ds)
  result["datasets"].push(igro_ds)
  result["datasets"].push(velv_ds)
  result["datasets"].push(perc75_ds)
  result["datasets"].push(perc90_ds)
  result["datasets"].push(perc95_ds)
  return result
}

const chartBiella = computed(() => {
  let result = getData("Biella")
  return result
})

const chartAlessandria = computed(() => {
  let result = getData("Alessandria")
  return result
})

const chartAsti = computed(() => {
  let result = getData("Asti")
  return result
})

const chartCuneo = computed(() => {
  let result = getData("Cuneo")
  return result
})

const chartNovara = computed(() => {
  let result = getData("Novara")
  return result
})

const chartTorino = computed(() => {
  let result = getData("Torino")
  return result
})

const chartVerbania = computed(() => {
  let result = getData("Verbania")
  return result
})

const chartVercelli = computed(() => {
  let result = getData("Vercelli")
  return result
})

// Column Definitions: Defines the columns to be displayed.
const colDefs = ref([
  { field: "venue" , filter: true, floatingFilter: true, flex: 1 },
  { field: "data", filter: true, floatingFilter: true, flex: 1 },
  { field: "parametro", filter: true, floatingFilter: true, flex: 1,
    cellStyle: function(params) {
      let background = ""
      let color = ""
      var parametro = params.node.data.parametro
      if (parametro == 'ATMAX'){
        background = "#FFCCCC"
        color = "black"
      } else if (parametro == 'ATMIN'){
        background = "#99ebff"
        color = "black"
      }
      return {
        background: background,
        color: color
      }
    }
  },
  { field: "terma", flex: 1,
    cellStyle: function(params) {
      let background = ""
      let color = ""
      var terma = params.node.data.terma
      if (terma == -9999){
        background = "#d7d5d0"
        color = "black"
      }
      return {
        background: background,
        color: color
      }
    }
  },
  { field: "igro", flex: 1,
    cellStyle: function(params) {
      let background = ""
      let color = ""
      var igro = params.node.data.igro
      if (igro == -9999){
        background = "#d7d5d0"
        color = "black"
      }
      return {
        background: background,
        color: color
      }
    }
  },
  { field: "velv", flex: 1,
    cellStyle: function(params) {
      let background = ""
      let color = ""
      var velv = params.node.data.velv
      if (velv == -9999){
        background = "#d7d5d0"
        color = "black"
      }
      return {
        background: background,
        color: color
      }
    }
  },
  { 
    field: "at", 
    flex: 1, 
    cellStyle: function(params) {
      var at = params.node.data.at
      var perc75 = params.node.data.perc75
      var perc90 = params.node.data.perc90
      var perc95 = params.node.data.perc95
      let background = ""
      let color = ""
      if (!(at=="nan")){
        perc75 = parseFloat(perc75)
        perc90 = parseFloat(perc90)
        perc95 = parseFloat(perc95)
        if (at > perc95){
          background = "red"
          color = "white"
        }else if (at > perc90){
          background = "orange"
          color = "black"
        }else if (at > perc75){
          background = "yellow"
          color = "black"
        }else if (at == -9999){
          background = "#d7d5d0"
          color = "black"
        }
        return {
          background: background,
          color: color
        }
      }
    }
  },
  { field: "perc75", flex: 1 },
  { field: "perc90", flex: 1 },
  { field: "perc95", flex: 1 },
])

const rowData = computed(() => {
  /*
  const rowData = ref([
   { make: "Tesla", model: "Model Y", price: 64950, electric: true },
   { make: "Ford", model: "F-Series", price: 33850, electric: false },
   { make: "Toyota", model: "Corolla", price: 29600, electric: false },
  ])
  */
  let result = []
  var separateLines = caldo.value.osservati.split(/\r?\n|\r|\n/g);
  let skip_header = true
  separateLines.forEach(element => {
    if (!(skip_header)){
      let valori = element.split(";")
      let terma = valori[3]
      let igro = valori[4]
      let velv = valori[5]
      let at = valori[6]
      let perc75 = valori[7]
      let perc90 = valori[8]
      let perc95 = valori[9]
      if (!(terma == "nan")) terma = parseFloat(terma)
      else terma=-9999
      if (!(igro == "nan")) igro = parseFloat(igro)
      else igro=-9999
      if (!(velv == "nan")) velv = parseFloat(velv)
      else velv=-9999
      if (!(at == "nan")) at = parseFloat(at)
      else at=-9999
      if (!(perc75 == "nan")) perc75 = parseFloat(perc75)
      else perc75=-9999
      if (!(perc90 == "nan")) perc90 = parseFloat(perc90)
      else perc90=-9999
      if (!(perc95 == "nan")) perc95 = parseFloat(perc95)
      else perc95=-9999
      let dict = {
        'venue': valori[0], 
        'data': valori[1], 
        'parametro': valori[2], 
        'terma': terma,
        'igro': igro,
        'velv': velv,
        'at': at,
        'perc75': perc75,
        'perc90': perc90,
        'perc95': perc95
      }
      result.push(dict)
    }else{
      skip_header = false
    }
  })
  return result
})

const gridApi = ref(null);

function getYesterdaysDate() {
  var date = new Date(caldo.value.data_emissione);
  date.setDate(date.getDate()-1);
  var month = (date.getMonth() + 1).toString()
  if (month.length == 1 ) month = '0' + month
  var day = (date.getDate()).toString()
  if (day.length == 1 ) day = '0' + day
  return date.getFullYear() + '-' + month + '-' + day;
}

const onGridReady = (params) => {
  gridApi.value = params.api;

  // Apply filter on startup
  gridApi.value.setFilterModel({
    venue: {
      type: 'contains',
      filter: 'Torino',
    },
    data: {
      type: 'contains',
      filter: getYesterdaysDate(),
    },
    parametro: {
      type: 'contains',
      filter: 'ATMAX',
    },
  });
};

function osservati_table(venue){
  let str = '<table class="table table-striped table-hover table-bordered tableFixHead" style="width:100%">'
  var separateLines = caldo.value.osservati.split(/\r?\n|\r|\n/g);
  let head_line = true
  separateLines.forEach(element => {
    if (head_line){
      str = str + "<thead>"
      str = str + "<tr><td>"
      str = str + element.replaceAll(";", "</td><td>");
      str = str + "</td></tr>"
      str = str + "</thead>"
      head_line = false
    }else{
      let valori = element.split(";")
      if (valori[0] == venue){
        let colore = ""
        if (!(valori[6] == "nan") && !(valori[7] == "nan") && !(valori[8] == "nan") && !(valori[9] == "nan")){
          if (parseFloat(valori[6]) >= parseFloat(valori[9])){
            colore = ' style="background-color:red;color:white;" '
          }else if (parseFloat(valori[6]) >= parseFloat(valori[8])){
            colore = ' style="background-color:orange;" '
          }else if (parseFloat(valori[6]) >= parseFloat(valori[7])){
            colore = ' style="background-color:yellow;" '
          }
        }
        let colore_parametro = ""
        if (valori[2] == "ATMIN") colore_parametro = ' style="background-color:#99ebff;" '
        if (valori[2] == "ATMAX") colore_parametro = ' style="background-color:#FFCCCC;" '
        str = str + "<tr><td>" + valori[0] + "</td>"
        str = str + "<td>" + valori[1] + "</td>"
        str = str + "<td "+ colore_parametro + ">" + valori[2] + "</td>"
        str = str + "<td>" + valori[3] + "</td>"
        str = str + "<td>" + valori[4] + "</td>"
        str = str + "<td>" + valori[5] + "</td>"
        str = str + "<td" + colore + ">" + valori[6] + "</td>"
        str = str + "<td>" + valori[7] + "</td>"
        str = str + "<td>" + valori[8] + "</td>"
        str = str + "<td>" + valori[9] + "</td></tr>"
      }
    }
  })
  str = str + "</table>"
  return str
}

const osservati_table_alessandria = computed(() => {
  let str = osservati_table("Alessandria")
  return str
})

const osservati_table_asti = computed(() => {
  let str = osservati_table("Asti")
  return str
})

const osservati_table_biella = computed(() => {
  let str = osservati_table("Biella")
  return str
})

const osservati_table_cuneo = computed(() => {
  let str = osservati_table("Cuneo")
  return str
})

const osservati_table_novara = computed(() => {
  let str = osservati_table("Novara")
  return str
})

const osservati_table_torino = computed(() => {
  let str = osservati_table("Torino")
  return str
})

const osservati_table_verbania = computed(() => {
  let str = osservati_table("Verbania")
  return str
})

const osservati_table_vercelli = computed(() => {
  let str = osservati_table("Vercelli")
  return str
})

const debug_text = computed(() => {
  let str = ""
  if (caldo.value.debug){
    if (caldo.value.debug.length > 0){
      let linee = caldo.value.debug.split("\n")
      linee.forEach(element => {
        let dati = element.split(",")
        if (dati[0] == "at_element"){
          dati[1] = idVenue2Name[dati[1]]
          str = str + dati.join(",") + "<br>"
        }
        if (dati[0] == "giorni_di_caldo"){
          let json_str = element.replaceAll("giorni_di_caldo,","")
          json_str = json_str.replaceAll("'","\"")
          let json = JSON.parse(json_str)
          for (const [key, value] of Object.entries(json)) {
            str = str + "giorni_di_caldo," + idVenue2Name[key] + "," + JSON.stringify(value) + "<br>"
          }
        }
        if (dati[0] == "tot_giorni_di_caldo"){
          let json_str = element.replaceAll("tot_giorni_di_caldo,","")
          json_str = json_str.replaceAll("'","\"")
          let json = JSON.parse(json_str)
          for (const [key, value] of Object.entries(json)) {
            str = str + "tot_giorni_di_caldo," + idVenue2Name[key] + "," + JSON.stringify(value) + "<br>"
          }
        }
      })
    }
  }
  return str
})

// per equazione di epidemiologia: dow:1 domenica, 7 sabato
const dayofweek = computed(() => {
  let day = {}
  for (const [tl, valuetl] of Object.entries(myDate.value)) {
    day[tl] = {}
    let d = valuetl
    let anno = d.substring(6, 10)
    let mese = d.substring(3, 5)
    let giorno = d.substring(0, 2)
    d = new Date(anno + "-" + mese + "-" + giorno)
    console.log("d", d)
    day[tl] = {'numeric_value': d.getDay() + 1} 
  }
  console.log("day", day)
  return day
})

// per equazione di epidemiologia - decremento estivo
const popday2 = computed(() => {
  let popday = {}
  for (const [tl, valuetl] of Object.entries(myDate.value)) {
    popday[tl] = {}
    let d = valuetl
    let anno = d.substring(6, 10)
    let mese = d.substring(3, 5)
    let giorno = d.substring(0, 2)
    
    // ricavo in che giorno cade ferragosto quest'anno
    let dow_fa = new Date('August 15, ' + anno + ' 12:00:00').getDay() + 1;
    // assunzione della distribuzione delle due settimane intorno a ferragosto
    if ( dow_fa==1 && mese=='08' && Number(giorno) >= 7 && Number(giorno) <= 22 ) {
      popday=2 
    }else if ( dow_fa==2 && mese=='08' && Number(giorno) >= 6 && Number(giorno) <= 21 ){
      popday[tl] = {'numeric_value': 2}
    }else if ( dow_fa==4 && mese=='08' && Number(giorno) >= 4 && Number(giorno) <= 19 ){
      popday[tl] = {'numeric_value': 2}
    }else if ( dow_fa==5 && mese=='08' && Number(giorno) >= 3 && Number(giorno) <= 18 ){
      popday[tl] = {'numeric_value': 2}
    }else if ( dow_fa==6 && mese=='08' && Number(giorno) >= 9 && Number(giorno) <= 24 ){
      popday[tl] = {'numeric_value': 2}
    }else if ( dow_fa==7 && mese=='08' && Number(giorno) >= 8 && Number(giorno) <= 23 ){
      popday[tl] = {'numeric_value': 2}
    }else if ( Number(giorno) <= 31 && mese == '08'){
      popday[tl] = {'numeric_value': 1}
    }else if ( Number(giorno) >=16 && Number(giorno) <=31  && mese == '07') {
      popday[tl] = {'numeric_value': 1}
    } else {	 
      popday[tl] = {'numeric_value': 9}
    }
  }
  return popday
})

async function updateAll(){
  loading.value=true
  await varWda()
  await varGiorniCons()
  await varColore()
  loading.value=false
}

async function updateAllVenue(id_venue, tl){
  // console.log("updateAllVenue", id_venue, tl)
  let inizio = new Date().getMilliseconds()
  loading.value=true
  let stack : Array<Object> = []
  await varWdaVenue(id_venue, tl, true)
  let mystack = await varGiorniConsVenue(id_venue, false)
  mystack.forEach(element => {
    stack.push(element)
  })
  mystack = await varColoreVenue(id_venue, false)
  mystack.forEach(element => {
    stack.push(element)
  })
  if (caldo.value.status === 'X' || caldo.value.status === '0') await saveW36(stack)
  loading.value=false
  console.log("updateAllVenue fine millisecondi", (new Date().getMilliseconds()) - inizio)
}

async function varWdaVenue(id_venue, tl, notify){
  let myAggreg = [940, 941, 942]
  if (!(id_venue in wda.value))
    wda.value[id_venue] = {}
  if (!(tl in wda.value[id_venue]))
    wda.value[id_venue][tl] = {}
  myAggreg.forEach(aggreg => {
    let atmax_prevista = caldo.value.w36_data[tl][id_venue]['ATMAX'][0].numeric_value
    let atmin_prevista = caldo.value.w36_data[tl][id_venue]['ATMIN'][0].numeric_value
    let atmax_percentile = caldo.value.w36_data[tl][id_venue]['ATMAX'][aggreg].numeric_value
    let atmin_percentile = caldo.value.w36_data[tl][id_venue]['ATMIN'][aggreg].numeric_value
    let cc = calcolaWda(atmax_prevista, atmax_percentile, atmin_prevista, atmin_percentile, notify, id_venue, tl, aggreg)
    console.log("\tvarWdaVenue - atmax_prevista, atmax_percentile, atmin_prevista, atmin_percentile", id_venue, tl, aggreg, atmax_prevista, atmax_percentile, atmin_prevista, atmin_percentile, cc)
    wda.value[id_venue][tl][aggreg] = {'numeric_value': cc}
  });
  if (id_venue == 59){
    var tloss = [15, 32]
    // nel caso di Torino devo calcolare il wda anche per il giorno precedente
    for (var ii=0; ii < tloss.length; ii++) {
      var mytl = tloss[ii]
      if (!(mytl in wda.value[id_venue]))
        wda.value[id_venue][mytl] = {}
      myAggreg.forEach(aggreg => {
        let atmax_prevista = caldo.value.w36_data[mytl][id_venue]['ATMAX'][0].numeric_value
        let atmin_prevista = caldo.value.w36_data[mytl][id_venue]['ATMIN'][0].numeric_value
        let atmax_percentile = caldo.value.w36_data[mytl][id_venue]['ATMAX'][aggreg].numeric_value
        let atmin_percentile = caldo.value.w36_data[mytl][id_venue]['ATMIN'][aggreg].numeric_value

        let cc = calcolaWda(atmax_prevista, atmax_percentile, atmin_prevista, atmin_percentile, notify, id_venue, mytl, aggreg)
        wda.value[id_venue][mytl][aggreg] = {'numeric_value': cc}
      })
    }
  }
  console.log("\tvarWdaVenue - return", id_venue, tl, wda.value[id_venue][tl])
}

function varWda(){
  console.log("varWda - inizio")
  for (const [id_venue, valueV] of Object.entries(myVenues)) {
    for (const [tl, valuetl] of Object.entries(myDate.value)) {
      varWdaVenue(id_venue, tl, false)
    }
  }
  var tloss = [15, 32]
  var id_venue = 59
  // nel caso di Torino devo calcolare il wda anche per il giorno precedente
  for (var ii=0; ii < tloss.length; ii++) {
    var tl = tloss[ii]
    varWdaVenue(id_venue, tl)
  }
  console.log("varWda - fine")
}

async function varGiorniConsVenue(id_venue, save){
  // variabile computed per il calcolo dei giorni consecutivi di caldo nei 3 gg di previsione
  // incrementa il valore di ggcons del giorno precedente se l'indice wda si accende
  console.log("\tvarGiorniConsVenue", id_venue, save)
  let stack : Array<Object> = []
  let map_ggprec = {48: 32, 66: 48, 83: 66}
  // ciclo per ogni venue
  for (const [tl, valuetl] of Object.entries(myDate.value)) {
    let tl_ggprec = map_ggprec[tl]
    let ggcons_ieri = caldo.value.w36_data[tl_ggprec][id_venue]['GGCONS'][0].numeric_value
    let wda75 = wda.value[id_venue][tl][940].numeric_value
    if (ggcons_ieri == null) {
      ggcons_ieri = 0
    }
    if (wda75 == 1) {
      if (!(caldo.value.w36_data[tl][id_venue]['GGCONS'][0].locked))
        caldo.value.w36_data[tl][id_venue]['GGCONS'][0].numeric_value = (ggcons_ieri + 1)
    } else {
      if (!(caldo.value.w36_data[tl][id_venue]['GGCONS'][0].locked))
        caldo.value.w36_data[tl][id_venue]['GGCONS'][0].numeric_value = 0
    }

    let id_w36_data = caldo.value.w36_data[tl][id_venue]["GGCONS"][0].id_w36_data
    let w36data = caldo.value.w36_data[tl][id_venue]["GGCONS"][0]
    let value = caldo.value.w36_data[tl][id_venue]['GGCONS'][0].numeric_value
    
    const payload = {"id_key":"id_w36_data","id":id_w36_data,"value_key": "numeric_value","new_value": value}
    w36data.numeric_value = value
    stack.push(payload)
    if (id_venue == 59) await calcolaCodiceSalute(calcolaEccessi(tl), tl)
  }
  const payloadusername = {"id_key":"id_w36","id":caldo.value.id_w36,"value_key":"username","new_value": store.state.username}
  stack.push(payloadusername)
  if (save)
    if (caldo.value.status === 'X' || caldo.value.status === '0') await saveW36(stack)
  // console.log("varGiorniConsVenue - return", stack)
  return stack
}

async function varGiorniCons(){
  // variabile computed per il calcolo dei giorni consecutivi di caldo nei 3 gg di previsione
  // incrementa il valore di ggcons del giorno precedente se l'indice wda si accende
  // ciclo per ogni venue
  console.log("varGiorniCons - inizio")
  let stack : Array<Object> = []
  for (const [id_venue, valueV] of Object.entries(myVenues)) {
    let mystack = await varGiorniConsVenue(id_venue, false)
    mystack.forEach(element => {
      stack.push(element)
    })
  }
  // console.log("varGiorniCons - stack", stack)
  if (caldo.value.status === 'X' || caldo.value.status === '0') await saveW36(stack)
  console.log("varGiorniCons - fine")
}

async function varColoreVenue(id_venue, save){
  console.log("\tvarColoreVenue", id_venue, save)
  let stack : Array<Object> = []
  for (const [tl, valuetl] of Object.entries(myDate.value)) {
    if (!(id_venue in colore.value))
      colore[id_venue] = {}
            
    let w36data = caldo.value.w36_data[tl][id_venue]["COD_COLORE"][0]
    let w36data_orig = caldo.value.w36_data[tl][id_venue]["COD_COLORE_ORIG"][0]
    
    let wda75 = wda.value[id_venue][tl][940].numeric_value
    let wda90 = wda.value[id_venue][tl][941].numeric_value
    let wda95 = wda.value[id_venue][tl][942].numeric_value
    console.log("\tvarColoreVenue - wda75 wda90 wda95", id_venue, tl, wda75, wda90, wda95)
    let myggcons = caldo.value.w36_data[tl][id_venue]['GGCONS'][0].numeric_value
    let atmax = caldo.value.w36_data[tl][id_venue]['ATMAX'][0].numeric_value

    if (wda95 == 1) {
      if (myggcons >= 3) {
        colore[id_venue][tl] = {'numeric_value': 3}
      } else {
        colore[id_venue][tl] = {'numeric_value': 2}
      }
    } else if (wda90 == 1) {
      colore[id_venue][tl] = {'numeric_value': 2}
    } else if (wda75 == 1) {
      colore[id_venue][tl] = {'numeric_value': 1}
    } else {
      colore[id_venue][tl] = {'numeric_value': 0}
    }

    // console.log("w36data.locked", w36data.locked, !(w36data.locked))
    if (!(w36data.locked)){
      let id_w36_data = w36data.id_w36_data  
      // console.log("modifico COD_COLORE", id_venue, tl, id_w36_data)
      let value = colore[id_venue][tl].numeric_value
      const payload = {"id_key":"id_w36_data","id":id_w36_data,"value_key": "numeric_value","new_value": value}
      w36data.numeric_value = value
      stack.push(payload)
    }
    let id_w36_data_orig = w36data_orig.id_w36_data  
    // console.log("modifico COD_COLORE_ORIG", id_venue, tl, id_w36_data_orig)
    let value = colore[id_venue][tl].numeric_value
    const payload = {"id_key":"id_w36_data","id":id_w36_data_orig,"value_key": "numeric_value","new_value": value}
    w36data_orig.numeric_value = value
    stack.push(payload)
    const payloadusername = {"id_key":"id_w36","id":caldo.value.id_w36,"value_key":"username","new_value": store.state.username}
    stack.push(payloadusername)
    if (save)
      if (caldo.value.status === 'X' || caldo.value.status === '0') await saveW36(stack)
  }
  return stack
}

async function varColore(){
  console.log("varColore - inizio")
  let stack : Array<Object> = []
  for (const [id_venue, valueV] of Object.entries(myVenues)) {
    let mystack = await varColoreVenue(id_venue, false)
    mystack.forEach(element => {
      stack.push(element)
    })
  }
  if (caldo.value.status === 'X' || caldo.value.status === '0') await saveW36(stack)
  console.log("varColore - fine")
}

const ATcalcolata = computed(() => {
  let tempApparente = {}
  let myAggreg = [327, 328]
  if (ready.value ){
    for (const [id_venue, valueV] of Object.entries(myVenues)) {
      tempApparente[id_venue] = {}
      for (const [tl, valuetl] of Object.entries(myDate.value)) {
        tempApparente[id_venue][tl] = {}
        myAggreg.forEach(aggreg => {
          let igro = caldo.value.w36_data[tl][id_venue]['IGRO'][aggreg].numeric_value
          let velv = caldo.value.w36_data[tl][id_venue]['VELV'][aggreg].numeric_value
          let terma = caldo.value.w36_data[tl][id_venue]['TERMA'][aggreg].numeric_value
          
          //Calcolo della temperatura apparente
          // e=6.112*10^(7.5*T/(237.7+T))*RH/100  tensione di vapore saturo
          // AT=-2.7+1.04*T+2*e/10-0.65V

          let e = 6.112 * 10 **((7.5 * terma) / (237.7 + terma)) * igro / 100
          let at = -2.7 + 1.04 * terma + 2 * e / 10 - 0.65 * velv
          tempApparente[id_venue][tl][aggreg] = {'numeric_value': Math.round(at * 10) / 10}
        })
      }
    }
  }
  return tempApparente
})

const validity = computed(() => {
  let validity = {
    global: true,
    capoluoghi: {tab: true, values: {}, internal_note: true },
    torino: {tab: true, values: {}},
    parametri: {tab: true, values: {}},
    epidemiologia: {tab: true, values: {}},
  }
  let soglie = {
    terma_max: 50,
    terma_min: -30,
    atmax_max: 70,
    atmax_min: -50,
    atmin_max: 70,
    atmin_min: -50,
    igro_max: 100,
    igro_min: 0,
    velv_max: 400,
    velv_min: 0
  }
  if (ready.value){
    // tab capoluoghi
    for (const [tl, tl_value] of Object.entries(myDate.value)) {
      if (!(tl in validity.capoluoghi.values)) validity.capoluoghi.values[tl] = {}
      for (const [venue, venue_value] of Object.entries(myVenues)) {
        if (!(venue in validity.capoluoghi.values[tl])) validity.capoluoghi.values[tl][venue] = {}
        // controlla i GGCONS
        if (!('GGCONS' in validity.capoluoghi.values[tl][venue])) 
          validity.capoluoghi.values[tl][venue]['GGCONS'] = {}
        let gg_value = caldo.value.w36_data[tl][venue]['GGCONS'][0].numeric_value
        if (!(gg_value==null)){
          validity.capoluoghi.values[tl][venue]['GGCONS'][0] = true
        }else{
          validity.capoluoghi.values[tl][venue]['GGCONS'][0] = false
          validity.capoluoghi.tab = false
          validity.global = false
        }
        for (const [key3, config] of Object.entries(configCaldo.variabili)) {
          if (!(config.parametro in validity.capoluoghi.values[tl][venue])) 
            validity.capoluoghi.values[tl][venue][config.parametro] = {}
          let value = caldo.value.w36_data[tl][venue][config.parametro][config.aggregazione].numeric_value
          if (!(value==null)){
            validity.capoluoghi.values[tl][venue][config.parametro][config.aggregazione] = true
            if (config.parametro.toLowerCase() + "_min" in soglie && config.parametro.toLowerCase() + "_max"){
              let min = soglie[config.parametro.toLowerCase() + "_min"]
              let max = soglie[config.parametro.toLowerCase() + "_max"]
              if (value>=min && value<=max){
                validity.capoluoghi.values[tl][venue][config.parametro][config.aggregazione] = true
              }else{
                validity.capoluoghi.values[tl][venue][config.parametro][config.aggregazione] = false
                validity.capoluoghi.tab = false
                validity.global = false
              }
            }
          }else{
            validity.capoluoghi.values[tl][venue][config.parametro][config.aggregazione] = false
            validity.capoluoghi.tab = false
            validity.global = false
          }
        }
      }  
    }
    if (gg_cons_modificabili.value){
      if (caldo.value.internal_note.length == 0){
        validity.capoluoghi.internal_note = false
        validity.capoluoghi.tab = false
        validity.global = false        
      }else{
        validity.capoluoghi.internal_note = true
      }
    }
    // tab torino
    for (const [tl_idx, tl_value] of Object.entries(myDateTorino.value)) {
      let tl = tl_value[0]
      if (!(tl in validity.torino.values)) validity.torino.values[tl] = {}
      let venue = 59
      if (!(venue in validity.torino.values[tl])) validity.torino.values[tl][venue] = {}
      for (const [key3, config] of Object.entries(configCaldo.temperature_torino)) {
        if (!(config.parametro in validity.torino.values[tl][venue])) 
          validity.torino.values[tl][venue][config.parametro] = {}
        let value = caldo.value.w36_data[tl][venue][config.parametro][config.aggregazione].numeric_value
        if (!(value==null)){
          validity.torino.values[tl][venue][config.parametro][config.aggregazione] = true
          if (config.parametro.toLowerCase() + "_min" in soglie && config.parametro.toLowerCase() + "_max"){
            let min = soglie[config.parametro.toLowerCase() + "_min"]
            let max = soglie[config.parametro.toLowerCase() + "_max"]
            if (value>=min && value<=max){
              validity.torino.values[tl][venue][config.parametro][config.aggregazione] = true
            }else{
              validity.torino.values[tl][venue][config.parametro][config.aggregazione] = false
              validity.torino.tab = false
              validity.global = false
            }
          }
        }else{
          validity.torino.values[tl][venue][config.parametro][config.aggregazione] = false
          validity.torino.tab = false
          validity.global = false
        }
      }
    }
    for (const [tl, tl_value] of Object.entries(myDate.value)) {
      if (!(tl in validity.torino.values)) validity.torino.values[tl] = {}
      let venue = 59
      if (!(venue in validity.torino.values[tl])) validity.torino.values[tl][venue] = {}
      for (const [key3, config] of Object.entries(configCaldo.temperature_torino)) {
        if (!(config.parametro in validity.torino.values[tl][venue])) 
          validity.torino.values[tl][venue][config.parametro] = {}
        let value = caldo.value.w36_data[tl][venue][config.parametro][config.aggregazione].numeric_value
        if (!(value==null)){
          validity.torino.values[tl][venue][config.parametro][config.aggregazione] = true
          if (config.parametro.toLowerCase() + "_min" in soglie && config.parametro.toLowerCase() + "_max"){
            let min = soglie[config.parametro.toLowerCase() + "_min"]
            let max = soglie[config.parametro.toLowerCase() + "_max"]
            if (value>=min && value<=max){
              validity.torino.values[tl][venue][config.parametro][config.aggregazione] = true
            }else{
              validity.torino.values[tl][venue][config.parametro][config.aggregazione] = false
              validity.torino.tab = false
              validity.global = false
            }
          }
        }else{
          validity.torino.values[tl][venue][config.parametro][config.aggregazione] = false
          validity.torino.tab = false
          validity.global = false
        }
      }
    }
    // tab parametri
    let tl_array = []
    for (const [tl, tl_value] of Object.entries(myDate.value)) {
      tl_array.push(tl)
    }
    tl_array.push(32)
    tl_array.forEach(tl => {
      if (!(tl in validity.parametri.values)) validity.parametri.values[tl] = {}
      for (const [venue, venue_value] of Object.entries(myVenues)) {
        if (!(venue in validity.parametri.values[tl])) validity.parametri.values[tl][venue] = {}
        let parametri = ['ATMIN', 'GGCONS', 'ATMAX']
        parametri.forEach(parametro => {
          if ((parametro == 'GGCONS' && tl == 32) || parametro!='GGCONS'){
            if (!(parametro in validity.parametri.values[tl][venue])) 
              validity.parametri.values[tl][venue][parametro] = {}
            let value = caldo.value.w36_data[tl][venue][parametro][0].numeric_value
            if (!(value==null)){
              validity.parametri.values[tl][venue][parametro][0] = true
              if (parametro.toLowerCase() + "_min" in soglie && parametro.toLowerCase() + "_max"){
                let min = soglie[parametro.toLowerCase() + "_min"]
                let max = soglie[parametro.toLowerCase() + "_max"]
                if (value>=min && value<=max){
                  validity.parametri.values[tl][venue][parametro][0] = true
                }else{
                  validity.parametri.values[tl][venue][parametro][0] = false
                  validity.parametri.tab = false
                  validity.global = false
                }
              }
            }else{
              validity.parametri.values[tl][venue][parametro][0] = false
              validity.parametri.tab = false
              validity.global = false
            }
          }
        })
      }
    })
    for (const [tl, tl_value] of Object.entries(myDate.value)) {
      if (!(tl in validity.parametri.values)) validity.parametri.values[tl] = {}
      for (const [venue, venue_value] of Object.entries(myVenues)) {
        if (!(venue in validity.parametri.values[tl])) validity.parametri.values[tl][venue] = {}
        myParam.forEach(parametro => {
          if (!(parametro in validity.parametri.values[tl][venue])) 
            validity.parametri.values[tl][venue][parametro] = {}
          let aggregazioni = [327, 328]
          aggregazioni.forEach(aggregazione => {
            let value = caldo.value.w36_data[tl][venue][parametro][aggregazione].numeric_value
            if (!(value==null)){
              validity.parametri.values[tl][venue][parametro][aggregazione] = true
              if (parametro.toLowerCase() + "_min" in soglie && parametro.toLowerCase() + "_max"){
                let min = soglie[parametro.toLowerCase() + "_min"]
                let max = soglie[parametro.toLowerCase() + "_max"]
                if (value>=min && value<=max){
                  validity.parametri.values[tl][venue][parametro][aggregazione] = true
                }else{
                  validity.parametri.values[tl][venue][parametro][aggregazione] = false
                  validity.parametri.tab = false
                  validity.global = false
                }
              }
            }else{
              validity.parametri.values[tl][venue][parametro][aggregazione] = false
              validity.parametri.tab = false
              validity.global = false
            }
          })
        })
      }  
    }
    // tab epidemiologia
    for (const [tl, tl_value] of Object.entries(myDate.value)) {
      if (!(tl in validity.epidemiologia.values)) validity.epidemiologia.values[tl] = {}
      let venue = 59
      if (!(venue in validity.epidemiologia.values[tl])) validity.epidemiologia.values[tl][venue] = {}
      let parametro = 'COD_SALUTE'
      if (!(parametro in validity.epidemiologia.values[tl][venue])) 
        validity.epidemiologia.values[tl][venue][parametro] = {}
      let value = caldo.value.w36_data[tl][venue][parametro][0].numeric_value
      if (!(value==null)){
        validity.epidemiologia.values[tl][venue][parametro][0] = true
        if (value>=0 && value<=3){
          validity.epidemiologia.values[tl][venue][parametro][0] = true
        }else{
          validity.epidemiologia.values[tl][venue][parametro][0] = false
          validity.epidemiologia.tab = false
          validity.global = false
        }
      }else{
        validity.epidemiologia.values[tl][venue][parametro][0] = false
        validity.epidemiologia.tab = false
        validity.global = false
      }
    }
  }
  // console.log(validity)
  return validity
})


watch(() => countdown.value, (new_value) => {
  if(new_value > 3){
    ready.value = true
  }
})

function getDateFormatted(rawString, time = true) {
  return api.getDateFormatted(rawString, time)
}

function ricavatl(id, tl) {
  let tlnew = 0
  if (id == "D0") {
    tlnew = tl
  } else if (id == "D1"){
    tlnew = tl_ieri[tl]
  } else if (id == "D2"){
    tlnew = tl_altroieri[tl]
  }
  return tlnew
}
 
function valoreStima(parametro, valore) {
  // definisco un oggetto che mappa il nome dell'etichetta con il prefisso del nome del campo della tabella 
  // w36_parametri_equazione.
  // la tabella è contenuta nell'oggetto parametri, così prefisso + giorno + valore ricavo  
  // il nome completo del campo e la relativa stima
  let stima = 0
  let classe = ""
  const mapp = {
    "WDA75p": "wda_75p",
    "WDA90p": "wda_90p",
    "WDA95p": "wda_95p",
    "GG cons oggi": "cons_class_0_",
    "GG cons ieri": "cons_class_1_",
    "GG cons altroieri": "cons_class_2_",
    "ATmin oggi": "atmin_class_0_",
    "ATmin ieri": "atmin_class_1_",
    "ATmin altroieri": "atmin_class_2_",
    "popday2 - decr.estivo": "popday_",
    "dow - day of week": "dow"
  }

  // CDL occhio a come gestire -1.... non è nel nome del campo del db

  if (parametro == 'WDA75p' || parametro == 'WDA90p'|| parametro == 'WDA95p') {
    if ( valore == 1) { 
      classe = mapp[parametro] }
    else {
      classe = ""
    }
  } else { 
    if (valore == -1) {
      classe = mapp[parametro] + '0'
    } else {
      classe = mapp[parametro] + valore
    }
  }
  if (classe != "") {
    stima = parametri.value[classe][classe].stima
  } else {
    stima = 0
  }
  //console.log("stima", stima, parametro, valore)
  return stima
}

function valoreClasse(parametro, tl) {
  const mapp = new Map();
  let wda75p = wda.value[59][tl][940].numeric_value 
  let wda90p = wda.value[59][tl][941].numeric_value 
  let wda95p = wda.value[59][tl][942].numeric_value 
  let atmin_48 = caldo.value.w36_data[tl][59]['ATMIN'][0].numeric_value 
  let atmin_32 = caldo.value.w36_data[tl_ieri[tl]][59]['ATMIN'][0].numeric_value 
  let atmin_15 = caldo.value.w36_data[tl_altroieri[tl]][59]['ATMIN'][0].numeric_value 
  let ggcons_48 = caldo.value.w36_data[tl][59]['GGCONS'][0].numeric_value
  let ggcons_32 = caldo.value.w36_data[tl_ieri[tl]][59]['GGCONS'][0].numeric_value
  let ggcons_15 = caldo.value.w36_data[tl_altroieri[tl]][59]['GGCONS'][0].numeric_value 
  mapp.set('ATmin oggi', atmin_48);
  mapp.set('ATmin ieri', atmin_32);
  mapp.set('ATmin altroieri', atmin_15);
  mapp.set('GG cons oggi', ggcons_48);
  mapp.set('GG cons ieri', ggcons_32);
  mapp.set('GG cons altroieri', ggcons_15);



  if (parametro == 'WDA75p') { 
    if ( wda75p ==1 && wda90p ==0 ) {
      return 1
    } else {
      return 0
    }
  } else if (parametro == 'WDA90p') { 
    if ( wda90p ==0 && wda95p ==0 ) {
      return 0
    } else if (wda90p ==0 && wda95p ==1){
      // è impossibile
      return 0
    } else if (wda90p ==1 && wda95p ==1){
      if (ggcons_48 >=3){
        return 0 // perchè return 1 wda95p
      }else{
        return 1 // prendo il wda90p e non il wda95
      }
    } else if (wda90p ==1 && wda95p ==0){
      return 1
    } 
  } else if (parametro == 'WDA95p') { 
    if ( wda90p ==0 && wda95p ==0 ) {
      return 0
    } else if (wda90p ==0 && wda95p ==1){
      // è impossibile
      return 0
    } else if (wda90p ==1 && wda95p ==1){
      if (ggcons_48 >=3){
        return 1
      }else{
        return 0
      }
    } else if (wda90p ==1 && wda95p ==0){
      return 0
    }
  } else if (parametro == 'ATmin oggi' || parametro == 'ATmin ieri' || parametro == 'ATmin altroieri' ) {
    let atmin = mapp.get(parametro)
    if (atmin >=0 && atmin < 12) {
      return -1
    } else if (atmin >=12 && atmin < 18) {
      return 9
    } else if (atmin >=18 && atmin < 21) {
      return 1
    } else if (atmin >=21 && atmin < 24) {
      return 2
    } else {
      return 3
    }
  } else if (parametro == 'GG cons oggi' || parametro == 'GG cons ieri' || parametro == 'GG cons altroieri' ) {
    let myggcons = mapp.get(parametro)
    if (myggcons >=1 && myggcons <= 3) {
      return 1
    } else if (myggcons >=4 && myggcons <= 7) {
      return 2
    } else if (myggcons >=8 ) {
      return 3
    } else {
      return 9
    }
  } 
   //if caldo.value.w36_data[tl][id_venue]['IGRO'][aggreg].numeric_value }
}

function calcolaEsponente (tl) {
  let k = 0
  k = -0.073623 +
  valoreStima("WDA75p", valoreClasse("WDA75p", tl)) +
  valoreStima("WDA90p", valoreClasse("WDA90p", tl)) +
  valoreStima("WDA95p", valoreClasse("WDA95p", tl)) +
  valoreStima("GG cons oggi", valoreClasse("GG cons oggi", tl)) +
  valoreStima("GG cons ieri", valoreClasse("GG cons ieri", tl)) +
  valoreStima("GG cons altroieri", valoreClasse("GG cons altroieri", tl)) +
  valoreStima("ATmin oggi", valoreClasse("ATmin oggi", tl)) +
  valoreStima("ATmin ieri", valoreClasse("ATmin ieri", tl)) +
  valoreStima("ATmin altroieri", valoreClasse("ATmin altroieri", tl)) +
  valoreStima('popday2 - decr.estivo', popday2.value[tl].numeric_value) +
  valoreStima('dow - day of week', dayofweek.value[tl].numeric_value)
  
  return k
}
function calcolaPrevisti(tl) {
  let previsti = Math.round(caldo.value.w36_data[tl][59]['ATTESI'][0].numeric_value * Math.exp(calcolaEsponente(tl)) * 100)/100
  return previsti
}

function calcolaEccessi(tl) {
  let eccessi = Math.round((calcolaPrevisti(tl) - caldo.value.w36_data[tl][59]['ATTESI'][0].numeric_value) * 100)/100
  return eccessi
}

async function calcolaCodiceSalute(eccessi, tl){
  console.log("calcolaCodiceSalute", eccessi, tl)
  let codice_salute = 0
  let ggcons_48 = caldo.value.w36_data[tl][59]['GGCONS'][0].numeric_value
  let ggcons_32 = caldo.value.w36_data[tl_ieri[tl]][59]['GGCONS'][0].numeric_value
  let ggcons_15 = caldo.value.w36_data[tl_altroieri[tl]][59]['GGCONS'][0].numeric_value
  //let eccessi = Math.round(eccessi_float)
  
  // il codice salute esce sono se l'altroieri o ieri o oggi era un giorno caldo
  if (ggcons_15 >=1 ||  ggcons_32>=1 || ggcons_48 >=1) {
    if (eccessi <= 2){
      codice_salute = 0 }
    else if (eccessi > 2 && eccessi <= 5){
      codice_salute = 1 }
    else if (eccessi > 5 && eccessi <= 10){
      codice_salute = 2 }
    else if (eccessi > 10){
      codice_salute = 3
    }
  }

  if (caldo.value.status === '0'){
    let id_w36_data = caldo.value.w36_data[tl][59]['COD_SALUTE'][0].id_w36_data
    await saveW36Data(id_w36_data, 'COD_SALUTE', 59, tl, 0, codice_salute, false, false)
  }
  return codice_salute
}

function evidenziaPercentili(tl,id_venue,param){
  let id0=tl+'_'+id_venue+'_'+param+'_940'
  let id1=tl+'_'+id_venue+'_'+param+'_941'
  let id2=tl+'_'+id_venue+'_'+param+'_942'
  if (param =='ATMAX'){
    document.getElementById(id0).style.backgroundColor="#ffcccc"
    document.getElementById(id1).style.backgroundColor="#ffcccc"
    document.getElementById(id2).style.backgroundColor="#ffcccc"
  } else if (param == 'ATMIN') {
    document.getElementById(id0).style.backgroundColor="#99ebff"
    document.getElementById(id1).style.backgroundColor="#99ebff"
    document.getElementById(id2).style.backgroundColor="#99ebff"
  }
}

function rilasciaPercentili(tl,id_venue,param){
  let id0=tl+'_'+id_venue+'_'+param+'_940'
  let id1=tl+'_'+id_venue+'_'+param+'_941'
  let id2=tl+'_'+id_venue+'_'+param+'_942'
  if (param =='ATMAX'){
    document.getElementById(id0).style.backgroundColor="#F0F0F0"
    document.getElementById(id1).style.backgroundColor="#F0F0F0"
    document.getElementById(id2).style.backgroundColor="#F0F0F0"
  } else if (param == 'ATMIN') {
    document.getElementById(id0).style.backgroundColor="#F0F0F0"
    document.getElementById(id1).style.backgroundColor="#F0F0F0"
    document.getElementById(id2).style.backgroundColor="#F0F0F0"
  } else {
    // i percentili si evidenziano solo per focus su ATMAX o ATMIN
  }
}

function ossField(tl){
  // funzione che, per la tabella di Torino, colora diversamente le celle per i campi osservati e 
  // per distinguerli da quelli previsti.
  if ([301, 300, 15, 32].includes(tl)){
    return blue
  } else {
    return red
  }
}

function calcolaAT(tl, id_venue, param, aggreg){
  // le ATmax e ATmin del panel parametri sono calcolate a partire dai parametri
  // primari T, RH e V. Una volta calcolate devono essere salvate e visibili anche
  // sul panel capoluoghi
  console.log("calcolaAT",tl, id_venue, param, aggreg)

  let igro = caldo.value.w36_data[tl][id_venue]['IGRO'][aggreg].numeric_value
  let velv = caldo.value.w36_data[tl][id_venue]['VELV'][aggreg].numeric_value
  let terma = caldo.value.w36_data[tl][id_venue]['TERMA'][aggreg].numeric_value
  
  //Calcolo della temperatura apparente
  // e=6.112*10^(7.5*T/(237.7+T))*RH/100  tensione di vapore saturo
  // AT=-2.7+1.04*T+2*e/10-0.65V

  let e = 6.112 * 10 **((7.5 * terma) / (237.7 + terma)) * igro / 100
  let at = -2.7 + 1.04 * terma + 2 * e / 10 - 0.65 * velv
  let temp_apparente = Math.round(at * 10) / 10
  return temp_apparente
}


async function calcolaSalvaAT(tl, id_venue, param, aggreg){
  // le ATmax e ATmin del panel parametri sono calcolate a partire dai parametri
  // primari T, RH e V. Una volta calcolate devono essere salvate e visibili anche
  // sul panel capoluoghi

  // se la chiamata arriva da un campo AT, non faccio nulla
  if (['IGRO', 'VELV', 'TERMA'].includes(param)){
    let tempApparente = calcolaAT(tl, id_venue, param, aggreg)
    let param_ta= ''
    if(aggreg == 327){
      param_ta='ATMIN'
    } else {
      param_ta='ATMAX'
    }
    let id_w36_data = caldo.value.w36_data[tl][id_venue][param_ta][0].id_w36_data
    await saveW36Data(id_w36_data, param_ta, id_venue, tl, 0, tempApparente, false, false)
    // tab Torino propone dati vecchi
    console.log("calcolaSalvaAT", tl, id_venue, param, aggreg)
    if (id_venue == 59 && (tl == 48 || tl == 66 || tl == 83)) calcolaCodiceSalute(calcolaEccessi(tl), tl)
  }
}

async function salvaGiorniConsecutivi(tl, id_venue, param, valore){
  // 
  let id_w36_data = caldo.value.w36_data[tl][id_venue][param][0].id_w36_data
  await saveW36Data(id_w36_data, param, id_venue, tl, 0, valore, false, false)
}


function idTL2Date(tl){
  let today = dateToString(new Date(caldo.value.data_emissione))
  let tomorrow = dateToString(new Date(new Date(caldo.value.data_emissione).setDate(new Date(caldo.value.data_emissione).getDate()+1)))
  let afterTomorrow = dateToString(new Date(new Date(caldo.value.data_emissione).setDate(new Date(caldo.value.data_emissione).getDate()+2)))
  let yesterday = dateToString(new Date(new Date(caldo.value.data_emissione).setDate(new Date(caldo.value.data_emissione).getDate()-1)))
  let twodaysago = dateToString(new Date(new Date(caldo.value.data_emissione).setDate(new Date(caldo.value.data_emissione).getDate()-2)))
  let date = today
  if (tl == 66){
    date = tomorrow
  }
  if (tl == 83){
    date = afterTomorrow
  }
  if (tl == 15){
    date = twodaysago
  }
  if (tl == 32){
    date = yesterday
  }
  return date
}


function createDate(){
  let today = dateToString(new Date(caldo.value.data_emissione))
  let tomorrow = dateToString(new Date(new Date(caldo.value.data_emissione).setDate(new Date(caldo.value.data_emissione).getDate()+1)))
  let afterTomorrow = dateToString(new Date(new Date(caldo.value.data_emissione).setDate(new Date(caldo.value.data_emissione).getDate()+2)))
  let yesterday = dateToString(new Date(new Date(caldo.value.data_emissione).setDate(new Date(caldo.value.data_emissione).getDate()-1)))
  let twodaysago = dateToString(new Date(new Date(caldo.value.data_emissione).setDate(new Date(caldo.value.data_emissione).getDate()-2)))
  let threedaysago = dateToString(new Date(new Date(caldo.value.data_emissione).setDate(new Date(caldo.value.data_emissione).getDate()-3)))
  let fourdaysago = dateToString(new Date(new Date(caldo.value.data_emissione).setDate(new Date(caldo.value.data_emissione).getDate()-4)))

  myDate.value = {
    48: `${today}`,
    66: `${tomorrow}`,
    83: `${afterTomorrow}`
  }

  myDateTorino.value = {
  0: [301,`${fourdaysago}`],
  1: [300,`${threedaysago}`],
  2: [15,`${twodaysago}`],
  3: [32,`${yesterday}`]
  }

  myDateEpidem.value = {
    15: `${twodaysago}`,
    32: `${yesterday}`,
    48: `${today}`
  }
}

function calcolaWda(atmax_prevista, atmax_percentile, atmin_prevista, atmin_percentile, notify, id_venue, tl, aggreg){
  // algoritmo di calcolo del wda
  let wda_value = 0
  // iserisco la condizione che la atmax superari almeno i 27°C per far accendere wda,
  // altrimenti con percentili bassi a inizio maggio uscirebbe sempre un livello di disagio valorizzato
  if (atmax_prevista >= 27) {
    if (atmax_prevista >= atmax_percentile) {
      console.log("\t\tcalcolaWda - atmax_prevista >= atmax_percentile",atmax_prevista, atmax_percentile, atmin_prevista, atmin_percentile)
      if (notify){
        toast.open(
          {
            message: 'calcolaWda - ' + idVenue2Name[id_venue] + ', ' + idTL2Date(tl) + ', ' + idAggreg2Name[aggreg] + ', atmax_prevista >= atmax_percentile',
            type: 'info',
            position: 'top-left',
            duration: 6000
          }
        )
      }
      wda_value = 1
    } else if ((atmax_percentile - atmax_prevista) <= 0.5){
      if (atmin_prevista >= (atmin_percentile-0.5)){
        console.log("\t\tcalcolaWda - atmin_prevista >= (atmin_percentile-0.5)",atmax_prevista, atmax_percentile, atmin_prevista, atmin_percentile)
        if (notify){
          toast.open(
            {
              message: 'calcolaWda - ' + idVenue2Name[id_venue] + ', ' + idTL2Date(tl) + ', ' + idAggreg2Name[aggreg] + ', atmin_prevista >= (atmin_percentile-0.5)',
              type: 'info',
              position: 'top-left',
              duration: 6000
            }
          )
        }
        wda_value = 1
      } else {
        console.log("\t\tcalcolaWda - (atmax_percentile - atmax_prevista) <= 0.5",atmax_prevista, atmax_percentile, atmin_prevista, atmin_percentile)
        wda_value = 0
      }
    } else {
      console.log("\t\tcalcolaWda - atmax_prevista >= 27")
      wda_value = 0
    }
  }
  console.log("\t\tcalcolaWda - calcolaWda return",wda_value)
  return wda_value
}

async function setMeasure(id_w36_data, campo, tl, aggreg, id_venue, locked){
  let inizio = new Date().getMilliseconds()
  // questa funzione ricava il nuovo valore da salvare
  let stack : Array<Object> = []
  let mystack : Array<Object> = []
  if(window.event && window.event.target !== null){
    let new_value = parseFloat((window.event.target as HTMLInputElement).value)
    if (campo=='COD_COLORE'){
      toast.open(
        {
          message: 'ATTENZIONE: se forzi il codice colore verifica che siano corretti i giorni consecutivi e inserisci nota interna!',
          type: 'warning',
          position: 'top-left',
          duration: 6000
        }
      )
      gg_cons_modificabili.value = true
      let ggcons_32 = caldo.value.w36_data[32][id_venue]['GGCONS'][0]
      let ggcons_48 = caldo.value.w36_data[48][id_venue]['GGCONS'][0]
      let ggcons_66 = caldo.value.w36_data[66][id_venue]['GGCONS'][0]
      let ggcons_83 = caldo.value.w36_data[83][id_venue]['GGCONS'][0]
      let cod_colore_66 = caldo.value.w36_data[66][id_venue]['COD_COLORE'][0]
      let cod_colore_83 = caldo.value.w36_data[83][id_venue]['COD_COLORE'][0]
      if (tl == 48){
        // modifica anche 66 e 83
        if (new_value == 0){
          // decrementa
          ggcons_48.numeric_value = 0
          if (cod_colore_66.numeric_value > 0){
            ggcons_66.numeric_value = 1
          }else{
            ggcons_66.numeric_value = 0
          }
          if (cod_colore_83.numeric_value > 0){
            ggcons_83.numeric_value = ggcons_66.numeric_value + 1
          }else{
            ggcons_83.numeric_value = 0
          }
        }else{
          // incrementa
          ggcons_48.numeric_value = ggcons_32.numeric_value + 1
          if (cod_colore_66.numeric_value > 0){
            ggcons_66.numeric_value = ggcons_48.numeric_value + 1
          }else{
            ggcons_66.numeric_value = 0
          }
          if (cod_colore_83.numeric_value > 0){
            ggcons_83.numeric_value = ggcons_66.numeric_value + 1
          }else{
            ggcons_83.numeric_value = 0
          }
        }
        mystack = await saveW36Data(ggcons_48.id_w36_data, "GGCONS", id_venue, "48", 0, ggcons_48.numeric_value, false, true ,false)
        mystack.forEach(element => {
          stack.push(element)
        })
        mystack = await saveW36Data(ggcons_66.id_w36_data, "GGCONS", id_venue, "66", 0, ggcons_66.numeric_value, false, true ,false)
        mystack.forEach(element => {
          stack.push(element)
        })
        mystack = await saveW36Data(ggcons_83.id_w36_data, "GGCONS", id_venue, "83", 0, ggcons_83.numeric_value, false, true ,false)
        mystack.forEach(element => {
          stack.push(element)
        })
      }else if (tl == 66){
        // modifica anche 83
        if (new_value == 0){
          // decrementa
          ggcons_66.numeric_value = 0
          if (cod_colore_83.numeric_value > 0){
            ggcons_83.numeric_value = 1
          }else{
            ggcons_83.numeric_value = 0
          }
        }else{
          // incrementa
          ggcons_66.numeric_value = ggcons_48.numeric_value + 1 
          if (cod_colore_83.numeric_value > 0){
            ggcons_83.numeric_value = ggcons_66.numeric_value + 1
          }else{
            ggcons_83.numeric_value = 0
          }
        }
        mystack = await saveW36Data(ggcons_66.id_w36_data, "GGCONS", id_venue, "66", 0, ggcons_66.numeric_value, false, true ,false)
        mystack.forEach(element => {
          stack.push(element)
        })
        mystack = await saveW36Data(ggcons_83.id_w36_data, "GGCONS", id_venue, "83", 0, ggcons_83.numeric_value, false, true ,false)
        mystack.forEach(element => {
          stack.push(element)
        })
      }else if (tl == 83){
  
        // modifica solo l'83
        if (new_value == 0){
          // decrementa
          ggcons_83.numeric_value = 0
        }else{
          // incrementa
          ggcons_83.numeric_value = ggcons_66.numeric_value + 1
        }
        mystack = await saveW36Data(ggcons_83.id_w36_data, "GGCONS", id_venue, "83", 0, ggcons_83.numeric_value, false, true ,false)
        mystack.forEach(element => {
          stack.push(element)
        })
      }
    }
    if (campo=='GGCONS' && new_value <0) new_value = 0
    // salvataggio ggcons id_time_layout 15
    // 66634 'GGCONS' 1 32 0 2
    if (campo=='GGCONS' && tl=="32" && aggreg=="0"){
      // CERCA l'id del GGCONS tl 15
      let w36_data_found_id = caldo.value.w36_data[15][id_venue]['GGCONS'][0].id_w36_data
      let myggcons = new_value - 1
      if (myggcons<0) myggcons=0
      console.log("setMeasure - salvo GGCONS 15", id_venue, myggcons)
      mystack = await saveW36Data(w36_data_found_id, campo, id_venue, "15", aggreg, myggcons, false, locked ,false)
      mystack.forEach(element => {
        stack.push(element)
      })
    }
    mystack = await saveW36Data(id_w36_data, campo, id_venue, tl, aggreg, new_value, true, locked ,false)
    mystack.forEach(element => {
      stack.push(element)
    })
    if (caldo.value.status === 'X' || caldo.value.status === '0'){
      if (id_venue == 59)
        await saveW36(stack, true, true)
      else
        await saveW36(stack, true)
    }
  }
  console.log("setMeasure fine millisecondi", (new Date().getMilliseconds()) - inizio)
}


async function saveW36Data(id_w36_data, campo, id_venue, tl,aggreg, new_value, notify_success, locked, save = true){
  // funzione che prepara lo "stack", ovvero l'array con le modifiche da mandare al bulk_update del backend
  let w36data = caldo.value.w36_data[tl][id_venue][campo][aggreg]
  let stack : Array<Object> = []
  let value = new_value
  let replot = false
  if(isNaN(new_value)){
    value = null
  }
  
  const payload = {"id_key":"id_w36_data","id":id_w36_data,"value_key":"numeric_value","new_value": value}
  const payload_locked = {"id_key":"id_w36_data","id":id_w36_data,"value_key":"locked","new_value": true}
  const payloadusername = {"id_key":"id_w36","id":caldo.value.id_w36,"value_key":"username","new_value": store.state.username}
  // x immediata visualizzazione sul frontend del nuovo valore

  w36data.numeric_value = value
  stack.push(payload)
  if (locked){
    // console.log("Aggiungo locked", payload_locked)
    stack.push(payload_locked)
    w36data.locked = locked
  }
  stack.push(payloadusername)
  
  if (w36data.id_parametro == 'ATMAX' || w36data.id_parametro == 'ATMIN' || w36data.id_parametro == 'TERMA') {
    replot = true
  }
  if (save) saveW36(stack, notify_success, replot)
  return stack
}

function saveField(field) {
  actions.value.saving = true
  let stack : Array<Object> = []

  if(window.event && window.event.target !== null){
    let new_value = (window.event.target as HTMLInputElement).value
    const payload = {"id_key":"id_w36","id":caldo.value.id_w36,"value_key":field,"new_value": new_value}
    const payloadusername = {"id_key":"id_w36","id":caldo.value.id_w36,"value_key":"username","new_value": store.state.username}
    
    if (field == "note") caldo.value.note = new_value

    if (field == "internal_note") caldo.value.internal_note = new_value
    
    stack.push(payload)
    stack.push(payloadusername)

    saveW36(stack)
    actions.value.saving = false
  }
}

async function saveW36(stack, notify_success = false, replot=false) {
  const username = stack.find((element) => element.value_key == 'username');
  if (username.new_value === owner.value){
    // console.log("saveW36 salvo", username.new_value, owner.value, stack)
    await bulkUpdateW36(stack).then((response) => {
      if (response === undefined || !response.ok) {
        toast.open(
          {
            message: 'Errore nel salvataggio',
            type: 'error',
            position: 'top-left'
          }
        )
      }else{
        return response.json()
      }
    }).then(data => {
      if (notify_success){
        toast.open(
          {
            message: 'Dato salvato',
            type: 'success',
            position: 'top-left'
          }
        )
      }
      caldo.value.last_update = data.bulletin.last_update
      caldo.value.username = store.state.username
    }).catch((error) => {
      toast.open(
        {
          message: `Errore di comunicazione: ${error}`,
          type: 'error',
          position: 'top-left'
        }
      )
    })
    if (replot) {
      await fetchChart(caldo_id.value).then(response => {
        if (!response.ok) {
          toast.open(
            {
              message: `Errore ${response.status} nel recupero del bollettino`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json() // Serve casting al tipo
      }).then(data => { 
        image_max.value = data['graphic_max']
        image_min.value = data['graphic_min']
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
  }else{
    console.log("username diverso non salvo!")
  }
}

async function bulkUpdateW36(payload) {
  // console.log("payload",payload)
  // richiamo il bulk_update lato backend
  if(store.state.access !== null){
    const response = await api.fetch_wrapper(
      store.state.access,
      `/api/w36/bulletins/bulk_update/`,
      {
        method: 'POST',
        body: JSON.stringify(payload)
      }
    )
    return response
  }else{
    toast.open(
      {
        message: `Errore: non sei loggato`,
        type: 'error',
        position: 'top-left'
      }
    )
  }
  
}

function dateToString(date): String{
  const yy = date.getFullYear()
  const mm = date.getMonth() + 1
  const dd = date.getDate()
  return [(dd>9 ? '' : '0') + dd,  (mm>9 ? '' : '0') + mm, yy].join('-')
}

async function execute(action, reroute, message) {
  actions.value[action + 'ing']= true
  if (action === 'bollmeteo_terma') {
    await fetchBollMeteoTemp(true)
    await updateAll()
  }else{
    fetchCaldoAction(action).then(response => {
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
      if (action === "send"){
        store.state.caldo_first = "true"
        store.save()
      }
      if (action === "reopen"){
        store.state.caldo_first = "false"
        store.save()
      }
      if (reroute) {
        router.push({ path: `/w36/${data.id_w36}`})
        caldo_id.value = data.id_w36
        // console.log("execute fetchData reroute")
        fetchData()
      } else {
        // console.log("execute fetchData")
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
}

function execute_timeout(action, reroute, message){
  // console.log("inizio execute_timeout")
  if (actions.value.saving){
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

async function fetchCaldoAction (action) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w36/bulletins/${caldo_id.value}/${action}/`
  )
  return response
}

async function fetchCaldo (id) {
  const response = await fetch('/api/w36/bulletins/' + id + '/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchParametri () {
  // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
  const response = await fetch('/api/w36/parametri/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchJson (endpoint, description) {
	try {
		const response = await fetch(endpoint, {
			headers: {
			accept: 'application/json'
			}
		})
		if (!response.ok) {
			toast.open(
			{
				message: `Errore ${response.status} nel recupero di ${description}`,
				type: 'error',
				position: 'top-left'
			}
			)
			return {}
		} else {
			return response.json()
		}
	} catch(error) {
		toast.open(
		{
			message: `Errore ${error}`,
			type: 'error',
			position: 'top-left'
		}
		)
		return {}
	}
}

async function fetchBollMeteoTemp(user_request = false){
  // console.log("fetchBollMeteoTemp")
	let stack : Array<Object> = []
	let w36_tl2w05_tl={
    "48_327": 51,
		"48_328": 50,
		"66_327": 68,
		"66_328": 67,
		"83_327": 85,
		"83_328": 84,
	}
	let meteo = await fetchJson(`/api/w05/current/${caldo.value.data_emissione}/`, "Bollettino meteo")
  if (meteo.id_w05){
    if (meteo.status == "0"){
      if (!confirm("Vuoi prendere le temperature dal bollettino meteo di oggi anche se in bozza?")) {
        return
      } 
    }
    if (meteo.status == "1"){
      if (user_request){
        if (!confirm("Vuoi prendere le temperature dal bollettino meteo definitivo di oggi?")) {
          return
        } 
      }else{
        toast.open(
          {
            message: "Prendo le temperature dal bollettino meteo odierno",
            type: 'success',
            position: 'top-left'
          }
        )
      }
    }
    let w05data_terma = meteo.w05data_set.filter(w05data => {
      return w05data.id_parametro === 'TERMA'
    })
    let w36data_terma = caldo.value.w36data_set.filter(w36data => {
      return w36data.id_parametro === 'TERMA'
    })
    for (const [key, value] of Object.entries(w36data_terma)) {
      let w05data = w05data_terma.filter(w05data => {
        return w05data.id_parametro === value.id_parametro &&
          w05data.id_aggregazione === value.id_aggregazione &&
          w05data.id_time_layouts === w36_tl2w05_tl[
            value.id_time_layouts + '_' + value.id_aggregazione] &&
          w05data.id_venue === value.id_venue
      })
      if (w05data[0]){
        value.numeric_value = parseFloat(w05data[0].numeric_value)
        caldo.value.w36_data[value.id_time_layouts][value.id_venue]['TERMA'][value.id_aggregazione].numeric_value = value.numeric_value
        let param = ''
        if(value.id_aggregazione == 327){
          param='ATMIN'
        } else {
          param='ATMAX'
        }
        const payload = {"id_key":"id_w36_data","id":value.id_w36_data,"value_key": "numeric_value","new_value": value.numeric_value}
        let temp_apparente = calcolaAT(value.id_time_layouts, value.id_venue, param, value.id_aggregazione)
        let id_w36_data = caldo.value.w36_data[value.id_time_layouts][value.id_venue][param][0].id_w36_data
        let w36_data = caldo.value.w36_data[value.id_time_layouts][value.id_venue][param][0]
        w36_data.numeric_value = temp_apparente
        const payloadAT = {"id_key":"id_w36_data","id":id_w36_data,"value_key": "numeric_value","new_value": temp_apparente}
        stack.push(payload)
        stack.push(payloadAT)
      }
    }
    const payloadusername = {"id_key":"id_w36","id":caldo.value.id_w36,"value_key":"username","new_value": store.state.username}
    stack.push(payloadusername)
    saveW36(stack, false, true)
  }else{
    toast.open(
		{
			message: `Non trovo nessun bollettino meteo con la data odierna!`,
			type: 'error',
			position: 'top-left'
		}
    )
  }
}

function setTab(tab){
  selectedTab.value = tab
}

function rearrange(data: any[], key: string, func: ArrayTransformer | null = null) {
//function rearrange(data: any[], key: string, func=null) {
  // rearranges the array data in a dictionary
  // aggregating all records with the same key as an array
  // optionally transforming each array with the func function
  let value_data = {}
  
  data.forEach((record: { [x: string]: string | number }) => {
    if (!(record[key] in value_data)) {
      value_data[record[key]] = []
    }
    value_data[record[key]].push(record)
  })
  if (func) {
    Object.keys(value_data).forEach(key => value_data[key] = func(value_data[key]))
  }
  if (!Object.values(value_data).some(item => item != undefined)) value_data = {}
  return value_data
}

async function fetchData () {
  let stack : Array<Object> = []
  countdown.value = 0
  ready.value = false
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  await fetchCaldo(caldo_id.value).then(response => {
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
    owner.value = data['username']
    if (data['username'] !== store.state.username) readonly.value = true
    let tmp = rearrange(
      data['w36data_set'],
      "id_time_layouts",
      pippo=>rearrange(pippo, "id_venue",
      pippo2=>rearrange(pippo2, "id_parametro",
      pippo3=>rearrange(pippo3, "id_aggregazione", (arr: any[]) => arr[0] )))
    )

    caldo.value = {
      id_w36: data.id_w36,
      data_emissione: data.data_emissione,
      status: data.status,
      note: data.note,
      internal_note: data.internal_note,
      osservati: data.osservati,
      debug: data.debug,
      last_update: data.last_update,
      username: data.username,
      w36_data: tmp,
			w36data_set: data['w36data_set']
    }
    if (store.state.username === owner.value)
      readonly.value = (caldo.value.status === '1' || caldo.value.status === '2' || !state.value.username)
    countdown.value += 1
  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
  // console.log("fetchParametri")
  // fetchParametri
  await fetchParametri().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero dei dati sui parametri dell'equazione di epidemiologia`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(data => {
    let tmp = rearrange(
      data,
      "parametro_epid",
      pippo=>rearrange(pippo, "parametro_epid", (arr: any[]) => arr[0])
    )
    parametri.value = tmp
    countdown.value += 1
  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
  // console.log("fetchChart")
  await fetchChart(caldo_id.value).then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero del bollettino`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json() // Serve casting al tipo
  }).then(data => {
    image_max.value = data['graphic_max']
    image_min.value = data['graphic_min']
    countdown.value += 1
  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
  if (caldo.value.status === "X"){
    await fetchBollMeteoTemp()
    // console.log("lo status è a X lo metto a zero!")
    const payloadstatus = {"id_key":"id_w36","id":caldo.value.id_w36,"value_key":"status","new_value": "0"}
    stack.push(payloadstatus)
    const payloadusername = {"id_key":"id_w36","id":caldo.value.id_w36,"value_key":"username","new_value": store.state.username}
    stack.push(payloadusername)
    await saveW36(stack)
    caldo.value.status = '0'
  }
  createDate()
  await updateAll()
  // console.log("caldo.value.status", caldo.value.status, caldo.value.status === '0')
  if ( (caldo.value.status === '0' || caldo.value.status === 'X') && store.state.username === owner.value){
    await calcolaCodiceSalute(calcolaEccessi(48), 48)
    await calcolaCodiceSalute(calcolaEccessi(66), 66)
    await calcolaCodiceSalute(calcolaEccessi(83), 83)
    caldo.value.w36data_set.forEach(element => {
      if (element.locked) gg_cons_modificabili.value = true
    });
  }
  countdown.value += 1
}

async function fetchChart (id) {
  const response = await fetch('/api/w36/chart/' + id, {
    headers: {
      accept: 'text/html"'
    }
  })
  return response
}

function remove() {
  if (
    confirm('Vuoi davvero cancellare questo bollettino?')
  ) {
    api.fetchBulletinDelete(caldo_id.value, 'w36/bulletins', store).then(response => {
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
function goto(id) {
  const element = document.getElementById(id)
  element.scrollIntoView({ behavior: "smooth" })
}

function setOwner(){
  if (!confirm("Vuoi diventare il proprietario di questo bollettino?")) {
    return
  } 
  owner.value = store.state.username
  readonly.value = false
}

function downloadCsv() {
  let element = document.createElement('a');
	element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(caldo.value.osservati));
	element.setAttribute('download', "caldo_osservati_" + caldo.value.data_emissione + ".csv");

	element.style.display = 'none';
	document.body.appendChild(element);

	element.click();
	document.body.removeChild(element);   
}

window.onscroll = function(){
  if (ready.value){
    const element = document.getElementById("idBI")
    if (element){
      var top  = window.pageYOffset || element.scrollTop
      if (top > 400){
        isTop.value = true
      }else{
        isTop.value = false
      }
    }
  }
}
</script>

<style>

table {
  table-layout: auto;
  width: 400px;
}

th {
  white-space: normal;
}

.nevetd {
  width: 60%;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="Number"] {
  appearance: textfield;
}
.map {
  display: none;
}

.map-top {
  display: none;
}

.map-right {
  display: none;
}

@media screen and (max-width: 2400px) {
  .map-top {
    display: block;
  }
  .map {
    display: block;
  }
}

@media screen and (min-width: 2400px) {
  .map-right {
    display: block;
  }
}

.yellow {
  background-color: yellow;
  color: black;
}

.orange {
  background-color: orange;
  color: black;
}

.red {
  background-color: red;
  color: white;
}
</style>