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
        <a
          class="btn btn-outline-primary"
          :href="'/api/w17/pdf/' + analisi.id_w17"
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
          v-if="analisi.status === '0' && state.username"
          :disabled="actions.sending || sendValidity"
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
          v-if="analisi.status === '1' && state.username && analisi.data_emissione.substring(0, 10) === today"
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
          v-if="analisi.status === '0' && state.username"
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
      <h1>Bollettino Analisi {{ analisi.numero_bollettino }}</h1>
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="analisi.status === '1'">
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
            :value="getDateFormatted(analisi.data_emissione, false)"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_validita">Data analisi
          <input
            id="data_validita"
            disabled
            class="form-control"
            name="data_validita"
            type="text"
            :value="getDateFormatted(analisi.data_analysis, false)"
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
            :value="getDateFormatted(analisi.last_update)"
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
            :value="analisi.username"
          >
        </label>
      </div>
    </div>

    <div 
      v-if="ready"
      class="row mt-3"
    >
      <div class="col-xl-12 col-md-12 mb-3">
        <ul
          class="nav nav-tabs nav-justified sticky-top bg-light"
          style="top: 46px;"
          role="tablist"
        >
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pill-situazione-tab"
              class="nav-link"
              :class="{active: selectedTab == 'Situazione generale' }"
              :style="tabValidity['situazione_generale'] ? 'border: #FF0000; border:1px solid #FF0000;' : ''"
              data-bs-toggle="pill"
              data-bs-target="#pill-situazione"
              type="button"
              role="tab"
              aria-controls="pill-situazione"
              aria-selected="true"
              @click="setTab('Situazione generale')"
            >
              Situazione generale
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pill-precipitazione-tab"
              class="nav-link"
              :class="{active: selectedTab == 'Precipitazioni' }"
              :style="tabValidity['precipitazioni'] ? 'border: #FF0000; border:1px solid #FF0000;' : ''"
              data-bs-toggle="pill"
              data-bs-target="#pill-precipitazione"
              type="button"
              role="tab"
              aria-controls="pill-precipitazione"
              aria-selected="false"
              @click="setTab('Precipitazioni')"
            >
              Precipitazioni
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pill-temperature-tab"
              class="nav-link"
              :class="{active: selectedTab == 'Temperature e Zero Termico' }"
              :style="tabValidity['temperature'] ? 'border: #FF0000; border:1px solid #FF0000;' : ''"
              data-bs-toggle="pill"
              data-bs-target="#pill-temperature"
              type="button"
              role="tab"
              aria-controls="pill-temperature"
              aria-selected="false"
              @click="setTab('Temperature e Zero Termico')"
            >
              Temperature e Zero Termico
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pill-vento-tab"
              class="nav-link" 
              :class="{active: selectedTab == 'Vento' }"
              :style="tabValidity['vento'] ? 'border: #FF0000; border:1px solid #FF0000;' : ''"
              data-bs-toggle="pill"
              data-bs-target="#pill-vento"
              type="button"
              role="tab"
              aria-controls="pill-vento"
              aria-selected="false"
              @click="setTab('Vento')"
            >
              Vento
            </button>
          </li>
        </ul>
        <!-- Situazione generale inizio -->
        <div
          v-show="selectedTab == 'Situazione generale'"
          id="pill-situazione"
          role="tabpanel"
          aria-labelledby="pill-situazione-tab"
        >
          <div class="col-md-12 mb-3 mt-3">
            <h4>Situazione generale</h4>
            <textarea
              id="situation"
              v-model="analisi.situation"
              :disabled="readonly"
              :style="textValidity['situation'] ? 'border: #FF0000; border:3px solid #FF0000;' : ''"
              name="situation"
              class="form-control"
              style="height: 150px; width: 100%"
              @change="saveField('situation')"
            />
            <br>
            <h4>Nuvolosità e visibilità</h4>
            <textarea
              id="cloudiness"
              v-model="analisi.cloudiness"
              :disabled="readonly"
              :style="textValidity['cloudiness'] ? 'border: #FF0000; border:3px solid #FF0000;' : ''"
              name="cloudiness"
              class="form-control"
              style="height: 150px; width: 100%"
              @change="saveField('cloudiness')"
            />
            <br>
            <h4>Codice di tempo</h4>
            <textarea
              id="weather_code"
              v-model="analisi.weather_code"
              :disabled="readonly"
              :style="textValidity['weather_code'] ? 'border: #FF0000; border:3px solid #FF0000;' : ''"
              name="weather_code"
              class="form-control small-width"
              rows="1"
              @change="saveField('weather_code')"
            />
          </div>
          <br>
          <div class="row">
            <div class="col-6">
              <h4>Nuvolosità Mattino</h4>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['COP_TOT'][1].classes_value"
                  :data="analisi.w17classes[30]['COP_TOT'][1]"
                  :readonly="readonly"
                  :validity="classesValidity[30]['COP_TOT'][1]"
                  :title="'Classe di Appartenenza :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['COP_TOT'][2].classes_value"
                  :data="analisi.w17classes[30]['COP_TOT'][2]"
                  :readonly="readonly"
                  :validity="classesValidity[30]['COP_TOT'][2]"
                  :title="'Evoluzione :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['COP_TOT'][3].classes_value"
                  :data="analisi.w17classes[30]['COP_TOT'][3]"
                  :readonly="readonly"
                  :validity="classesValidity[30]['COP_TOT'][3]"
                  :title="'Localizzazione :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['COP_TOT'][4].classes_value"
                  :data="analisi.w17classes[30]['COP_TOT'][4]"
                  :readonly="readonly"
                  :validity="classesValidity[30]['COP_TOT'][4]"
                  :title="'Visibilità :'"
                  @set-class="setClass"
                />
              </div>
            </div>
            <div class="col-6">
              <h4>Nuvolosità Pomeriggio</h4>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['COP_TOT'][1].classes_value"
                  :data="analisi.w17classes[31]['COP_TOT'][1]"
                  :readonly="readonly"
                  :validity="classesValidity[31]['COP_TOT'][1]"
                  :title="'Classe di Appartenenza :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['COP_TOT'][2].classes_value"
                  :data="analisi.w17classes[31]['COP_TOT'][2]"
                  :readonly="readonly"
                  :validity="classesValidity[31]['COP_TOT'][2]"
                  :title="'Evoluzione :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['COP_TOT'][3].classes_value"
                  :data="analisi.w17classes[31]['COP_TOT'][3]"
                  :readonly="readonly"
                  :validity="classesValidity[31]['COP_TOT'][3]"
                  :title="'Localizzazione :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['COP_TOT'][4].classes_value"
                  :data="analisi.w17classes[31]['COP_TOT'][4]"
                  :readonly="readonly"
                  :validity="classesValidity[31]['COP_TOT'][4]"
                  :title="'Visibilità :'"
                  @set-class="setClass"
                />
              </div>
            </div>
          </div>
        </div>
        <!-- Situazione generale fine -->
        <!-- Precipitazioni inizio -->
        <div
          v-show="selectedTab == 'Precipitazioni'"
          id="pill-precipitazione"
          role="tabpanel"
          aria-labelledby="pill-precipitazione-tab"
        >
          <div class="col-md-12 mb-3 mt-3">
            <h4>Precipitazioni giornaliere</h4>
            <textarea
              id="precipitazioni_giornaliere"
              v-model="analisi.w17data['PLUV'][32][67][912].text_value"
              :style="textValidity['PLUV'] ? 'border: #FF0000; border:3px solid #FF0000;' : ''"
              :disabled="readonly"
              class="form-control"
              name="precipitazioni_giornaliere"
              style="height: 100px; width: 100%"
              @change="saveText('PLUV', 32, 67, 912)"
            /> 
          </div>

          <br>
          <div class="row">
            <div class="col-8">
              <table class="table">
                <thead>
                  <tr>
                    <th
                      rowspan="3"
                      class="vertical-center"
                    >
                      Prov
                    </th>
                    <th colspan="5">
                      MATTINO
                    </th>
                  </tr>
                  <tr>
                    <th rowspan="2">
                      Media Areale
                    </th>
                    <th colspan="2">
                      Massimo puntuale su 12 ore
                    </th>
                    <th colspan="2">
                      Massimo puntuale su 3 ore
                    </th>
                  </tr>
                  <tr>
                    <th>Stazione</th>
                    <th>mm/12h</th>
                    <th>Stazione</th>
                    <th>mm/3h</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(v, k) in analisi.w17data['PLUV'][30]"
                    :key="k"
                  >
                    <th scope="row">
                      {{ province[k] }}
                    </th>
                    <td scope="row">
                      <div class="input-group">
                        <input
                          class="form-control"
                          style="height: 25px; width: 100px"
                          :value="v[901].numeric_value"
                          :disabled="readonly"
                          type="number"
                          step="0.1"
                          min="0.1"
                          @change="saveNumeric('PLUV', 30, k, 901)"
                        >
                        <button 
                          class="btn btn-outline-secondary button"
                          :disabled="readonly"
                          @click="clearValue(v[901])"
                        >
                          x
                        </button>
                      </div>
                    </td>
                    <td scope="row">
                      <input
                        class="form-control"
                        style="height: 25px; width: 100%"
                        :value="stazioni[v[907].cod_staz_meteo]"
                        disabled="true"
                      >
                    </td>
                    <td scope="row">
                      <div class="input-group">
                        <input
                          class="form-control"
                          style="height: 25px; width: 100px"
                          :value="v[907].numeric_value"
                          :disabled="readonly"
                          type="number"
                          step="0.1"
                          min="0.1"
                          @change="saveNumeric('PLUV', 30, k, 907)"
                        >
                        <button 
                          class="btn btn-outline-secondary button"
                          :disabled="readonly"
                          @click="clearValue(v[907])"
                        >
                          x
                        </button>
                      </div>
                    </td>
                    <td scope="row">
                      <input
                        class="form-control"
                        style="height: 25px; width: 100%"
                        :value="stazioni[v[905].cod_staz_meteo]"
                        disabled="true"
                      >
                    </td>
                    <td scope="row">
                      <div class="input-group">
                        <input
                          class="form-control"
                          style="height: 25px; width: 100px"
                          :value="v[905].numeric_value"
                          :disabled="readonly"
                          type="number"
                          step="0.1"
                          min="0.1"
                          @change="saveNumeric('PLUV', 30, k, 905)"
                        >
                        <button 
                          class="btn btn-outline-secondary button"
                          :disabled="readonly"
                          @click="clearValue(v[905])"
                        >
                          x
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table class="table">
                <thead>
                  <tr>
                    <th
                      rowspan="3"
                      class="vertical-center"
                    >
                      Prov
                    </th>
                    <th colspan="5">
                      MATTINO
                    </th>
                  </tr>
                  <tr>
                    <th rowspan="2">
                      Media Areale
                    </th>
                    <th colspan="2">
                      Massimo puntuale su 12 ore
                    </th>
                    <th colspan="2">
                      Massimo puntuale su 3 ore
                    </th>
                  </tr>
                  <tr>
                    <th>Stazione</th>
                    <th>mm/12h</th>
                    <th>Stazione</th>
                    <th>mm/3h</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(v, k) in analisi.w17data['PLUV'][31]"
                    :key="k"
                  >
                    <th scope="row">
                      {{ province[k] }}
                    </th>
                    <td scope="row">
                      <div class="input-group">
                        <input
                          class="form-control"
                          style="height: 25px; width: 100px"
                          :value="v[901].numeric_value"
                          :disabled="readonly"
                          type="number"
                          step="0.1"
                          min="0.1"
                          @change="saveNumeric('PLUV', 31, k, 901)"
                        >
                        <button 
                          class="btn btn-outline-secondary button"
                          :disabled="readonly"
                          @click="clearValue(v[901])"
                        >
                          x
                        </button>
                      </div>
                    </td>
                    <td scope="row">
                      <input
                        class="form-control"
                        style="height: 25px; width: 100%"
                        :value="stazioni[v[907].cod_staz_meteo]"
                        disabled="true"
                      >
                    </td>
                    <td scope="row">
                      <div class="input-group">
                        <input
                          class="form-control"
                          style="height: 25px; width: 100px"
                          :value="v[907].numeric_value"
                          :disabled="readonly"
                          type="number"
                          step="0.1"
                          min="0.1"
                          @change="saveNumeric('PLUV', 31, k, 907)"
                        >
                        <button 
                          class="btn btn-outline-secondary button"
                          :disabled="readonly"
                          @click="clearValue(v[907])"
                        >
                          x
                        </button>
                      </div>
                    </td>
                    <td scope="row">
                      <input
                        class="form-control"
                        style="height: 25px; width: 100%"
                        :value="stazioni[v[905].cod_staz_meteo]"
                        disabled="true"
                      >
                    </td>
                    <td scope="row">
                      <div class="input-group">
                        <input
                          class="form-control"
                          style="height: 25px; width: 100px"
                          :value="v[905].numeric_value"
                          type="number"
                          :disabled="readonly"
                          step="0.1"
                          min="0.1"
                          @change="saveNumeric('PLUV', 31, k, 905)"
                        >
                        <button 
                          class="btn btn-outline-secondary button"
                          :disabled="readonly"
                          @click="clearValue(v[905])"
                        >
                          x
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="col-4">
              <img
                v-if="today == analisi.data_emissione"
                :src="url_prec_mattino_image"
                class="img-fluid"
                style="height: 500px; width: 500px;"
              >
              <img
                v-else
                src="../back/static/images/empty.png"
                class="img-fluid"
                style="height: 500px; width: 500px;"
              >
              <img 
                v-if="today == analisi.data_emissione"
                :src="url_prec_pomeriggio_image"
                class="img-fluid"
                style="height: 500px; width: 500px;"
              >
              <img 
                v-else
                src="../back/static/images/empty.png"
                class="img-fluid"
                style="height: 500px; width: 500px;"
              >
            </div>
          </div>

          <br>
          <div class="row">
            <div class="col-6">
              <h4>Precipitazioni Mattino</h4>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['PLUV'][5].classes_value"
                  :data="analisi.w17classes[30]['PLUV'][5]"
                  :readonly="readonly"
                  :validity="classesValidity[30]['PLUV'][5]"
                  :title="'Classe su Regione :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['PLUV'][6].classes_value"
                  :data="analisi.w17classes[30]['PLUV'][6]"
                  :readonly="readonly"
                  :validity="classesValidity[30]['PLUV'][6]"
                  :title="'Classe su Area :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['PLUV'][7].classes_value"
                  :data="analisi.w17classes[30]['PLUV'][7]"
                  :readonly="readonly"
                  :validity="classesValidity[30]['PLUV'][7]"
                  :title="'Classe del Valore Massimo :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['PLUV'][8].classes_value"
                  :data="analisi.w17classes[30]['PLUV'][8]"
                  :readonly="readonly"
                  :validity="classesValidity[30]['PLUV'][8]"
                  :title="'Evoluzione :'"
                  @set-class="setClass"
                />
              </div>
            </div>
            <div class="col-6">
              <h4>Precipitazioni Pomeriggio</h4>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['PLUV'][5].classes_value"
                  :data="analisi.w17classes[31]['PLUV'][5]"
                  :readonly="readonly"
                  :validity="classesValidity[31]['PLUV'][5]"
                  :title="'Classe su Regione :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['PLUV'][6].classes_value"
                  :data="analisi.w17classes[31]['PLUV'][6]"
                  :readonly="readonly"
                  :validity="classesValidity[31]['PLUV'][6]"
                  :title="'Classe su Area :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['PLUV'][7].classes_value"
                  :data="analisi.w17classes[31]['PLUV'][7]"
                  :readonly="readonly"
                  :validity="classesValidity[31]['PLUV'][7]"
                  :title="'Classe del Valore Massimo :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['PLUV'][8].classes_value"
                  :data="analisi.w17classes[31]['PLUV'][8]"
                  :readonly="readonly"
                  :validity="classesValidity[31]['PLUV'][8]"
                  :title="'Evoluzione :'"
                  @set-class="setClass"
                />
              </div>
            </div>
          </div>
        </div>
        <!-- Precipitazioni fine -->
        <!-- Temperature e Zero Termico inizio -->
        <div
          v-show="selectedTab == 'Temperature e Zero Termico'"
          id="pill-temperature"
          role="tabpanel"
          aria-labelledby="pill-temperature-tab"
        >
          <div class="col-md-12 mb-3 mt-3">
            <h4>Temperature</h4>
            <textarea
              id="temperature"
              v-model="analisi.w17data['TERMA'][32][67][912].text_value"
              :style="textValidity['TERMA'] ? 'border: #FF0000; border:3px solid #FF0000;' : ''"
              :disabled="readonly"
              name="temperature"
              class="form-control"
              style="height: 50px; width: 100%"
              @change="saveText('TERMA', 32, 67, 912)"
            />
          </div>

          <div class="row">
            <div class="col-7">
              <table class="table">
                <thead>
                  <tr>
                    <th scope="col" />
                    <th scope="col">
                      Min
                    </th>
                    <th scope="col">
                      Trend
                    </th>
                    <th scope="col">
                      Max
                    </th>
                    <th scope="col">
                      Trend
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <th scope="col">
                      Pianura
                    </th>
                    <td scope="row">
                      <input
                        v-model="analisi.w17data['TERMA'][34][67][327].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 34, 67, 327)"
                      >
                    </td>
                    <td scope="row">
                      <input
                        v-model="analisi.w17data['TERMA'][34][67][327].id_trend"
                        class="form-control"
                        type="number"
                        :disabled="readonly"
                        @change="saveTrend('TERMA', 34, 67, 327)"
                      >
                    </td>
                    <td scope="row">
                      <input
                        v-model="analisi.w17data['TERMA'][33][67][328].numeric_value"
                        class="form-control"
                        type="number"
                        :disabled="readonly"
                        @change="saveNumeric('TERMA', 33, 67, 328)"
                      >
                    </td>
                    <td scope="row">
                      <input
                        v-model="analisi.w17data['TERMA'][33][67][328].id_trend"
                        class="form-control"
                        type="number"
                        :disabled="readonly"
                        @change="saveTrend('TERMA', 33, 67, 328)"
                      >
                    </td>
                  </tr>
                </tbody>
              </table>

              <table class="table">
                <thead>
                  <tr>
                    <th scope="col">
                      Prov
                    </th>
                    <th scope="col">
                      Minima
                    </th>
                    <th scope="col">
                      Trend
                    </th>
                    <th scope="col">
                      Massima
                    </th>
                    <th scope="col">
                      Trend
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <th scope="row">
                      AL
                    </th>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][34][9][327].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 34, 9, 327)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][34][9][327]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][33][9][328].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 33, 9, 328)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][33][9][328]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                  </tr>
                  <tr>
                    <th scope="row">
                      AT
                    </th>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][34][11][327].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 34, 11, 327)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][34][11][327]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][33][11][328].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 33, 11, 328)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][33][11][328]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                  </tr>
                  <tr>
                    <th scope="row">
                      BI
                    </th>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][34][1][327].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 34, 1, 327)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][34][1][327]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][33][1][328].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 33, 1, 328)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][33][1][328]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                  </tr>
                  <tr>
                    <th scope="row">
                      CN
                    </th>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][34][28][327].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 34, 28, 327)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][34][28][327]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][33][28][328].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 33, 28, 328)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][33][28][328]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                  </tr>
                  <tr>
                    <th scope="row">
                      NO
                    </th>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][34][33][327].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 34, 33, 327)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][34][33][327]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][33][33][328].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 33, 33, 328)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][33][33][328]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                  </tr>
                  <tr>
                    <th scope="row">
                      TO
                    </th>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][34][59][327].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 34, 59, 327)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][34][59][327]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][33][59][328].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 33, 59, 328)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][33][59][328]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                  </tr>
                  <tr>
                    <th scope="row">
                      VB
                    </th>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][34][63][327].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 34, 63, 327)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][34][63][327]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][33][63][328].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 33, 63, 328)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][33][63][328]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                  </tr>
                  <tr>
                    <th scope="row">
                      VC
                    </th>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][34][64][327].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 34, 64, 327)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][34][64][327]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA'][33][64][328].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA', 33, 64, 328)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA'][33][64][328]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                  </tr>
                  <tr>
                    <th scope="row">
                      700m
                    </th>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA_700'][34][67][327].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA_700', 34, 67, 327)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA_700'][34][67][327]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA_700'][33][67][328].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA_700', 33, 67, 328)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA_700'][33][67][328]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                  </tr>
                  <tr>
                    <th scope="row">
                      1500m
                    </th>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA_1500'][34][67][327].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA_1500', 34, 67, 327)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA_1500'][34][67][327]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA_1500'][33][67][328].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA_1500', 33, 67, 328)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA_1500'][33][67][328]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                  </tr>
                  <tr>
                    <th scope="row">
                      2000m
                    </th>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA_2000'][34][67][327].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA_2000', 34, 67, 327)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA_2000'][34][67][327]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                    <td>
                      <input
                        v-model="analisi.w17data['TERMA_2000'][33][67][328].numeric_value"
                        :disabled="readonly"
                        type="number"
                        class="form-control"
                        @change="saveNumeric('TERMA_2000', 33, 67, 328)"
                      >
                    </td>
                    <td>
                      <TrendSelect
                        :trend="trend"
                        :data="analisi.w17data['TERMA_2000'][33][67][328]"
                        :readonly="readonly"
                        @set-trend="setTrend"
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="col-1" />
            <div class="col-4">
              <div class="row">
                <h3>Radiosondaggi</h3>
                <div class="col-4">
                  <h4>Cuneo 00 ieri</h4>
                  <button
                    type="button"
                    @click="openTab(url_sound_1)"
                  >
                    <img
                      v-if="today == analisi.data_emissione"
                      :src="url_sound_1"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                    <img 
                      v-else
                      src="../back/static/images/empty.png"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                  </button>
                  <h4>Cameri 00 ieri</h4>
                  <button
                    type="button"
                    @click="openTab(url_sound_6)"
                  >
                    <img
                      v-if="today == analisi.data_emissione"
                      :src="url_sound_6"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                    <img 
                      v-else
                      src="../back/static/images/empty.png"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                  </button>
                </div>
                <div class="col-4">
                  <h4>Cuneo 12 ieri</h4>
                  <button
                    type="button"
                    @click="openTab(url_sound_2)"
                  >
                    <img
                      v-if="today == analisi.data_emissione"
                      :src="url_sound_2"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                    <img 
                      v-else
                      src="../back/static/images/empty.png"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                  </button>
                  <h4>Cameri 12 ieri</h4>
                  <button
                    type="button"
                    @click="openTab(url_sound_5)"
                  >
                    <img
                      v-if="today == analisi.data_emissione"
                      :src="url_sound_5"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                    <img 
                      v-else
                      src="../back/static/images/empty.png"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                  </button>
                  <h4>Analisi ECMWF</h4>
                  <button
                    type="button"
                    @click="openTab(url_freezingl_0)"
                  >
                    <img
                      v-if="today == analisi.data_emissione"
                      :src="url_freezingl_0"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                    <img 
                      v-else
                      src="../back/static/images/empty.png"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                  </button>
                </div>
                <div class="col-4">
                  <h4>Cuneo 00 oggi</h4>
                  <button
                    type="button"
                    @click="openTab(url_sound_3)"
                  >
                    <img
                      v-if="today == analisi.data_emissione"
                      :src="url_sound_3"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                    <img 
                      v-else
                      src="../back/static/images/empty.png"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                  </button>
                  <h4>Cameri 00 oggi</h4>
                  <button
                    type="button"
                    @click="openTab(url_sound_4)"
                  >
                    <img 
                      v-if="today == analisi.data_emissione"
                      :src="url_sound_4"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                    <img 
                      v-else
                      src="../back/static/images/empty.png"
                      alt="Anteprima immagine"
                      style="max-width: 150px; max-height: 150px;"
                    >
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-12 mb-3 mt-3">
            <h4>Zero Termico</h4>
            <textarea
              id="zero_termico"
              v-model="analisi.w17data['FRZLVL'][32][67][912].text_value"
              :style="textValidity['FRZLVL'] ? 'border: #FF0000; border:3px solid #FF0000;' : ''"
              :disabled="readonly"
              name="zero_termico"
              class="form-control"
              @change="saveText('FRZLVL', 32, 67, 912)"
            />
          </div>

          <!-- No validation for SNOW_LEV since it need to be "" to disappear in the pdf-->
          <div class="col-md-12 mb-3 mt-3">
            <h4>Nevicate e Quota Neve</h4>
            <textarea
              id="nevicate"
              v-model="analisi.w17data['SNOW_LEV'][32][67][912].text_value"
              :disabled="readonly"
              name="nevicate"
              class="form-control"
              @change="saveText('SNOW_LEV', 32, 67, 912)"
            />
          </div>

          <div class="row">
            <div class="col-6">
              <h4>Zero Termico</h4>
              <form class="row">
                <div class="col-6">
                  <label
                    for="valore_12_24"
                    class="form-label"
                  >Valore dalle 12 alle 24:</label>
                  <input
                    id="valore_12_24"
                    v-model="analisi.w17data['FRZLVL'][31][67][914].numeric_value"
                    :style="numberValidity['FRZLVL'][31][67][914] ? 'border: #FF0000; border:3px solid #FF0000;' : ''"
                    :disabled="readonly"
                    type="number"
                    step="100"
                    class="form-control"
                    @change="saveNumeric('FRZLVL', 31, 67, 914)"
                  >
                </div>
                <div class="col-6">
                  <ClassesSelect
                    :classes-value="rearrengedclasses['FRZLVL'][12].classes_value"
                    :data="analisi.w17classes[31]['FRZLVL'][12]"
                    :readonly="readonly"
                    :validity="classesValidity[31]['FRZLVL'][12]"
                    :title="'&nbsp'"
                    @set-class="setClass"
                  />
                </div>
              </form>
              <form class="row">
                <div class="col-6 mt-3">
                  <label
                    for="valore_00_24"
                    class="form-label"
                  >Valore dalle 00 alle 24	:</label>
                  <input
                    id="valore_00_24"
                    v-model="analisi.w17data['FRZLVL'][32][67][912].numeric_value"
                    :style="numberValidity['FRZLVL'][32][67][912] ? 'border: #FF0000; border:3px solid #FF0000;' : ''"
                    :disabled="readonly"
                    type="number"
                    step="100"
                    class="form-control"
                    @change="saveNumeric('FRZLVL', 32, 67, 912)"
                  >
                </div>
                <div class="col-6 mt-3">
                  <ClassesSelect
                    :classes-value="rearrengedclasses['FRZLVL'][13].classes_value"
                    :data="analisi.w17classes[32]['FRZLVL'][13]"
                    :readonly="readonly"
                    :validity="classesValidity[32]['FRZLVL'][13]"
                    :title="'&nbsp'"
                    @set-class="setClass"
                  />
                </div>
              </form>
            </div>
            <div
              v-if="'SNOW_LEV' in analisi.w17classes[32]"
              class="col-6"
            >
              <h4>Quota Neve</h4>
              <form class="row">
                <div class="col-6">
                  <label
                    for="valore_riferimento_min"
                    class="form-label"
                  >Valore di riferimento min:</label>
                  <input
                    id="valore_riferimento_min"
                    v-model="analisi.w17data['SNOW_LEV'][32][67][324].numeric_value"
                    :style="numberValidity['SNOW_LEV'][32][67][324] ? 'border: #FF0000; border:3px solid #FF0000;' : ''"
                    :disabled="readonly"
                    type="number"
                    step="100"
                    class="form-control"
                    @change="saveNumeric('SNOW_LEV', 32, 67, 324)"
                  >
                </div>
                <div class="col-6">
                  <ClassesSelect
                    :classes-value="rearrengedclasses['SNOW_LEV'][14].classes_value"
                    :data="analisi.w17classes[32]['SNOW_LEV'][14]"
                    :readonly="readonly"
                    :title="'&nbsp'"
                    @set-class="setClass"
                  />
                </div>
              </form>
              <form class="row">
                <div class="col-6 mt-3">
                  <label
                    for="valore_riferimento_max"
                    class="form-label"
                  >Valore di riferimento max:</label>
                  <input
                    id="valore_riferimento_max"
                    v-model="analisi.w17data['SNOW_LEV'][32][67][323].numeric_value"
                    :style="numberValidity['SNOW_LEV'][32][67][323] ? 'border: #FF0000; border:3px solid #FF0000;' : ''"
                    :disabled="readonly"
                    type="number"
                    step="100"
                    class="form-control"
                    @change="saveNumeric('SNOW_LEV', 32, 67, 323)"
                  >
                </div>
                <div class="col-6 mt-3">
                  <ClassesSelect
                    :classes-value="rearrengedclasses['SNOW_LEV'][15].classes_value"
                    :data="analisi.w17classes[32]['SNOW_LEV'][15]"
                    :readonly="readonly"
                    :title="'&nbsp'"
                    @set-class="setClass"
                  />
                </div>
              </form>
            </div>
          </div>
        </div>
        <!-- Temperature e Zero Termico fine -->
        <!-- Vento inizio -->
        <div
          v-show="selectedTab == 'Vento'"
          id="pill-vento"
          role="tabpanel"
          aria-labelledby="pill-vento-tab"
        >
          <div class="col-md-12 mb-3 mt-3">
            <h4>Venti</h4>
            <textarea
              id="venti"
              v-model="analisi.w17data['VELS'][32][67][912].text_value"
              :style="textValidity['VELS'] ? 'border: #FF0000; border:3px solid #FF0000;' : ''"
              :disabled="readonly"
              name="venti"
              class="form-control"
              style="height: 150px; width: 100%"
              @change="saveText('VELS', 32, 67, 912)"
            />
          </div>

          <br>
          <div class="row">
            <h3>Analisi ECMWF 0100</h3>
            <div class="col-3">
              <h4>Vento 700</h4>
              <button
                type="button"
                @click="openTab(url_wind_700)"
              >
                <img
                  v-if="today == analisi.data_emissione"
                  :src="url_wind_700"
                  alt="Anteprima immagine"
                  style="max-width: 250px; max-height: 250px;"
                >
                <img
                  v-else
                  src="../back/static/images/empty.png"
                  alt="Anteprima immagine"
                  style="max-width: 250px; max-height: 250px;"
                >
              </button>
            </div>
            <div class="col-3">
              <h4>Vento 850</h4>
              <button
                type="button"
                @click="openTab(url_wind_850)"
              >
                <img
                  v-if="today == analisi.data_emissione"
                  :src="url_wind_850"
                  alt="Anteprima immagine"
                  style="max-width: 250px; max-height: 250px;"
                >
                <img
                  v-else
                  src="../back/static/images/empty.png"
                  alt="Anteprima immagine"
                  style="max-width: 250px; max-height: 250px;"
                >
              </button>
            </div>
            <div class="col-3">
              <h4>Vento 925</h4>
              <button
                type="button"
                @click="openTab(url_wind_925)"
              >
                <img
                  v-if="today == analisi.data_emissione"
                  :src="url_wind_925"
                  alt="Anteprima immagine"
                  style="max-width: 250px; max-height: 250px;"
                >
                <img
                  v-else
                  src="../back/static/images/empty.png"
                  alt="Anteprima immagine"
                  style="max-width: 250px; max-height: 250px;"
                >
              </button>
            </div>
            <div class="col-3">
              <h4>Vento 1000</h4>
              <button
                type="button"
                @click="openTab(url_wind_1000)"
              >
                <img
                  v-if="today == analisi.data_emissione"
                  :src="url_wind_1000"
                  alt="Anteprima immagine"
                  style="max-width: 250px; max-height: 250px;"
                >
                <img
                  v-else
                  src="../back/static/images/empty.png"
                  alt="Anteprima immagine"
                  style="max-width: 250px; max-height: 250px;"
                >
              </button>
            </div>
          </div>

          <br>
          <div class="row">
            <div class="col-6">
              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['VELV'][16].classes_value"
                  :data="analisi.w17classes[32]['VELV'][16]"
                  :readonly="readonly"
                  :validity="classesValidity[32]['VELV'][16]"
                  :title="'Intensità in pianura :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['VELV'][18].classes_value"
                  :data="analisi.w17classes[32]['VELV'][18]"
                  :readonly="readonly"
                  :validity="classesValidity[32]['VELV'][18]"
                  :title="'Intensità in montagna :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['VELV'][20].classes_value"
                  :data="analisi.w17classes[32]['VELV'][20]"
                  :readonly="readonly"
                  :validity="classesValidity[32]['VELV'][20]"
                  :title="'Rinforzi :'"
                  @set-class="setClass"
                />
              </div>
            </div>
            <div class="col-6">
              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['VELV'][17].classes_value"
                  :data="analisi.w17classes[32]['VELV'][17]"
                  :readonly="readonly"
                  :validity="classesValidity[32]['VELV'][17]"
                  :title="'Andamento in pianura :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['VELV'][19].classes_value"
                  :data="analisi.w17classes[32]['VELV'][19]"
                  :readonly="readonly"
                  :validity="classesValidity[32]['VELV'][19]"
                  :title="'Andamento in montagna :'"
                  @set-class="setClass"
                />
              </div>

              <div class="mb-3">
                <ClassesSelect
                  :classes-value="rearrengedclasses['VELV'][21].classes_value"
                  :data="analisi.w17classes[32]['VELV'][21]"
                  :readonly="readonly"
                  :validity="classesValidity[32]['VELV'][21]"
                  :title="'Foehn :'"
                  @set-class="setClass"
                />
              </div>
            </div>
          </div>
        </div>
        <!-- Vento fine -->
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import ClassesSelect from './ClassesSelect.vue'
  import TrendSelect from './TrendSelect.vue'

  export default {
    name: 'AnalisiBulletin',
    components: {
      ClassesSelect,
      TrendSelect,
    }
  }
