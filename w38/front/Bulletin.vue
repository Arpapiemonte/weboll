// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="container-fluid">
    <div class="row justify-content-end sticky-top py-1" style="background-color: #f8f9fa;">
      <!-- https://getbootstrap.com/docs/5.1/components/button-group/ -->
      <div class="btn-group w-auto" role="group" aria-label="Basic outlined example">
        <a class="btn btn-outline-primary" :href="'/api/w38/pdf/' + uvi.id_w38" target="_blank" role="button">
          <img src="~bootstrap-icons/icons/file-earmark-pdf-fill.svg" alt="PDF icon" width="18" height="18"> PDF
        </a>
        <button v-if="uvi.status === '0' && state.username" :disabled="actions.sending" type="button"
          class="btn btn-outline-success" @click="execute_timeout('send', false, 'Bollettino inviato')">
          <span v-if="actions.sending">
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" />
            Sto inviando il bollettino ...
          </span>
          <span v-else>
            <img src="~bootstrap-icons/icons/send-fill.svg" alt="unlock icon" width="18" height="18"> Invia
          </span>
        </button>
        <button v-if="uvi.status === '1' && state.username && uvi.data_emissione.substring(0, 10) === today"
          type="button" class="btn btn-outline-warning" @click="execute('reopen', true, 'Bollettino riaperto')">
          <span v-if="reopening">
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" />
            Sto riaprendo il bollettino ...
          </span>
          <span v-else>
            <img src="~bootstrap-icons/icons/unlock-fill.svg" alt="unlock icon" width="18" height="18"> Riapri
          </span>
        </button>
        <button v-if="uvi.status === '0' && state.username" type="button" class="btn btn-outline-danger"
          @click="remove()">
          <img src="~bootstrap-icons/icons/trash-fill.svg" alt="unlock icon" width="18" height="18"> Elimina
        </button>
      </div>
      <div
        class="btn-group w-auto mt-1 pt-1"
        role="group"
      >
        <div class="form-check form-switch">
          <input
            id="flexSwitchCheckDefault"
            v-model="switch_map"
            class="form-check-input"
            type="checkbox"
          >
          <label
            v-if="switch_map"
            class="form-check-label"
            for="flexSwitchCheckDefault"
          >Disabilita modifiche</label>
          <label
            v-else
            class="form-check-label"
            for="flexSwitchCheckDefault"
          >Abilita modifiche</label>
        </div>
      </div>
    </div>

    <div class="row mb-3">
      <h1>Bollettino Uvi {{ uvi.numero_bollettino }}</h1>

    </div>

    <div v-if="!verifica_bolmeteo_status1" class="alert alert-danger" role="alert">
      Manca ultimo bollettino meteo
    </div>

    <div v-if="!verifica_json_nuvolosita" class="alert alert-danger" role="alert">
      Manca Json copertura nuvolosa
    </div>

    <div v-if="!verifica_data_uviIvrea" class="alert alert-danger" role="alert">
      Mancano dati UVI aggiornati da Ivrea (Inviare Mail)<br>Dati Ivrea dell'ultimo bollettino emesso
    </div>

    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="uvi.status == 1">
            <input id="stato" disabled class="form-control" name="stato" type="text" value="Inviato">
          </span>
          <span v-else>
            <input id="stato" disabled class="form-control" name="stato" type="text" value="Bozza">
          </span>
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_emissione">Data emissione
          <input id="data_emissione" disabled class="form-control" name="data_emissione" type="text"
            :value="getDateFormatted(uvi.data_emissione, false)">
        </label>
      </div>





      <div class="col-md-2 mb-3">
        <label for="last_update">Ultima modifica
          <input id="last_update" disabled class="form-control" name="last_update" type="text"
            :value="getDateFormatted(uvi.last_update)">
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="username">Autore
          <input id="username" disabled class="form-control" name="username" type="text" :value="uvi.username">
        </label>
      </div>
    </div>
    <div class="row mt-3 sticky-top" style="top: 45px;background: white; height:45px;">

      <div class="col-xl-12 col-md-12 mb-3">
        <ul class="nav nav-pills mb-3" role="tablist">
          <li v-for="(value, key) in uvi.w38_data" :key="key" class="nav-item" role="presentation">
            <button class="nav-link" :class="{ 'active': selected_time_layout === parseInt(key.toString()) }"
              type="button" role="tab" @click="selected_time_layout = parseInt(key.toString())">
              {{ tabsDate[key] }}
            </button>
          </li>
        </ul>
      </div>
    </div>
    <div class="row">
      <div class="col-md-5 mb-3">
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">
                Comune
              </th>
              <th scope="col">
                UVI <br>in condizioni di <br>cielo sereno
              </th>
              <th scope="col">
                UVI <br>sulla base della <br>nuvolosità prevista
              </th>
              <th scope="col">
                NUVOLOSITA'
              </th>
            </tr>
          </thead>
          <tbody>
            <tr><!--Alessandria-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['9']['COP_TOT']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['9']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['9']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['9']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['9']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['9']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[9][selected_time_layout]]};`">
                <input v-model="uvicalcolato[9][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['9']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['9']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Asti-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['11']['COP_TOT']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['11']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['11']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['11']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['11']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['11']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[11][selected_time_layout]]};`">
                <input v-model="uvicalcolato[11][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled=true>
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['11']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['11']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Biella-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['1']['COP_TOT']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['1']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['1']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['1']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['1']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['1']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[1][selected_time_layout]]};`">
                <input v-model="uvicalcolato[1][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled=true>
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['1']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['1']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Cuneo-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['28']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['28']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['28']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['28']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['28']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['28']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[28][selected_time_layout]]};`">
                <input v-model="uvicalcolato[28][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled=true>
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['28']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['28']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Novara-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['33']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['33']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['33']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['33']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['33']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['33']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[33][selected_time_layout]]};`">
                <input v-model="uvicalcolato[33][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled=true>
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['33']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['33']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Torino-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['59']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['59']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['59']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['59']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['59']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['59']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[59][selected_time_layout]]};`">
                <input v-model="uvicalcolato[59][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled=true>
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['59']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['59']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Verbania - lago Maggiore-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['63']['UVICS']['0'].id_venue] }} - Lago Maggiore
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['63']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['63']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['63']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['63']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['63']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[63][selected_time_layout]]};`">
                <input v-model="uvicalcolato[63][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled=true>
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['63']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['63']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Vercelli-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['64']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['64']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['64']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['64']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['64']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['64']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[64][selected_time_layout]]};`">
                <input v-model="uvicalcolato[64][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled=true>
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['64']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['64']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--lago sirio - ivrea-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['16']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['16']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['16']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['16']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['16']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['16']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[16][selected_time_layout]]};`">
                <input v-model="uvicalcolato[16][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['16']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['16']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Lago Orta-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['191']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['191']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['191']['UVICS']['0'].numeric_value"
                  type="Number" min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['191']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['191']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['191']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[191][selected_time_layout]]};`">
                <input v-model="uvicalcolato[191][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['191']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['191']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Lago Avigliana-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['192']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['192']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['192']['UVICS']['0'].numeric_value"
                  type="Number" min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['192']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['192']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['192']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[192][selected_time_layout]]};`">
                <input v-model="uvicalcolato[192][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['192']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['192']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Alpi Lepontine-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['89']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['89']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['89']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['89']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['89']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['89']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[89][selected_time_layout]]};`">
                <input v-model="uvicalcolato[89][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled=true>
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['89']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['89']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Alpi Pennine-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['190']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['190']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['190']['UVICS']['0'].numeric_value"
                  type="Number" min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['190']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['190']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['190']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[190][selected_time_layout]]};`">
                <input v-model="uvicalcolato[190][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled=true>
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['190']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['190']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Alpi Graie-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['88']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['88']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['88']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['88']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['88']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['88']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[88][selected_time_layout]]};`">
                <input v-model="uvicalcolato[88][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled=true>
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['88']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['88']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Alpi Cozie-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['87']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['87']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['87']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['87']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['87']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['87']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[87][selected_time_layout]]};`">
                <input v-model="uvicalcolato[87][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled=true>
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['87']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['87']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Alpi Marittime-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['90']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['90']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['90']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['90']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['90']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['90']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[90][selected_time_layout]]};`">
                <input v-model="uvicalcolato[90][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['90']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['90']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Alpi Liguri-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['116']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['116']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['116']['UVICS']['0'].numeric_value"
                  type="Number" min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['116']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['116']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['116']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[116][selected_time_layout]]};`">
                <input v-model="uvicalcolato[116][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['116']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['116']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
            <tr><!--Appennino-->
              <td>
                {{ venue_rif[uvi['w38_data'][selected_time_layout]['91']['UVICS']['0'].id_venue] }}
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['91']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['91']['UVICS']['0'].numeric_value" type="Number"
                  min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['91']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else 
                :style="`background-color: ${colorehtml[uvi['w38_data'][selected_time_layout]['91']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['91']['UVICS']['0'].numeric_value" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td :style="`background-color: ${colorehtml[uvicalcolato[91][selected_time_layout]]};`">
                <input v-model="uvicalcolato[91][selected_time_layout]" type="Number" min="1" max="11" step="1"
                  class="form-control" :disabled="true">
              </td>
              <td>
                <select id="uviValueSelect"
                  v-model="uvi['w38_data'][selected_time_layout]['91']['COP_TOT']['0'].numeric_value"
                  :disabled="readonly" class="form-control"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['91']['COP_TOT']['0'].id_w38_data, 'numeric_value')">
                  <option disabled value="">Seleziona un valore</option>
                  <option v-for="n in uviOptions" :key="n" :value="n">
                    {{ n.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
                  </option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="col-md-5 mb-3">
        <img 
                src="../back/static/images/nuvolosita-uvi.png"
                class="img-fluid"
                style="height: 175px; width: 404px;"
              >
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">
                Pianura
              </th>
              <th scope="col">
                Montagna
              </th>
              <th scope="col">
                ALTA Montagna
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtmlmap[uvi['w38_data'][selected_time_layout]['193']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['193']['UVICS']['0'].numeric_value"
                  type="Number" min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['193']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else
                :style="`background-color: ${colorehtmlmap[uvi['w38_data'][selected_time_layout]['193']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['193']['UVICS']['0'].numeric_value"
                  type="Number" min="1" max="11" step="1" class="form-control" :disabled=true
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['193']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtmlmap[uvi['w38_data'][selected_time_layout]['194']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['194']['UVICS']['0'].numeric_value"
                  type="Number" min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['194']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else
                :style="`background-color: ${colorehtmlmap[uvi['w38_data'][selected_time_layout]['194']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['194']['UVICS']['0'].numeric_value"
                  type="Number" min="1" max="11" step="1" class="form-control" :disabled=true
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['194']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-if="switch_map"
                :style="`background-color: ${colorehtmlmap[uvi['w38_data'][selected_time_layout]['195']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['195']['UVICS']['0'].numeric_value"
                  type="Number" min="1" max="11" step="1" class="form-control" :disabled="readonly"
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['195']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
              <td v-else
                :style="`background-color: ${colorehtmlmap[uvi['w38_data'][selected_time_layout]['195']['UVICS']['0'].numeric_value]};`">
                <input v-model="uvi['w38_data'][selected_time_layout]['195']['UVICS']['0'].numeric_value"
                  type="Number" min="1" max="11" step="1" class="form-control" :disabled=true
                  @change="setUvi(uvi['w38_data'][selected_time_layout]['195']['UVICS']['0'].id_w38_data, 'numeric_value')">
              </td>
            </tr>
          </tbody>
        </table>
        <div>
          <div class="row">
            <div class="col-sm">
              PIANURA
            </div>
            <div class="col-sm">
              MONTAGNA
            </div>
            <div class="col-sm">
              ALTA MONTAGNA
            </div>
          </div>
          <div class="row">
            <div class="col-sm">
              <MapUvi :tl=selected_time_layout :uvi="uvi" />
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-12 mb-3">
        <label for="situazione_evoluzione">Situazione ed evoluzione meteo nei prossimi 3 giorni</label><br>
        <textarea id="situazione_evoluzione" v-model="uvi.situazione_evoluzione" name="situazione_evoluzione" rows="6"
          cols="150" :readonly="readonly"
          @change="saveW38(uvi.situazione_evoluzione, uvi.id_w38, 'situazione_evoluzione')" />
      </div>
      
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'uviBulletin',
  components: {
    MapUvi
  }
}
</script>

<script setup lang="ts">
import { Ref, ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toast-notification'

import api from '../../src/api'
import store from '../../src/store'

import MapUvi from './MapUvi.vue'

import { components } from '../../src/types/weboll'
import type { W38_data } from "../types"

const router = useRouter()
const toast = useToast()

type W38Full = components['schemas']['W38'] & { w38_data: W38_data } & { w38data_set: components['schemas']['W38Data'][] }

type ArrayTransformer = (arr: Array<any>) => any
// reactive properties
let uvi_id = ref('')
let uvi: Ref<W38Full> = ref(
  { "id_w38": 521, "w38data_set": [{ "id_w38_data": 1669, "id_venue": "9", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1670, "id_venue": "9", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1671, "id_venue": "9", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1672, "id_venue": "9", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1673, "id_venue": "9", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1674, "id_venue": "9", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1675, "id_venue": "11", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1676, "id_venue": "11", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1677, "id_venue": "11", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1678, "id_venue": "11", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1679, "id_venue": "11", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1680, "id_venue": "11", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1681, "id_venue": "1", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1682, "id_venue": "1", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1683, "id_venue": "1", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1684, "id_venue": "1", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1685, "id_venue": "1", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1686, "id_venue": "1", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1687, "id_venue": "28", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1688, "id_venue": "28", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1689, "id_venue": "28", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1690, "id_venue": "28", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1691, "id_venue": "28", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1692, "id_venue": "28", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1693, "id_venue": "33", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1694, "id_venue": "33", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1695, "id_venue": "33", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1696, "id_venue": "33", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1697, "id_venue": "33", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1698, "id_venue": "33", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1699, "id_venue": "59", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1700, "id_venue": "59", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1701, "id_venue": "59", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1702, "id_venue": "59", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1703, "id_venue": "59", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1704, "id_venue": "59", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1705, "id_venue": "63", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1706, "id_venue": "63", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1707, "id_venue": "63", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1708, "id_venue": "63", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1709, "id_venue": "63", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1710, "id_venue": "63", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1711, "id_venue": "64", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1712, "id_venue": "64", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1713, "id_venue": "64", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1714, "id_venue": "64", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1715, "id_venue": "64", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1716, "id_venue": "64", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1717, "id_venue": "89", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1718, "id_venue": "89", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1719, "id_venue": "89", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1720, "id_venue": "89", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1721, "id_venue": "89", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1722, "id_venue": "89", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1723, "id_venue": "190", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1724, "id_venue": "190", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1725, "id_venue": "190", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1726, "id_venue": "190", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1727, "id_venue": "190", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1728, "id_venue": "190", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1729, "id_venue": "88", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1730, "id_venue": "88", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1731, "id_venue": "88", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1732, "id_venue": "88", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1733, "id_venue": "88", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1734, "id_venue": "88", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1735, "id_venue": "87", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1736, "id_venue": "87", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1737, "id_venue": "87", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1738, "id_venue": "87", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1739, "id_venue": "87", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1740, "id_venue": "87", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1741, "id_venue": "90", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1742, "id_venue": "90", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1743, "id_venue": "90", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1744, "id_venue": "90", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1745, "id_venue": "90", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1746, "id_venue": "90", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1747, "id_venue": "116", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1748, "id_venue": "116", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1749, "id_venue": "116", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1750, "id_venue": "116", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1751, "id_venue": "116", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1752, "id_venue": "116", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1753, "id_venue": "91", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1754, "id_venue": "91", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1755, "id_venue": "91", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1756, "id_venue": "91", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1757, "id_venue": "91", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1758, "id_venue": "91", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1759, "id_venue": "191", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1760, "id_venue": "191", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1761, "id_venue": "191", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1762, "id_venue": "191", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1763, "id_venue": "191", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1764, "id_venue": "191", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1765, "id_venue": "192", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1766, "id_venue": "192", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1767, "id_venue": "192", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1768, "id_venue": "192", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1769, "id_venue": "192", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1770, "id_venue": "192", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1771, "id_venue": "16", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1772, "id_venue": "16", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1773, "id_venue": "16", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1774, "id_venue": "16", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1775, "id_venue": "16", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1776, "id_venue": "16", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 }, { "id_w38_data": 1777, "id_venue": "193", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1778, "id_venue": "193", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1779, "id_venue": "193", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1780, "id_venue": "194", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1781, "id_venue": "194", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1782, "id_venue": "194", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1783, "id_venue": "195", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1784, "id_venue": "195", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 }, { "id_w38_data": 1785, "id_venue": "195", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 }], "data_emissione": "2025-07-08", "data_validita": "2025-07-09", "numero_bollettino": "256/2025", "situazione_evoluzione": "Giornata odierna caratterizzata ancora da temperature massime in pianura localmente sui 36-37 °C, con temporali a ridosso delle valli e fenomeni isolati su zone di pianura e collina adiacenti. Nel corso della prossima notte un rinforzo nei bassi strati di correnti umide orientali porterà all'innesco di rovesci e temporali nelle prime ore della giornata di domani su zone di pianura e collina centro-settentrionali, che determineranno anche un calo delle temperature. Giornata di sabato quindi all'insegna della variabilità, con nuovi rovesci e temporali sparsi nelle ore pomeridiane. Domenica l'alta pressione lascerà spazio alle nostre latitudini al transito di una perturbazione nordatlantica, con instabilità più diffusa, in particolare sui settori centro-orientali. Al passaggio della perturbazione si attiveranno nel corso della serata venti di foehn nelle valli occidentali che favoriranno un progressivo miglioramento a partire da ovest.", "status": "0", "last_update": "2025-07-08T12:54:29", "username": "aliccoop", "note": "-", "id_w38_parent": null, "w38_data": { "48": { "1": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1681, "id_venue": "1", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1684, "id_venue": "1", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "9": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1669, "id_venue": "9", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1672, "id_venue": "9", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "11": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1675, "id_venue": "11", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1678, "id_venue": "11", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "16": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1771, "id_venue": "16", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1774, "id_venue": "16", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "28": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1687, "id_venue": "28", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1690, "id_venue": "28", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "33": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1693, "id_venue": "33", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1696, "id_venue": "33", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "59": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1699, "id_venue": "59", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1702, "id_venue": "59", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "63": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1705, "id_venue": "63", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1708, "id_venue": "63", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "64": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1711, "id_venue": "64", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1714, "id_venue": "64", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "87": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1735, "id_venue": "87", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1738, "id_venue": "87", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "88": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1729, "id_venue": "88", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1732, "id_venue": "88", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "89": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1717, "id_venue": "89", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1720, "id_venue": "89", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "90": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1741, "id_venue": "90", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1744, "id_venue": "90", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "91": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1753, "id_venue": "91", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1756, "id_venue": "91", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "116": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1747, "id_venue": "116", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1750, "id_venue": "116", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "190": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1723, "id_venue": "190", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1726, "id_venue": "190", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "191": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1759, "id_venue": "191", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1762, "id_venue": "191", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "192": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1765, "id_venue": "192", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1768, "id_venue": "192", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "193": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1777, "id_venue": "193", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } } }, "194": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1780, "id_venue": "194", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } } }, "195": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1783, "id_venue": "195", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 48, "id_parametro": "UVICS", "id_aggregazione": 0 } } } } } }, "66": { "1": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1682, "id_venue": "1", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1685, "id_venue": "1", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "9": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1670, "id_venue": "9", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1673, "id_venue": "9", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "11": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1676, "id_venue": "11", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1679, "id_venue": "11", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "16": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1772, "id_venue": "16", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1775, "id_venue": "16", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "28": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1688, "id_venue": "28", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1691, "id_venue": "28", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "33": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1694, "id_venue": "33", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1697, "id_venue": "33", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "59": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1700, "id_venue": "59", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1703, "id_venue": "59", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "63": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1706, "id_venue": "63", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1709, "id_venue": "63", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "64": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1712, "id_venue": "64", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1715, "id_venue": "64", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "87": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1736, "id_venue": "87", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1739, "id_venue": "87", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "88": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1730, "id_venue": "88", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1733, "id_venue": "88", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "89": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1718, "id_venue": "89", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1721, "id_venue": "89", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "90": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1742, "id_venue": "90", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1745, "id_venue": "90", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "91": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1754, "id_venue": "91", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1757, "id_venue": "91", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "116": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1748, "id_venue": "116", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1751, "id_venue": "116", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "190": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1724, "id_venue": "190", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1727, "id_venue": "190", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "191": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1760, "id_venue": "191", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1763, "id_venue": "191", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "192": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1766, "id_venue": "192", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1769, "id_venue": "192", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "193": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1778, "id_venue": "193", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } } }, "194": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1781, "id_venue": "194", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } } }, "195": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1784, "id_venue": "195", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 66, "id_parametro": "UVICS", "id_aggregazione": 0 } } } } } }, "83": { "1": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1683, "id_venue": "1", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1686, "id_venue": "1", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "9": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1671, "id_venue": "9", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1674, "id_venue": "9", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "11": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1677, "id_venue": "11", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1680, "id_venue": "11", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "16": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1773, "id_venue": "16", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1776, "id_venue": "16", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "28": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1689, "id_venue": "28", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1692, "id_venue": "28", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "33": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1695, "id_venue": "33", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1698, "id_venue": "33", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "59": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1701, "id_venue": "59", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1704, "id_venue": "59", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "63": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1707, "id_venue": "63", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1710, "id_venue": "63", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "64": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1713, "id_venue": "64", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1716, "id_venue": "64", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "87": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1737, "id_venue": "87", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1740, "id_venue": "87", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "88": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1731, "id_venue": "88", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1734, "id_venue": "88", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "89": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1719, "id_venue": "89", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1722, "id_venue": "89", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "90": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1743, "id_venue": "90", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1746, "id_venue": "90", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "91": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1755, "id_venue": "91", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1758, "id_venue": "91", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "116": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1749, "id_venue": "116", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1752, "id_venue": "116", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "190": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1725, "id_venue": "190", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1728, "id_venue": "190", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "191": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1761, "id_venue": "191", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1764, "id_venue": "191", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "192": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1767, "id_venue": "192", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } }, "COP_TOT": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1770, "id_venue": "192", "numeric_value": 1, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "COP_TOT", "id_aggregazione": 0 } } } } }, "193": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1779, "id_venue": "193", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } } }, "194": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1782, "id_venue": "194", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } } }, "195": { "UVICS": { "0": { "_custom": { "type": "reactive", "stateTypeName": "Reactive", "value": { "id_w38_data": 1785, "id_venue": "195", "numeric_value": 5, "id_w38": 521, "id_time_layouts": 83, "id_parametro": "UVICS", "id_aggregazione": 0 } } } } } } } })
let state = ref(store.state)
let ready = ref(false)
let readonly = ref(true)
let today = ref('')
let switch_map = ref(false)

let saving = ref(false)

const props = defineProps({
  id: {
    type: String,
    default: () => ''
  },
})

let colorehtmlmap = ref({
  1: '#4eb400',
  2: '#a0ce00',
  3: '#f7e400',
  4: '#f8b600',
  5: '#f88700',
  6: '#f85900',
  7: '#e82c0e',
  8: '#d8001d',
  9: '#ff0099',
  10: '#b54cff',
  11: '#998cff',
})

let colorehtml = ref({
  1: '#3EA635',
  2: '#3EA635',
  3: '#F8E825',
  4: '#F8E825',
  5: '#F8E825',
  6: '#F08A04',
  7: '#F08A04',
  8: '#F93B21',
  9: '#F93B21',
  10: '#F93B21',
  11: '#B467A3',
})


const base_data_url = computed(() => {
  // Ora restituisce un array fisso con solo i valori desiderati
  //console.log("++++++++++++++++++",import.meta.env.VITE_BASE_DATA_URL)
  return import.meta.env.VITE_BASE_DATA_URL || ""
});


const uviOptions = computed(() => {
  // Ora restituisce un array fisso con solo i valori desiderati
  // return [0.2, 0.4, 0.5, 0.8, 0.9, 1.0];
  return [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];
});