</script>

<script setup lang="ts">
import { Ref, ref, onMounted, watch, computed} from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vue-toast-notification'

import api from '../../src/api'
import store from '../../src/store'

import { components } from '../../src/types/weboll'

const router = useRouter()
const route = useRoute()
const toast = useToast()

type Trend = components["schemas"]["Trend"]
type W17 = components["schemas"]["W17"]
type W17Data = components['schemas']['W17Data']
type W17Classes = components['schemas']['W17Classes']
type W17Full = W17 & { w17data_set: W17Data[], w17classes_set: W17Classes[] }
type w17data = {
  "TERMA": {
    "32": {
      "67": {
        "912": W17Data,
      }
    },
    "33": {
      "1": {
        "328": W17Data,
      },
      "9": {
        "328": W17Data,
      },
      "11": {
        "328": W17Data,
      },
      "28": {
        "328": W17Data,
      },
      "33": {
        "328": W17Data,
      },
      "59": {
        "328": W17Data,
      },
      "63": {
        "328": W17Data,
      },
      "64": {
        "328": W17Data,
      },
      "67": {
        "328": W17Data,
      }
    },
    "34": {
      "1": {
        "327": W17Data,
      },
      "9": {
        "327": W17Data,
      },
      "11": {
        "327": W17Data,
      },
      "28": {
        "327": W17Data,
      },
      "33": {
        "327": W17Data,
      },
      "59": {
        "327": W17Data,
      },
      "63": {
        "327": W17Data,
      },
      "64": {
        "327": W17Data,
      },
      "67": {
        "327": W17Data,
      }
    }
  },
  "FRZLVL": {
    "31": {
      "67": {
        "914": W17Data,
      }
    },
    "32": {
      "67": {
        "912": W17Data,
      }
    }
  },
  "PLUV": {
    "30": {
      "171": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "172": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "173": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "174": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "175": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "176": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "177": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "178": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      }
    },
    "31": {
      "171": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "172": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "173": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "174": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "175": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data
      },
      "176": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "177": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      },
      "178": {
        "901": W17Data,
        "905": W17Data,
        "907": W17Data,
      }
    },
    "32": {
      "67": {
        "912": W17Data,
      }
    }
  },
  "SNOW_LEV": {
    "32": {
      "67": {
        "323": W17Data,
        "324": W17Data,
        "912": W17Data,
      }
    }
  },
  "VELS": {
    "32": {
      "67": {
        "912": W17Data,
      }
    }
  },
  "TERMA_1500": {
    "33": {
      "67": {
        "328": W17Data,
      }
    },
    "34": {
      "67": {
        "327": W17Data,
      }
    }
  },
  "TERMA_2000": {
    "33": {
      "67": {
        "328": W17Data,
      }
    },
    "34": {
      "67": {
        "327": W17Data,
      }
    }
  },
  "TERMA_700": {
    "33": {
      "67": {
        "328": W17Data,
      }
    },
    "34": {
      "67": {
        "327": W17Data,
      }
    }
  }
}
type w17classes = {
    "30": {
      "COP_TOT": {
        [index: number]: W17Classes,
      },
      "PLUV": {
        [index: number]: W17Classes,
      }
    },
    "31": {
      "COP_TOT": {
        [index: number]: W17Classes
      },
      "PLUV": {
        [index: number]: W17Classes
      },
      "FRZLVL": {
        [index: number]: W17Classes
      },
      "SNOW_LEV"?: {
        [index: number]: W17Classes
      }
    },
    "32": {
      "FRZLVL": {
        [index: number]: W17Classes
      },
      "VELV": {
        [index: number]: W17Classes
      },
      "SNOW_LEV"?: {
        [index: number]: W17Classes
      }
    },
    "33": {
      "TERMA": {
        [index: number]: W17Classes
      }
    },
    "34": {
      "TERMA": {
        [index: number]: W17Classes
      }
    }
  }
type W17FullRearranged = W17Full & {w17classes?: w17classes, w17data?: w17data}
type ArrayTransformer = (arr: Array<any>) => any

// reactive properties
const w17classes_set_istance: W17Classes = {
          "id_w17_classes": 2,
          "id_w17": 3408,
          "id_parametro": "COP_TOT",
          "id_classes_value": 3,
          "id_classes": 1,
          "id_time_layouts": 30
        }
const w17data_set_istance: W17Data = {
          "id_w17_data": 28,
          "numeric_value": "27",
          "id_trend": 2,
          "text_value": null,
          "cod_staz_meteo": null,
          "id_w17": 3408,
          "id_venue": 67,
          "id_time_layouts": 33,
          "id_parametro": "TERMA_700",
          "id_aggregazione": 328
        }
let trend: Ref<Trend[]> = ref([])
let analisi_id = ref('')
let analisi : Ref<W17FullRearranged> = ref({
  "id_w17":3384,
  "w17data_set":[],
  "w17classes_set":[],
  "w17data": {
    "TERMA": {
      "32": {
        "67": {
          "912": w17data_set_istance,
        }
      },
      "33": {
        "1": {
          "328": w17data_set_istance,
        },
        "9": {
          "328": w17data_set_istance,
        },
        "11": {
          "328": w17data_set_istance,
        },
        "28": {
          "328": w17data_set_istance,
        },
        "33": {
          "328": w17data_set_istance,
        },
        "59": {
          "328": w17data_set_istance,
        },
        "63": {
          "328": w17data_set_istance,
        },
        "64": {
          "328": w17data_set_istance,
        },
        "67": {
          "328": w17data_set_istance,
        }
      },
      "34": {
        "1": {
          "327": w17data_set_istance,
        },
        "9": {
          "327": w17data_set_istance,
        },
        "11": {
          "327": w17data_set_istance,
        },
        "28": {
          "327": w17data_set_istance,
        },
        "33": {
          "327": w17data_set_istance,
        },
        "59": {
          "327": w17data_set_istance,
        },
        "63": {
          "327": w17data_set_istance,
        },
        "64": {
          "327": w17data_set_istance,
        },
        "67": {
          "327": w17data_set_istance,
        }
      }
    },
    "FRZLVL": {
      "31": {
        "67": {
          "914": w17data_set_istance,
        }
      },
      "32": {
        "67": {
          "912": w17data_set_istance,
        }
      }
    },
    "PLUV": {
      "30": {
        "171": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "172": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "173": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "174": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "175": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "176": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "177": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "178": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        }
      },
      "31": {
        "171": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "172": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "173": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "174": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "175": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "176": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "177": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        },
        "178": {
          "901": w17data_set_istance,
          "905": w17data_set_istance,
          "907": w17data_set_istance,
        }
      },
      "32": {
        "67": {
          "912": w17data_set_istance,
        }
      }
    },
    "SNOW_LEV": {
      "32": {
        "67": {
          "323": w17data_set_istance,
          "324": w17data_set_istance,
          "912": w17data_set_istance,
        }
      }
    },
    "VELS": {
      "32": {
        "67": {
          "912": w17data_set_istance,
        }
      }
    },
    "TERMA_1500": {
      "33": {
        "67": {
          "328": w17data_set_istance,
        }
      },
      "34": {
        "67": {
          "327": w17data_set_istance,
        }
      }
    },
    "TERMA_2000": {
      "33": {
        "67": {
          "328": w17data_set_istance,
        }
      },
      "34": {
        "67": {
          "327": w17data_set_istance,
        }
      }
    },
    "TERMA_700": {
      "33": {
        "67": {
          "328": w17data_set_istance,
        }
      },
      "34": {
        "67": {
          "327": w17data_set_istance,
        }
      }
    }
  },
  "w17classes": {
    "30": {
      "COP_TOT": {
        "1": w17classes_set_istance,
      },
      "PLUV": {
        "5": w17classes_set_istance,
      }
    },
    "31": {
      "COP_TOT": {
        "1": w17classes_set_istance
      },
      "PLUV": {
        "5": w17classes_set_istance
      },
      "FRZLVL": {
        "12": w17classes_set_istance
      }
    },
    "32": {
      "FRZLVL": {
        "13": w17classes_set_istance
      },
      "VELV": {
        "16": w17classes_set_istance
      }
    },
    "33": {
      "TERMA": {
        "10": w17classes_set_istance
      }
    },
    "34": {
      "TERMA": {
        "9": w17classes_set_istance
      }
    }
  },  
  "data_analysis":"2023-06-05",
  "data_emissione":"2023-06-06",
  "next_blt_time":"2023-06-07",
  "situation":"Un'area di bassa...",
  "cloudiness":"...",
  "weather_code":"20",
  "last_update":"2023-06-06T09:14:06",
  "username":"",
  "status":"1",
  "numero_bollettino":"157/2023",
  "id_w17_parent":null
  })