const uvicalcolato = computed(() => {
  let vd = {
    9: {},
    11: {},
    1: {},
    28: {},
    33: {},
    59: {},
    63: {},
    64: {},
    89: {},
    190: {},
    88: {},
    87: {},
    90: {},
    116: {},
    91: {},
    191: {},
    192: {},
    16: {},
  }
  if (ready.value)
    vd[9][48] = multiplyNumbers(uvi.value.w38_data[48][9]['UVICS'][0].numeric_value, uvi.value.w38_data[48][9]['COP_TOT'][0].numeric_value)
    vd[11][48] = multiplyNumbers(uvi.value.w38_data[48][11]['UVICS'][0].numeric_value, uvi.value.w38_data[48][11]['COP_TOT'][0].numeric_value)
    vd[1][48] = multiplyNumbers(uvi.value.w38_data[48][1]['UVICS'][0].numeric_value, uvi.value.w38_data[48][1]['COP_TOT'][0].numeric_value)
    vd[28][48] = multiplyNumbers(uvi.value.w38_data[48][28]['UVICS'][0].numeric_value, uvi.value.w38_data[48][28]['COP_TOT'][0].numeric_value)
    vd[33][48] = multiplyNumbers(uvi.value.w38_data[48][33]['UVICS'][0].numeric_value, uvi.value.w38_data[48][33]['COP_TOT'][0].numeric_value)
    vd[59][48] = multiplyNumbers(uvi.value.w38_data[48][59]['UVICS'][0].numeric_value, uvi.value.w38_data[48][59]['COP_TOT'][0].numeric_value)
    vd[63][48] = multiplyNumbers(uvi.value.w38_data[48][63]['UVICS'][0].numeric_value, uvi.value.w38_data[48][63]['COP_TOT'][0].numeric_value)
    vd[64][48] = multiplyNumbers(uvi.value.w38_data[48][64]['UVICS'][0].numeric_value, uvi.value.w38_data[48][64]['COP_TOT'][0].numeric_value)
    vd[89][48] = multiplyNumbers(uvi.value.w38_data[48][89]['UVICS'][0].numeric_value, uvi.value.w38_data[48][89]['COP_TOT'][0].numeric_value)
    vd[190][48] = multiplyNumbers(uvi.value.w38_data[48][190]['UVICS'][0].numeric_value, uvi.value.w38_data[48][190]['COP_TOT'][0].numeric_value)
    vd[88][48] = multiplyNumbers(uvi.value.w38_data[48][88]['UVICS'][0].numeric_value, uvi.value.w38_data[48][88]['COP_TOT'][0].numeric_value)
    vd[87][48] = multiplyNumbers(uvi.value.w38_data[48][87]['UVICS'][0].numeric_value, uvi.value.w38_data[48][87]['COP_TOT'][0].numeric_value)
    vd[90][48] = multiplyNumbers(uvi.value.w38_data[48][90]['UVICS'][0].numeric_value, uvi.value.w38_data[48][90]['COP_TOT'][0].numeric_value)
    vd[116][48] = multiplyNumbers(uvi.value.w38_data[48][116]['UVICS'][0].numeric_value, uvi.value.w38_data[48][116]['COP_TOT'][0].numeric_value)
    vd[91][48] = multiplyNumbers(uvi.value.w38_data[48][91]['UVICS'][0].numeric_value, uvi.value.w38_data[48][91]['COP_TOT'][0].numeric_value)
    vd[191][48] = multiplyNumbers(uvi.value.w38_data[48][191]['UVICS'][0].numeric_value, uvi.value.w38_data[48][191]['COP_TOT'][0].numeric_value)
    vd[192][48] = multiplyNumbers(uvi.value.w38_data[48][192]['UVICS'][0].numeric_value, uvi.value.w38_data[48][192]['COP_TOT'][0].numeric_value)
    vd[16][48] = multiplyNumbers(uvi.value.w38_data[48][16]['UVICS'][0].numeric_value, uvi.value.w38_data[48][16]['COP_TOT'][0].numeric_value)

    vd[9][66] = multiplyNumbers(uvi.value.w38_data[66][9]['UVICS'][0].numeric_value, uvi.value.w38_data[66][9]['COP_TOT'][0].numeric_value)
    vd[11][66] = multiplyNumbers(uvi.value.w38_data[66][11]['UVICS'][0].numeric_value, uvi.value.w38_data[66][11]['COP_TOT'][0].numeric_value)
    vd[1][66] = multiplyNumbers(uvi.value.w38_data[66][1]['UVICS'][0].numeric_value, uvi.value.w38_data[66][1]['COP_TOT'][0].numeric_value)
    vd[28][66] = multiplyNumbers(uvi.value.w38_data[66][28]['UVICS'][0].numeric_value, uvi.value.w38_data[66][28]['COP_TOT'][0].numeric_value)
    vd[33][66] = multiplyNumbers(uvi.value.w38_data[66][33]['UVICS'][0].numeric_value, uvi.value.w38_data[66][33]['COP_TOT'][0].numeric_value)
    vd[59][66] = multiplyNumbers(uvi.value.w38_data[66][59]['UVICS'][0].numeric_value, uvi.value.w38_data[66][59]['COP_TOT'][0].numeric_value)
    vd[63][66] = multiplyNumbers(uvi.value.w38_data[66][63]['UVICS'][0].numeric_value, uvi.value.w38_data[66][63]['COP_TOT'][0].numeric_value)
    vd[64][66] = multiplyNumbers(uvi.value.w38_data[66][64]['UVICS'][0].numeric_value, uvi.value.w38_data[66][64]['COP_TOT'][0].numeric_value)
    vd[89][66] = multiplyNumbers(uvi.value.w38_data[66][89]['UVICS'][0].numeric_value, uvi.value.w38_data[66][89]['COP_TOT'][0].numeric_value)
    vd[190][66] = multiplyNumbers(uvi.value.w38_data[66][190]['UVICS'][0].numeric_value, uvi.value.w38_data[66][190]['COP_TOT'][0].numeric_value)
    vd[88][66] = multiplyNumbers(uvi.value.w38_data[66][88]['UVICS'][0].numeric_value, uvi.value.w38_data[66][88]['COP_TOT'][0].numeric_value)
    vd[87][66] = multiplyNumbers(uvi.value.w38_data[66][87]['UVICS'][0].numeric_value, uvi.value.w38_data[66][87]['COP_TOT'][0].numeric_value)
    vd[90][66] = multiplyNumbers(uvi.value.w38_data[66][90]['UVICS'][0].numeric_value, uvi.value.w38_data[66][90]['COP_TOT'][0].numeric_value)
    vd[116][66] = multiplyNumbers(uvi.value.w38_data[66][116]['UVICS'][0].numeric_value, uvi.value.w38_data[66][116]['COP_TOT'][0].numeric_value)
    vd[91][66] = multiplyNumbers(uvi.value.w38_data[66][91]['UVICS'][0].numeric_value, uvi.value.w38_data[66][91]['COP_TOT'][0].numeric_value)
    vd[191][66] = multiplyNumbers(uvi.value.w38_data[66][191]['UVICS'][0].numeric_value, uvi.value.w38_data[66][191]['COP_TOT'][0].numeric_value)
    vd[192][66] = multiplyNumbers(uvi.value.w38_data[66][192]['UVICS'][0].numeric_value, uvi.value.w38_data[66][192]['COP_TOT'][0].numeric_value)
    vd[16][66] = multiplyNumbers(uvi.value.w38_data[66][16]['UVICS'][0].numeric_value, uvi.value.w38_data[66][16]['COP_TOT'][0].numeric_value)

    vd[9][83] = multiplyNumbers(uvi.value.w38_data[83][9]['UVICS'][0].numeric_value, uvi.value.w38_data[83][9]['COP_TOT'][0].numeric_value)
    vd[11][83] = multiplyNumbers(uvi.value.w38_data[83][11]['UVICS'][0].numeric_value, uvi.value.w38_data[83][11]['COP_TOT'][0].numeric_value)
    vd[1][83] = multiplyNumbers(uvi.value.w38_data[83][1]['UVICS'][0].numeric_value, uvi.value.w38_data[83][1]['COP_TOT'][0].numeric_value)
    vd[28][83] = multiplyNumbers(uvi.value.w38_data[83][28]['UVICS'][0].numeric_value, uvi.value.w38_data[83][28]['COP_TOT'][0].numeric_value)
    vd[33][83] = multiplyNumbers(uvi.value.w38_data[83][33]['UVICS'][0].numeric_value, uvi.value.w38_data[83][33]['COP_TOT'][0].numeric_value)
    vd[59][83] = multiplyNumbers(uvi.value.w38_data[83][59]['UVICS'][0].numeric_value, uvi.value.w38_data[83][59]['COP_TOT'][0].numeric_value)
    vd[63][83] = multiplyNumbers(uvi.value.w38_data[83][63]['UVICS'][0].numeric_value, uvi.value.w38_data[83][63]['COP_TOT'][0].numeric_value)
    vd[64][83] = multiplyNumbers(uvi.value.w38_data[83][64]['UVICS'][0].numeric_value, uvi.value.w38_data[83][64]['COP_TOT'][0].numeric_value)
    vd[89][83] = multiplyNumbers(uvi.value.w38_data[83][89]['UVICS'][0].numeric_value, uvi.value.w38_data[83][89]['COP_TOT'][0].numeric_value)
    vd[190][83] = multiplyNumbers(uvi.value.w38_data[83][190]['UVICS'][0].numeric_value, uvi.value.w38_data[83][190]['COP_TOT'][0].numeric_value)
    vd[88][83] = multiplyNumbers(uvi.value.w38_data[83][88]['UVICS'][0].numeric_value, uvi.value.w38_data[83][88]['COP_TOT'][0].numeric_value)
    vd[87][83] = multiplyNumbers(uvi.value.w38_data[83][87]['UVICS'][0].numeric_value, uvi.value.w38_data[83][87]['COP_TOT'][0].numeric_value)
    vd[90][83] = multiplyNumbers(uvi.value.w38_data[83][90]['UVICS'][0].numeric_value, uvi.value.w38_data[83][90]['COP_TOT'][0].numeric_value)
    vd[116][83] = multiplyNumbers(uvi.value.w38_data[83][116]['UVICS'][0].numeric_value, uvi.value.w38_data[83][116]['COP_TOT'][0].numeric_value)
    vd[91][83] = multiplyNumbers(uvi.value.w38_data[83][91]['UVICS'][0].numeric_value, uvi.value.w38_data[83][91]['COP_TOT'][0].numeric_value)
    vd[191][83] = multiplyNumbers(uvi.value.w38_data[83][191]['UVICS'][0].numeric_value, uvi.value.w38_data[83][191]['COP_TOT'][0].numeric_value)
    vd[192][83] = multiplyNumbers(uvi.value.w38_data[83][192]['UVICS'][0].numeric_value, uvi.value.w38_data[83][192]['COP_TOT'][0].numeric_value)
    vd[16][83] = multiplyNumbers(uvi.value.w38_data[83][16]['UVICS'][0].numeric_value, uvi.value.w38_data[83][16]['COP_TOT'][0].numeric_value)
  //console.log(vd[9][48],uvi.value.w38_data[48][9]['UVICS'][0].numeric_value, uvi.value.w38_data[48][9]['COP_TOT'][0].numeric_value)
  return vd
})

let venue_rif = ref({
  9: 'Alessandria',
  11: 'Asti',
  1: 'Biella',
  28: 'Cuneo',
  33: 'Novara',
  59: 'Torino',
  63: 'Verbania',
  64: 'Vercelli',
  89: 'Alpi Lepontine',
  190: 'Alpi Pennine',
  88: 'Alpi Graie',
  87: 'Alpi Cozie',
  90: 'Alpi Marittime',
  116: 'Alpi Liguri',
  91: 'Appennino',
  191: 'Lago Orta',
  192: 'Laghi di Avigliana',
  16: 'Ivrea',
  193: 'Pianura',
  194: 'Montagna',
  195: 'Alta montagna'
})

let verifica_bolmeteo_status1 = ref(false)
let verifica_json_nuvolosita = ref(false)
let verifica_data_uviIvrea = ref(false)



let selected_time_layout = ref(48)

let tabsDate = ref({
  48: '',
  66: '',
  83: '',
})

function multiplyNumbers(num1: number, num2: number): number {
  let valore = Math.round(num1 * num2);
  if (valore > 11)
    valore = 11
  if (valore < 1)
    valore = 1
  return valore;
}

function createTabsDate() {
  let today = dateToString(new Date(uvi.value.data_emissione))
  let tomorrow = dateToString(new Date(new Date(uvi.value.data_emissione).setDate(new Date(uvi.value.data_emissione).getDate() + 1)))
  let afterTomorrow = dateToString(new Date(new Date(uvi.value.data_emissione).setDate(new Date(uvi.value.data_emissione).getDate() + 2)))

  tabsDate.value = {
    48: `${today}`,
    66: `${tomorrow}`,
    83: `${afterTomorrow}`,
  }
}