let ready = ref(false)
let countfetch = ref(0)
let state = ref(store.state)
let today = ref('')
let rearrengedclasses = ref({})
let stazioni = ref({})
let readonly = ref(true)
let actions = ref({
  sending: false,
  reopening: false,
})
let province = ref({
  171: 'AL',
  172: 'AT',
  173: 'BI',
	174: 'CN',
  175: 'NO',
  176: 'TO',
	177: 'VB',
  178: 'VC'
})
let selectedTab = ref('Situazione generale')

let nullClass = ref([81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101])

const classesValidity = computed(() => {
  let classV = {}
  for (const tl in analisi.value.w17classes) {
    classV[tl] = {}
    for (const param in analisi.value.w17classes[tl]) {
      classV[tl][param] = {}
      for (const classe in analisi.value.w17classes[tl][param]) {
        classV[tl][param][classe] = false
        if (nullClass.value.includes(analisi.value.w17classes[tl][param][classe].id_classes_value)){
          classV[tl][param][classe] = true
        }
      }
    }
  }
  return classV
})

const numberValidity = computed(() => {
  const valueV = {}
  for (const param in analisi.value.w17data) {
    valueV[param] = {}
    for (const tl in analisi.value.w17data[param]) {
      valueV[param][tl] = {}
      for (const aggr in analisi.value.w17data[param][tl]) {
        valueV[param][tl][aggr] = {}
        for (const value in analisi.value.w17data[param][tl][aggr]) {
          const numericValue = analisi.value.w17data[param][tl][aggr][value].numeric_value
          if ( numericValue === null || numericValue === "" ){
            // SNOW_LEV può essere nullo
            if (param === "SNOW_LEV")
              valueV[param][tl][aggr][value] = false
            else
              valueV[param][tl][aggr][value] = true
          }else if(
            (param == "FRZLVL" && numericValue !== 0 && numericValue % 100 !== 0) ||
            (param == "FRZLVL" && numericValue > 6000) || 
            (param == "FRZLVL" && numericValue < 0) ) {
            valueV[param][tl][aggr][value] = true
          }else if(
            (param == "SNOW_LEV" && numericValue !== 0 && numericValue % 100 !== 0) ||
            (param == "SNOW_LEV" && numericValue > 4000) || 
            (param == "SNOW_LEV" && numericValue < 0) ) {
            valueV[param][tl][aggr][value] = true
          } else {
            valueV[param][tl][aggr][value] = false
          }
        }
      }
    }
  }
  return valueV
})


const textValidity = computed(() => {
  let textV = {}
  for (const param in analisi.value.w17data) {
    if (param !== 'SNOW_LEV' && param !== 'TERMA_1500' && param !== 'TERMA_2000' && param !== 'TERMA_700') {
      textV[param] = false
      if (analisi.value.w17data[param][32][67][912].text_value == null || analisi.value.w17data[param][32][67][912].text_value == "" ) {
        textV[param] = true
      }
    }
  }

  let w17_texts = ["situation", "cloudiness", "weather_code"]
  w17_texts.forEach(text => {
    if (analisi.value[text] == null || analisi.value[text] == "" ) {
      textV[text] = true
    }
    else textV[text] = false
  })
  return textV
})

const tabValidity = computed(() => {
  let tabV = { situazione_generale: false, precipitazioni: false, temperature: false, vento: false };

    // tab situazione_generale
  [30, 31].forEach(tl => {
    for (const classe in classesValidity.value[tl]["COP_TOT"]) {
      if (classesValidity.value[tl]["COP_TOT"][classe] || textValidity.value["situation"] == true || textValidity.value["cloudiness"] == true || textValidity.value["weather_code"] == true) {
        tabV.situazione_generale = true
      }
    }
  });

  // tab precipitazioni
  [30, 31].forEach(tl => {
    for (const classe in classesValidity.value[tl]["PLUV"]) {
      if (classesValidity.value[tl]["PLUV"][classe] || textValidity.value["PLUV"] == true) {
        tabV.precipitazioni = true
      }
    }
  });

  // tab temperature
  [31, 32].forEach(tl => {
    for (const classe in classesValidity.value[tl]["FRZLVL"]) {
      if (classesValidity.value[tl]["FRZLVL"][classe]) {
        tabV.temperature = true
      }
    }
  })

    if (textValidity.value["TERMA"] == true || textValidity.value["FRZLVL"] == true || numberValidity.value["FRZLVL"][31][67][914] == true || numberValidity.value["FRZLVL"][32][67][912] == true || numberValidity.value["SNOW_LEV"][32][67][323] == true  || numberValidity.value["SNOW_LEV"][32][67][324] == true ) {
    tabV.temperature = true
  }
  
  // tab vento
  for (const classe in classesValidity.value[32]["VELV"]) {
    if (classesValidity.value[32]["VELV"][classe] || textValidity.value["VELS"] == true){
      tabV.vento = true
    }
  }

  return tabV
})