let actions = ref({
  sending: false,
  reopening: false,
})

onMounted(async () => {
  uvi_id.value = props.id
  await fetchData()
  await fetchDataBolmeteo()
  await fetchDataJsonNuvolosita()
  await fetchDataIvrea()
})

async function fetchData() {
  today.value = dateToString(new Date())
  ready.value = false
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  fetchUvi(uvi_id.value).then((response: { ok: any; status: any; json: () => any }) => {
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
  }).then(async (data: any) => {

    uvi.value = data
    readonly.value = (uvi.value.status === '1' || uvi.value.status === '2' || !state.value.username)

    let rearrangeuvidata = rearrange(
      uvi.value['w38data_set'],
      "id_time_layouts",
      pippo => rearrange(pippo, "id_venue",
        pippo2 => rearrange(pippo2, "id_parametro",
          pippo3 => rearrange(pippo3, "id_aggregazione", (arr: any[]) => arr[0])))
    )
    uvi.value['w38_data'] = rearrangeuvidata
    createTabsDate()
    ready.value = true
  }).catch((error: any) => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

async function fetchDataBolmeteo() {
  today.value = dateToString(new Date())
  //ready.value = false
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  fetchBolmeteo().then((response: { ok: any; status: any; json: () => any }) => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero dei bollettino meteo`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(async (data: { [x: string]: { status: any }[] }) => {
    // verifico che ci sia ultimo bllettino meteo con status =1
    const data_oggi = today.value
    const last_bolmeteo_data = data['results'][0].start_valid_time.substring(0,10);
    const last_bolmeteo_status = data['results'][0].status
    if (last_bolmeteo_data == data_oggi){
      if (last_bolmeteo_status == "1"){
        verifica_bolmeteo_status1.value=true
      }
    }
  }).catch((error: any) => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

async function fetchDataJsonNuvolosita() {
  today.value = dateToString(new Date())
  let day = today.value.substring(8,10)
  let year = today.value.substring(0,4)
  let mounth = today.value.substring(5,7)
  let datenow = year + mounth + day
  let url=base_data_url.value+"/uvi/"+datenow+"_cop_tot.json"
  //let url=base_data_url.value+"/uvi/yyyymmgg_cop_tot.json"
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  fetchjson(url).then((response: { ok: any; status: any; json: () => any }) => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero del json della nuvolosità`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(async (data: any) => {
    verifica_json_nuvolosita.value=true
  }).catch((error: any) => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

async function fetchDataIvrea() {
  today.value = dateToString(new Date())
  //ready.value = false
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  fetchDatiIvrea().then((response: { ok: any; status: any; json: () => any }) => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero dei dati di ivrea`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(async (data: { [x: string]: { status: any }[] }) => {
    // verifico che la data emissione dati ivrea si quella di oggi
    if (Object.keys(data).length > 0){
      const data_oggi = today.value
      const last_datiuvi_data = data[0].data_emissione.substring(0,10);
      if (last_datiuvi_data == data_oggi){
          verifica_data_uviIvrea.value=true
      }
    }
  }).catch((error: any) => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

async function fetchUvi(id: string | number) {
  const response = await fetch('/api/w38/bulletins/' + id + '/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}


async function fetchBolmeteo() {
  const response = await fetch('/api/w05/bulletins/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchDatiIvrea() {
  const response = await fetch('/api/w38/dataIvrea/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}


async function fetchjson (url:any){
  const response = await  fetch(url, {
    headers: {
      accept: 'application/json'
    }
  })
  // console.log('response=',response)
  return response;
}


function getDateFormatted(rawString: string, time = true) {
  return api.getDateFormatted(rawString, time)
}

function saveW38(newValue: any, id_w38: any, campo: any) {
  const payload = {}
  if (campo) {
    payload[campo] = newValue
  }
  payload['id_w38'] = id_w38
  payload['username'] = store.state.username
  bulkUpdateW38(payload).then((response: { ok: any; json: () => any }) => {
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
  }).then((data: { last_update: any }) => {
    toast.open(
      {
        message: 'Dato salvato',
        type: 'success',
        position: 'top-left'
      }
    )
    uvi.value.last_update = data.last_update
    uvi.value.username = (store.state.username || "")
  }).catch((error: any) => {
    toast.open(
      {
        message: `Errore di comunicazione: ${error}`,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}


function saveW38Data(newValue: any, id_w38_data: any, campo: string) {
  let myIdW38 = uvi.value.w38data_set.find((w38data: { id_w38_data: any }) => {
    return w38data.id_w38_data === id_w38_data
  })
  if (myIdW38) {
    const payload = {}
    //myIdW38[campo] = parseInt(newValue)
    myIdW38[campo] = newValue
    payload[campo] = newValue
    fetchPatch(myIdW38.id_w38_data, 'data', payload).then((response: { ok: any }) => {
      if (!response.ok) {
        toast.open(
          {
            message: 'Errore nel salvataggio',
            type: 'error',
            position: 'top-left'
          }
        )
      } else {
        saveW38(null, uvi.value.id_w38, null)
      }
    }).catch((error: any) => {
      toast.open(
        {
          message: `Errore di comunicazione: ${error}`,
          type: 'error',
          position: 'top-left'
        }
      )
    })
  }
}

function remove() {
  if (
    confirm('Vuoi davvero cancellare questo bollettino?')
  ) {
    api.fetchBulletinDelete(uvi_id.value, 'w38/bulletins', store).then((response: { ok: any; status: any }) => {
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
    }).catch((error: any) => {
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

function setUvi(id_w38_data: any, campo: any) {
  if (window.event && window.event.target !== null) {
    let new_value = (window.event.target as HTMLInputElement).value
    saveW38Data(new_value, id_w38_data, campo)
  }
}

async function fetchUviAction(action: any) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w38/bulletins/${uvi_id.value}/${action}/`
  )
  return response
}

function execute_timeout(action: string, reroute: any, message: any) {
  // console.log("inizio execute_timeout")
  if (saving.value) {
    console.log("saving è true faccio partire timeout")
    setTimeout(() => {
      console.log("aspetto 1 secondo finchè non finisce il salvataggio in corso")
      execute_timeout(action, reroute, message)
    }, 1000);
  } else {
    console.log("saving è false lancio execute")
    execute(action, reroute, message)
  }
  // console.log("fine execute_timeout")
}

function execute(action: string, reroute: any, message: any) {
  actions.value[action + 'ing'] = true
  fetchUviAction(action).then((response: { ok: any; json: () => any; status: any }) => {
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
  }).then((data: { id_w38: any }) => {
    toast.open(
      {
        message: message,
        type: 'success',
        position: 'top-left'
      }
    )
    if (reroute) {
      //router.push({ path: `/w38/${data.id_w38}` })
      router.push({ path: `/w38/${data.id_w38}` })
      uvi_id.value = data.id_w38
      fetchData()
    } else {
      router.push({ path: `/w38/` })
      fetchData()
    }
  }).catch((error: any) => {
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



async function fetchPatch(id: any, endpoint: string, payload: {}) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w38/${endpoint}/${id}/`,
    {
      method: 'PATCH',
      body: JSON.stringify(payload)
    }
  )
  return response
}

async function bulkUpdateW38(payload: {}) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w38/bulletins/bulk_update/`,
    {
      method: 'POST',
      body: JSON.stringify(payload)
    }
  )
  return response
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
    Object.keys(value_data).forEach((key: string | number) => value_data[key] = func(value_data[key]))
  }
  if (!Object.values(value_data).some((item: undefined) => item != undefined)) value_data = {}
  return value_data
}

function dateToString(date: { getFullYear: () => any; getMonth: () => number; getDate: () => any }) {
  const yy = date.getFullYear()
  const mm = date.getMonth() + 1
  const dd = date.getDate()
  return [yy, (mm > 9 ? '' : '0') + mm, (dd > 9 ? '' : '0') + dd].join('-')
}

</script>