const sendValidity = computed(() => {
  return !(Object.values(tabValidity.value).every((value) => value === false));
});

const url_base_data = computed(() => {
  return import.meta.env.VITE_BASE_DATA_URL || ""
});

const url_prec_mattino_image = computed(() => {
  return url_base_data.value + "/analisi/PLUV_913.PNG"
});

const url_prec_pomeriggio_image = computed(() => {
  return url_base_data.value + "/analisi/PLUV_914.PNG"
});

const url_sound_1 = computed(() => {
  return url_base_data.value + "/analisi/SOUND_1.PNG"
});

const url_sound_2 = computed(() => {
  return url_base_data.value + "/analisi/SOUND_2.PNG"
});

const url_sound_3 = computed(() => {
  return url_base_data.value + "/analisi/SOUND_3.PNG"
});

const url_sound_4 = computed(() => {
  return url_base_data.value + "/analisi/SOUND_4.PNG"
});

const url_sound_5 = computed(() => {
  return url_base_data.value + "/analisi/SOUND_5.PNG"
});

const url_sound_6 = computed(() => {
  return url_base_data.value + "/analisi/SOUND_6.PNG"
});

const url_freezingl_0 = computed(() => {
  return url_base_data.value + "/analisi/FREEZINGL_0.PNG"
});

const url_wind_700 = computed(() => {
  return url_base_data.value + "/analisi/WIND_700.PNG"
});

const url_wind_850 = computed(() => {
  return url_base_data.value + "/analisi/WIND_850.PNG"
});

const url_wind_925 = computed(() => {
  return url_base_data.value + "/analisi/WIND_925.PNG"
});

const url_wind_1000 = computed(() => {
  return url_base_data.value + "/analisi/WIND_1000.PNG"
});

onMounted(async () => {
  if (typeof route.params.id == "string") {
    analisi_id.value = route.params.id
    await fetchData()
  }
})

watch(countfetch, (count) => {
  if (count >= 4) {
    ready.value = true;
  }
})

async function fetchData () {
  today.value = dateToString(new Date())
  ready.value = false
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions

  await fetchAnalisi(analisi_id.value).then(response => {
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
  }).then((data: W17FullRearranged) => {
    // console.log("Analisi", data)
    data.w17data_set.forEach(x => {
      if (x.id_parametro === 'PLUV' && x.numeric_value != null) {
        x.numeric_value = Math.round(x.numeric_value * 10) / 10
      } else if (x.id_parametro === 'TERMA' || x.id_parametro === 'TERMA_700' || x.id_parametro === 'TERMA_1500' || x.id_parametro === 'TERMA_2000' || (x.id_parametro === 'FRZLVL' && x.numeric_value != null ) || x.id_parametro === 'SNOW_LEV') {
        if (x.numeric_value) x.numeric_value = Math.round(x.numeric_value)
      }
    })

    let w17classes = rearrange(
      data.w17classes_set,
      "id_time_layouts",
      data => rearrange(
        data,
        "id_parametro",
        data1 => rearrange(
          data1,
          "id_classes", arr => arr[0]
        )
      )
    )
    // console.log("w17classes", w17classes)
    data["w17classes"] = w17classes

    let w17data = rearrange(
      data.w17data_set,
      "id_parametro",
      data => rearrange(
        data,
        "id_time_layouts",
        data1 => rearrange(
          data1,
          "id_venue",
          data2 => rearrange(
            data2,
            "id_aggregazione", arr => arr[0]
          )
        )
      )
    )
    // console.log("w17data", w17data)
    // find w17data_set data in analisi.w17data['id_parametro'][id_time_layouts][id_venue][id_aggregazione]
    data["w17data"] = w17data

    analisi.value = data
    getTrend()
    getStazioni()
    rearrangeClasses()
    readonly.value = (analisi.value.status === '1' || analisi.value.status === '2' || !state.value.username)
    countfetch.value += 1
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

function rearrangeClasses() {
  fetchClasses().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero delle classi`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(data => {
    let classes = data.reduce((accumulator, currentValue) => {
      accumulator[currentValue.id_parametro][currentValue.id_classes] = currentValue;
      return accumulator
    }, { COP_TOT: {}, FRZLVL: {}, PLUV: {}, SNOW_LEV: {}, TERMA: {}, VELV: {} })
    Object.keys(classes).forEach(id_parametro => {
      let cl = classes[id_parametro]
      Object.keys(cl).forEach(index => {
        // get class descriptor array
        let classes_value = cl[index].classes_value
        // move last element of the array to the beginning
        classes_value.unshift(classes_value.pop())
      })
    })
    rearrengedclasses.value = classes
    // console.log("rearrengedclasses", rearrengedclasses.value)
    countfetch.value += 1
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

function getTrend() {
  fetchTrend().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero dei trends`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then((data: Trend[]) => {
    trend.value = data
    // add null trend
    let trend_null: Trend = {
      "id_trend": -1,
      "id_web": -2,
      "desc_ita": "n.d.",
      "desc_eng": "n.d.",
      "last_update": "2006-11-13T12:58:20",
      "username": "weboll",
    }
    trend.value.unshift(trend_null)
    trend.value = trend.value.sort((a, b) => a.id_trend - b.id_trend)
    countfetch.value += 1
  })
}

function getStazioni() {
  fetchStazioni().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero delle stazioni`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(data => {
    data.forEach(x => {
      if (x.cod_staz_meteo != null) {
        stazioni.value[x.cod_staz_meteo] = x.denominazione
      }
    })
    // console.log("stazioni.value", stazioni.value)
    countfetch.value += 1
  })
}

async function fetchAnalisi (id) {
  const response = await fetch('/api/w17/bulletins/' + id + '/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchClasses () {
  const response = await fetch('/api/w05/classes/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchTrend () {
  const response = await fetch('/api/w17/trend/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchStazioni () {
  const response = await fetch('/api/w17/stazioni/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchAnalisiAction (action) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w17/bulletins/${analisi_id.value}/${action}/`
  )
  return response
}

async function fetchPatch(id, endpoint, payload) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w17/${endpoint}/${id}/`,
    {
      method: 'PATCH',
      body: JSON.stringify(payload)
    }
  )
  return response
}

async function bulkUpdateW17(payload) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w17/bulletins/bulk_update/`,
    {
      method: 'POST',
      body: JSON.stringify(payload)
    }
  )
  return response
}

function updateW17(id_w17) {
  const payload = {}
  payload['id_w17'] = id_w17
  payload['username'] = store.state.username
  bulkUpdateW17(payload).then((response) => {
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
  }).then((data: W17) => {
    toast.open(
      {
        message: 'Dato salvato',
        type: 'success',
        position: 'top-left'
      }
    )
    analisi.value.last_update = data.last_update
    analisi.value.username = store.state.username
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

function setTrend(id_parametro: string, id_time_layouts : number, id_venue: number, id_aggregazione: number, new_value: number) {
  let payload = {}
  payload["id_trend"] = new_value
  savew17Trend(payload, id_parametro, id_time_layouts, id_venue, id_aggregazione)
}

function savew17Trend(payload, id_parametro, id_time_layouts, id_venue, id_aggregazione) {
  let id = analisi.value.w17data[id_parametro][id_time_layouts][id_venue][id_aggregazione].id_w17_data
  fetchPatch(id, 'data', payload).then((response) => {
    if (!response.ok) {
      toast.open(
        {
          message: 'Errore nel salvataggio',
          type: 'error',
          position: 'top-left'
        }
      )
    } else {
      analisi.value.w17data[id_parametro][id_time_layouts][id_venue][id_aggregazione].id_trend = payload.id_trend
      updateW17(analisi.value.id_w17)
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

function setClass(id_parametro: string, id_time_layouts: number, id_classes: number, new_value: number) {
  let payload = {}
  payload["id_classes_value"] = new_value
  savew17class(payload, id_parametro, id_time_layouts, id_classes)
}

function savew17class(payload, id_parametro, id_time_layouts, id_classes) {
  let id = analisi.value.w17classes[id_time_layouts][id_parametro][id_classes].id_w17_classes
  fetchPatch(id, 'classes', payload).then((response) => {
    if (!response.ok) {
      toast.open(
        {
          message: 'Errore nel salvataggio',
          type: 'error',
          position: 'top-left'
        }
      )
    } else {
      analisi.value.w17classes[id_time_layouts][id_parametro][id_classes].id_classes_value = payload.id_classes_value
      updateW17(analisi.value.id_w17)
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

function saveText(id_parametro, id_time_layouts, id_venue, id_aggregazione) {
  let id = analisi.value.w17data[id_parametro][id_time_layouts][id_venue][id_aggregazione].id_w17_data
  let payload = {}
  payload["text_value"] = analisi.value.w17data[id_parametro][id_time_layouts][id_venue][id_aggregazione].text_value
  fetchPatch(id, 'data', payload).then((response) => {
    if (!response.ok) {
      toast.open(
        {
          message: 'Errore nel salvataggio',
          type: 'error',
          position: 'top-left'
        }
      )
    } else {
      updateW17(analisi.value.id_w17)
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

function saveNumeric(id_parametro, id_time_layouts, id_venue, id_aggregazione) {

  // let value = analisi.value.w17data[id_parametro][id_time_layouts][id_venue][id_aggregazione].numeric_value
  let value
  if (id_parametro === 'PLUV')
    value = parseFloat((window.event.target as HTMLInputElement).value)
  else
    value = parseInt((window.event.target as HTMLInputElement).value)

  if ( (id_parametro === `FRZLVL` && (value !== 0 && value % 100 !== 0)) || 
    (id_parametro === `FRZLVL` && value > 6000) || 
    (id_parametro === `FRZLVL` && value < 0) ) {
    toast.open({
      message: 'Il valore deve essere 0 o un multiplo di 100 e inferiore a 6000 m.',
      type: 'error',
      position: 'top-left'
    });
    return
  }

  if ( !isNaN(value) ){
    if ( (id_parametro === `SNOW_LEV` && (value !== 0 && value % 100 !== 0)) || 
      (id_parametro === `SNOW_LEV` && value > 4000) || 
      (id_parametro === `SNOW_LEV` && value < 0) ) {
      toast.open({
        message: 'Il valore deve essere 0 o un multiplo di 100 e inferiore a 4000 m.',
        type: 'error',
        position: 'top-left'
      });
      return
    }
  }

  if ( isNaN(value) ) value = null // lo SNOW_LEV viene validato e può essere null
  // if ( typeof(value) === "string") value = null // lo SNOW_LEV viene validato e può essere null

  if ( id_parametro === `SNOW_LEV` && 
    analisi.value.w17data["SNOW_LEV"][32][67][324].numeric_value !== null &&
    analisi.value.w17data["SNOW_LEV"][32][67][324].numeric_value !== "" &&
    analisi.value.w17data["SNOW_LEV"][32][67][323].numeric_value !== null &&
    analisi.value.w17data["SNOW_LEV"][32][67][323].numeric_value !== "" ){
    if (analisi.value.w17data["SNOW_LEV"][32][67][324].numeric_value >
      analisi.value.w17data["SNOW_LEV"][32][67][323].numeric_value){
      toast.open({
        message: 'Il valore della quota neve minima dev\'essere uguale o inferiore alla quota massima.',
        type: 'error',
        position: 'top-left'
      });
      return
    }
  }
  
  analisi.value.w17data[id_parametro][id_time_layouts][id_venue][id_aggregazione].numeric_value = value

  let id = analisi.value.w17data[id_parametro][id_time_layouts][id_venue][id_aggregazione].id_w17_data
  let payload = {}
  payload["numeric_value"] = value
  fetchPatch(id, 'data', payload).then((response) => {
    if (!response.ok) {
      toast.open(
        {
          message: 'Errore nel salvataggio',
          type: 'error',
          position: 'top-left'
        }
      )
    } else {
      updateW17(analisi.value.id_w17)
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

function saveTrend(id_parametro, id_time_layouts, id_venue, id_aggregazione) {
  // this func save in some id_trend field but this trend it is actually a field used for the temperature excursion
  let id = analisi.value.w17data[id_parametro][id_time_layouts][id_venue][id_aggregazione].id_w17_data
  let payload = {}
  payload["id_trend"] = analisi.value.w17data[id_parametro][id_time_layouts][id_venue][id_aggregazione].id_trend
  fetchPatch(id, 'data', payload).then((response) => {
    if (!response.ok) {
      toast.open(
        {
          message: 'Errore nel salvataggio',
          type: 'error',
          position: 'top-left'
        }
      )
    } else {
      updateW17(analisi.value.id_w17)
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

function saveField(field) {
  const payload = {}
  payload['id_w17'] = analisi.value.id_w17
  payload['username'] = store.state.username
  payload[field] = analisi.value[field]
  bulkUpdateW17(payload).then((response) => {
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
  }).then((data: W17) => {
    toast.open(
      {
        message: 'Dato salvato',
        type: 'success',
        position: 'top-left'
      }
    )
    analisi.value.last_update = data.last_update
    analisi.value.username = store.state.username
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

function clearValue(x) {
  x.numeric_value = null
  x.cod_staz_meteo = null
  let id = x.id_w17_data
  let payload = {}
  payload["cod_staz_meteo"] = null
  payload["numeric_value"] = null
  fetchPatch(id, 'data', payload).then((response) => {
    if (!response.ok) {
      toast.open(
        {
          message: 'Errore nel salvataggio',
          type: 'error',
          position: 'top-left'
        }
      )
    } else {
      updateW17(analisi.value.id_w17)
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

function execute(action, reroute, message) {
  actions.value[action + 'ing'] = true
  fetchAnalisiAction(action).then(response => {
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
      router.push({ path: `/w17/${data.id_w17}`})
      analisi_id.value = data.id_w17
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

function remove() {
  if (
    confirm('Vuoi davvero cancellare questo bollettino?')
  ) {
    api.fetchBulletinDelete(analisi.value.id_w17, 'w17/bulletins', store).then(response => {
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

function setTab(tab){
  selectedTab.value = tab
}

function openTab (path) {
  window.open(path, "_blank");
}

function getDateFormatted(rawString, time = true) {
  return api.getDateFormatted(rawString, time)
}

function dateToString(date){
  const yy = date.getFullYear()
  const mm = date.getMonth() + 1
  const dd = date.getDate()
  return [yy, (mm>9 ? '' : '0') + mm, (dd>9 ? '' : '0') + dd].join('-')
}

function rearrange(data: any[], key: string, func: ArrayTransformer | null = null) {
  // rearranges the array data in a dictionary
  // aggregating all records with the same key as an array
  // optionally transforming each array with the func function
  let value_data = {}
  data.forEach(record => {
    if (!(record[key] in value_data)) {
      value_data[record[key]] = []
    }
    // console.log('rearrange record', record)
    value_data[record[key]].push(record)
  })
  if (func) {
    Object.keys(value_data).forEach(key => value_data[key] = func(value_data[key]))
  }
  if (!Object.values(value_data).some(item => item != undefined)) value_data = {}
  return value_data
}

</script>

<style>
table {
	text-align: center;
  }
.vertical-center {
	vertical-align : middle;
}
.trashcan {
	height: 25px;
	width: 25px;
}
.button {
	width: 25px;
	height: 25px;
	background: #4E9CAF;
	border-radius: 5px;
	color: white;
	font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}
.small-width {
  width: 10%; 
}
</style>
