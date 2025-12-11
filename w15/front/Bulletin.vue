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
          :href="'/api/w15/pdf/' + parchi.id_w15"
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
          v-if="parchi.status === '0' && state.username"
          :disabled="actions.sending"
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
          v-if="parchi.status === '1' && state.username && parchi.data_emissione.substring(0, 10) === today"
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
          v-if="parchi.status === '0' && state.username"
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
      <h1>Parchi Reali {{ parchi.id_w15 }}</h1>
      <!--
      <div
        class="alert alert-danger"
      >
        Ci sono dei campi incompleti
      </div>-->
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="parchi.status === '1'">
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
            :value="getDateFormatted(parchi.data_emissione, false)"
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
            :value="getDateFormatted(parchi.last_update)"
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
            :value="parchi.username"
          >
        </label>
      </div>
    </div>
    <div class="row mt-3 sticky-top">
      <div class="col-xl-12 col-md-12 mb-3">
        <ul
          class="nav nav-pills mb-3"
          role="tablist"
        >
          <li
            v-for="(value, key) in parchi.w15_data"
            :key="key"
            class="nav-item"
            role="presentation"
          >
            <button
              class="nav-link"
              :class="{'active' : selected_venue === parseInt(key.toString())}"
              type="button"
              role="tab"
              @click="selected_venue = parseInt(key.toString())"
            >
              {{ venue_rif[key] }}
            </button>
          </li>
        </ul>
      </div>
    </div>
    <div class="row">
      <div class="col-md-10 mb-3">
        <table
          border-collapse="collapse"
          class="table table-striped"
        >
          <thead>
            <tr>
              <th
                colspan="1"
                rowspan="2"
                scope="col"
                class="text-center align-middle"
              >
                Parametro
              </th>
              <th
                colspan="1"
                scope="col"
                class="text-center"
              >
                {{ tabsDate[0] }}
              </th>
              <th
                colspan="2"
                scope="col"
                class="text-center"
              >
                {{ tabsDate[1] }}
              </th>
              <th
                colspan="2"
                scope="col"
                class="text-center"
              >
                {{ tabsDate[2] }}
              </th>
            </tr>
            <tr>
              <th
                scope="col"
              >
                Pomeriggio
              </th>
              <th
                scope="col"
              >
                Mattino
              </th>
              <th
                scope="col"
              >
                Pomeriggio
              </th>
              <th
                scope="col"
              >
                Mattino
              </th>
              
              <th
                scope="col"
              >
                Pomeriggio
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="venue_terma.includes(selected_venue)">
              <td
                colspan="1"
                
                class="text-center"
              > 
                Temp. Max
              </td>
              <td
                colspan="1"
                
                class="text-center"
              >
                <input
                  v-model="parchi['w15_data'][selected_venue]['48']['TERMA'][0].numeric_value"
                  type="Number"
                  step="1"
                  max="50"
                  class="form-control"
                  title="Temperatura massima"
                  :disabled="readonly"
                  @change="setParchi(parchi['w15_data'][selected_venue]['48']['TERMA'][0].id_w15_data, 'numeric_value')"
                >
              </td>
              <td
                colspan="1"
                
                class="text-center"
              > 
                -
              </td>
              <td
                colspan="1"
                
                class="text-center"
              > 
                <input
                  v-model="parchi['w15_data'][selected_venue]['65']['TERMA'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Temperatura massima"
                  :disabled="readonly"
                  @change="setParchi(parchi['w15_data'][selected_venue]['65']['TERMA'][0].id_w15_data, 'numeric_value')"
                >
              </td>
              <td
                colspan="1"
                
                class="text-center"
              > 
                -
              </td>
              <td
                colspan="1"
                
                class="text-center"
              > 
                <input
                  v-model="parchi['w15_data'][selected_venue]['82']['TERMA'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Temperatura massima"
                  :disabled="readonly"
                  @change="setParchi(parchi['w15_data'][selected_venue]['82']['TERMA'][0].id_w15_data, 'numeric_value')"
                >
              </td>
            </tr>
            <tr v-else>                    
              <td
                colspan="1"
                
                class="text-center"
              > 
                Tempo prevalente
              </td>
              <!-- ciclo per ogni tl per costruire le celle td-->
              <td
                v-for="tl in tl_12h"
                :key="tl"
                class="text-center"
              >
                <select
                  :value="parchi['w15_data'][selected_venue][tl]['SKY_CONDIT'][0].numeric_value"
                  :disabled="readonly"
                  class="form-select col"
                  @change="setParchi(parchi['w15_data'][selected_venue][tl]['SKY_CONDIT'][0].id_w15_data, 'numeric_value')"
                >
                  <option
                    v-for="(d, j) in icons"
                    :key="j"
                    :value="d.id_sky_condition"
                  >
                    {{ d.description_ita }}
                  </option>
                </select>
              </td>
            </tr>
            <tr v-if="venue_terma.includes(selected_venue)"> 
              <td
                colspan="1"
                
                class="text-center"
              > 
                Temp. Min
              </td>
              <td
                colspan="1"
                
                class="text-center"
              > 
                -
              </td>
              <td
                colspan="1"
                
                class="text-center"
              > 
                <input
                  v-model="parchi['w15_data'][selected_venue]['64']['TERMA'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Temperatura minima"
                  :disabled="readonly"
                  @change="setParchi(parchi['w15_data'][selected_venue]['64']['TERMA'][0].id_w15_data, 'numeric_value')"
                >
              </td>
              <td
                colspan="1"
                
                class="text-center"
              > 
                -
              </td>
              <td
                colspan="1"
                
                class="text-center"
              > 
                <input
                  v-model="parchi['w15_data'][selected_venue]['81']['TERMA'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Temperatura minima"
                  :disabled="readonly"
                  @change="setParchi(parchi['w15_data'][selected_venue]['81']['TERMA'][0].id_w15_data, 'numeric_value')"
                >
              </td>
              <td
                colspan="1"
                
                class="text-center"
              > 
                -
              </td>
            </tr> 
            <tr v-if="venue_terma.includes(selected_venue)">
              <td
                colspan="1"
                
                class="text-center"
              >   
                Venti
              </td> 
              <!-- 48 ha colspan1, 66 e 83 hanno colspan2 perchè mattino e pomeriggio -->
              <td
                colspan="1"
                
                class="text-center"
              > 
                <select
                  :value="parchi['w15_data'][selected_venue]['48']['WIND_CLASS'][0].numeric_value"
                  :disabled="readonly"
                  class="form-select col"
                  @change="setParchi(parchi['w15_data'][selected_venue]['48']['WIND_CLASS'][0].id_w15_data, 'numeric_value')"
                >
                  <option
                    v-for="(d, j) in vento_rif"
                    :key="j"
                    :value="d.numeric_value"
                  >
                    {{ d.description }}
                  </option>
                </select>
              </td>
              <td
                v-for="tl in [66, 83]"
                :key="tl"
                colspan="2"
                class="text-center"
              > 
                <select
                  :value="parchi['w15_data'][selected_venue][tl]['WIND_CLASS'][0].numeric_value"
                  :disabled="readonly"
                  class="form-select col"
                  @change="setParchi(parchi['w15_data'][selected_venue][tl]['WIND_CLASS'][0].id_w15_data, 'numeric_value')"
                >
                  <option
                    v-for="(d, j) in vento_rif"
                    :key="j"
                    :value="d.numeric_value"
                  >
                    {{ d.description }}
                  </option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
      </div>  <!--col-->
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'ParchiBulletin',
}
</script>

<script setup lang="ts">
import { Ref, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toast-notification'

import api from '../../src/api'
import store from '../../src/store'

import { components } from '../../src/types/weboll'
import type { W15_data } from "../types"

const router = useRouter()
const toast = useToast()

type W15Full = components['schemas']['W15'] & { w15_data: W15_data } & { w15data_set: components['schemas']['W15Data'][] } 

type ArrayTransformer = (arr: Array<any>) => any
// reactive properties
let parchi_id = ref('')
let parchi: Ref<W15Full> = ref({"id_w15":238,"w15data_set":[{"id_w15_data":207100,"id_venue":"165","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207101,"id_venue":"165","numeric_value":21,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207102,"id_venue":"165","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":66,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207103,"id_venue":"165","numeric_value":23,"id_trend":1,"id_w15":238,"id_time_layouts":64,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207104,"id_venue":"165","numeric_value":5,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"TERMA","id_aggregazione":327},{"id_w15_data":207105,"id_venue":"165","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":83,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207106,"id_venue":"165","numeric_value":24,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207107,"id_venue":"165","numeric_value":6,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"TERMA","id_aggregazione":327},{"id_w15_data":207108,"id_venue":"59","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207109,"id_venue":"59","numeric_value":21,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207110,"id_venue":"59","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":66,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207111,"id_venue":"59","numeric_value":23,"id_trend":1,"id_w15":238,"id_time_layouts":64,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207112,"id_venue":"59","numeric_value":5,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"TERMA","id_aggregazione":327},{"id_w15_data":207113,"id_venue":"59","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":83,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207114,"id_venue":"59","numeric_value":24,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207115,"id_venue":"59","numeric_value":6,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"TERMA","id_aggregazione":327},{"id_w15_data":207116,"id_venue":"55","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207117,"id_venue":"55","numeric_value":21,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207118,"id_venue":"55","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":66,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207119,"id_venue":"55","numeric_value":23,"id_trend":1,"id_w15":238,"id_time_layouts":64,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207120,"id_venue":"55","numeric_value":5,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"TERMA","id_aggregazione":327},{"id_w15_data":207121,"id_venue":"55","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":83,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207122,"id_venue":"55","numeric_value":24,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207123,"id_venue":"55","numeric_value":6,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"TERMA","id_aggregazione":327},{"id_w15_data":207124,"id_venue":"157","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207125,"id_venue":"157","numeric_value":21,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207126,"id_venue":"157","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":66,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207127,"id_venue":"157","numeric_value":23,"id_trend":1,"id_w15":238,"id_time_layouts":64,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207128,"id_venue":"157","numeric_value":5,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"TERMA","id_aggregazione":327},{"id_w15_data":207129,"id_venue":"157","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":83,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207130,"id_venue":"157","numeric_value":24,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207131,"id_venue":"157","numeric_value":6,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"TERMA","id_aggregazione":327},{"id_w15_data":207132,"id_venue":"158","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207133,"id_venue":"158","numeric_value":21,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207134,"id_venue":"158","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":66,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207135,"id_venue":"158","numeric_value":23,"id_trend":1,"id_w15":238,"id_time_layouts":64,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207136,"id_venue":"158","numeric_value":5,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"TERMA","id_aggregazione":327},{"id_w15_data":207137,"id_venue":"158","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":83,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207138,"id_venue":"158","numeric_value":24,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207139,"id_venue":"158","numeric_value":6,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"TERMA","id_aggregazione":327},{"id_w15_data":207140,"id_venue":"159","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207141,"id_venue":"159","numeric_value":21,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207142,"id_venue":"159","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":66,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207143,"id_venue":"159","numeric_value":23,"id_trend":1,"id_w15":238,"id_time_layouts":64,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207144,"id_venue":"159","numeric_value":5,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"TERMA","id_aggregazione":327},{"id_w15_data":207145,"id_venue":"159","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":83,"id_parametro":"WIND_CLASS","id_aggregazione":0},{"id_w15_data":207146,"id_venue":"159","numeric_value":24,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"TERMA","id_aggregazione":328},{"id_w15_data":207147,"id_venue":"159","numeric_value":6,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"TERMA","id_aggregazione":327},{"id_w15_data":207148,"id_venue":"166","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"SKY_CONDIT","id_aggregazione":0},{"id_w15_data":207149,"id_venue":"166","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":64,"id_parametro":"SKY_CONDIT","id_aggregazione":0},{"id_w15_data":207150,"id_venue":"166","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":65,"id_parametro":"SKY_CONDIT","id_aggregazione":0},{"id_w15_data":207151,"id_venue":"166","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"SKY_CONDIT","id_aggregazione":0},{"id_w15_data":207152,"id_venue":"166","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"SKY_CONDIT","id_aggregazione":0},{"id_w15_data":207153,"id_venue":"170","numeric_value":22,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"SKY_CONDIT","id_aggregazione":0},{"id_w15_data":207154,"id_venue":"170","numeric_value":16,"id_trend":null,"id_w15":238,"id_time_layouts":64,"id_parametro":"SKY_CONDIT","id_aggregazione":0},{"id_w15_data":207155,"id_venue":"170","numeric_value":22,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"SKY_CONDIT","id_aggregazione":0},{"id_w15_data":207156,"id_venue":"170","numeric_value":16,"id_trend":null,"id_w15":238,"id_time_layouts":81,"id_parametro":"SKY_CONDIT","id_aggregazione":0},{"id_w15_data":207157,"id_venue":"170","numeric_value":22,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"SKY_CONDIT","id_aggregazione":0}],"seq_num":126,"data_emissione":"2024-02-17T01:00:00","status":"1","last_update":"2024-01-29T16:16:35.065639","username":"aliccoop","id_w15_parent":null,"w15_data":{"55":{"48":{"WIND_CLASS":[{"id_w15_data":207116,"id_venue":"55","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"WIND_CLASS","id_aggregazione":0}],"TERMA":[{"id_w15_data":207117,"id_venue":"55","numeric_value":21,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"TERMA","id_aggregazione":328}]},"64":{"TERMA":[{"id_w15_data":207119,"id_venue":"55","numeric_value":23,"id_trend":1,"id_w15":238,"id_time_layouts":64,"id_parametro":"TERMA","id_aggregazione":328}]},"65":{"TERMA":[{"id_w15_data":207120,"id_venue":"55","numeric_value":5,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"TERMA","id_aggregazione":327}]},"66":{"WIND_CLASS":[{"id_w15_data":207118,"id_venue":"55","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":66,"id_parametro":"WIND_CLASS","id_aggregazione":0}]},"81":{"TERMA":[{"id_w15_data":207122,"id_venue":"55","numeric_value":24,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"TERMA","id_aggregazione":328}]},"82":{"TERMA":[{"id_w15_data":207123,"id_venue":"55","numeric_value":6,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"TERMA","id_aggregazione":327}]},"83":{"WIND_CLASS":[{"id_w15_data":207121,"id_venue":"55","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":83,"id_parametro":"WIND_CLASS","id_aggregazione":0}]}},"59":{"48":{"WIND_CLASS":[{"id_w15_data":207108,"id_venue":"59","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"WIND_CLASS","id_aggregazione":0}],"TERMA":[{"id_w15_data":207109,"id_venue":"59","numeric_value":21,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"TERMA","id_aggregazione":328}]},"64":{"TERMA":[{"id_w15_data":207111,"id_venue":"59","numeric_value":23,"id_trend":1,"id_w15":238,"id_time_layouts":64,"id_parametro":"TERMA","id_aggregazione":328}]},"65":{"TERMA":[{"id_w15_data":207112,"id_venue":"59","numeric_value":5,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"TERMA","id_aggregazione":327}]},"66":{"WIND_CLASS":[{"id_w15_data":207110,"id_venue":"59","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":66,"id_parametro":"WIND_CLASS","id_aggregazione":0}]},"81":{"TERMA":[{"id_w15_data":207114,"id_venue":"59","numeric_value":24,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"TERMA","id_aggregazione":328}]},"82":{"TERMA":[{"id_w15_data":207115,"id_venue":"59","numeric_value":6,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"TERMA","id_aggregazione":327}]},"83":{"WIND_CLASS":[{"id_w15_data":207113,"id_venue":"59","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":83,"id_parametro":"WIND_CLASS","id_aggregazione":0}]}},"157":{"48":{"WIND_CLASS":[{"id_w15_data":207124,"id_venue":"157","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"WIND_CLASS","id_aggregazione":0}],"TERMA":[{"id_w15_data":207125,"id_venue":"157","numeric_value":21,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"TERMA","id_aggregazione":328}]},"64":{"TERMA":[{"id_w15_data":207127,"id_venue":"157","numeric_value":23,"id_trend":1,"id_w15":238,"id_time_layouts":64,"id_parametro":"TERMA","id_aggregazione":328}]},"65":{"TERMA":[{"id_w15_data":207128,"id_venue":"157","numeric_value":5,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"TERMA","id_aggregazione":327}]},"66":{"WIND_CLASS":[{"id_w15_data":207126,"id_venue":"157","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":66,"id_parametro":"WIND_CLASS","id_aggregazione":0}]},"81":{"TERMA":[{"id_w15_data":207130,"id_venue":"157","numeric_value":24,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"TERMA","id_aggregazione":328}]},"82":{"TERMA":[{"id_w15_data":207131,"id_venue":"157","numeric_value":6,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"TERMA","id_aggregazione":327}]},"83":{"WIND_CLASS":[{"id_w15_data":207129,"id_venue":"157","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":83,"id_parametro":"WIND_CLASS","id_aggregazione":0}]}},"158":{"48":{"WIND_CLASS":[{"id_w15_data":207132,"id_venue":"158","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"WIND_CLASS","id_aggregazione":0}],"TERMA":[{"id_w15_data":207133,"id_venue":"158","numeric_value":21,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"TERMA","id_aggregazione":328}]},"64":{"TERMA":[{"id_w15_data":207135,"id_venue":"158","numeric_value":23,"id_trend":1,"id_w15":238,"id_time_layouts":64,"id_parametro":"TERMA","id_aggregazione":328}]},"65":{"TERMA":[{"id_w15_data":207136,"id_venue":"158","numeric_value":5,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"TERMA","id_aggregazione":327}]},"66":{"WIND_CLASS":[{"id_w15_data":207134,"id_venue":"158","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":66,"id_parametro":"WIND_CLASS","id_aggregazione":0}]},"81":{"TERMA":[{"id_w15_data":207138,"id_venue":"158","numeric_value":24,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"TERMA","id_aggregazione":328}]},"82":{"TERMA":[{"id_w15_data":207139,"id_venue":"158","numeric_value":6,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"TERMA","id_aggregazione":327}]},"83":{"WIND_CLASS":[{"id_w15_data":207137,"id_venue":"158","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":83,"id_parametro":"WIND_CLASS","id_aggregazione":0}]}},"159":{"48":{"WIND_CLASS":[{"id_w15_data":207140,"id_venue":"159","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"WIND_CLASS","id_aggregazione":0}],"TERMA":[{"id_w15_data":207141,"id_venue":"159","numeric_value":21,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"TERMA","id_aggregazione":328}]},"64":{"TERMA":[{"id_w15_data":207143,"id_venue":"159","numeric_value":23,"id_trend":1,"id_w15":238,"id_time_layouts":64,"id_parametro":"TERMA","id_aggregazione":328}]},"65":{"TERMA":[{"id_w15_data":207144,"id_venue":"159","numeric_value":5,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"TERMA","id_aggregazione":327}]},"66":{"WIND_CLASS":[{"id_w15_data":207142,"id_venue":"159","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":66,"id_parametro":"WIND_CLASS","id_aggregazione":0}]},"81":{"TERMA":[{"id_w15_data":207146,"id_venue":"159","numeric_value":24,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"TERMA","id_aggregazione":328}]},"82":{"TERMA":[{"id_w15_data":207147,"id_venue":"159","numeric_value":6,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"TERMA","id_aggregazione":327}]},"83":{"WIND_CLASS":[{"id_w15_data":207145,"id_venue":"159","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":83,"id_parametro":"WIND_CLASS","id_aggregazione":0}]}},"165":{"48":{"WIND_CLASS":[{"id_w15_data":207100,"id_venue":"165","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"WIND_CLASS","id_aggregazione":0}],"TERMA":[{"id_w15_data":207101,"id_venue":"165","numeric_value":21,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"TERMA","id_aggregazione":328}]},"64":{"TERMA":[{"id_w15_data":207103,"id_venue":"165","numeric_value":23,"id_trend":1,"id_w15":238,"id_time_layouts":64,"id_parametro":"TERMA","id_aggregazione":328}]},"65":{"TERMA":[{"id_w15_data":207104,"id_venue":"165","numeric_value":5,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"TERMA","id_aggregazione":327}]},"66":{"WIND_CLASS":[{"id_w15_data":207102,"id_venue":"165","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":66,"id_parametro":"WIND_CLASS","id_aggregazione":0}]},"81":{"TERMA":[{"id_w15_data":207106,"id_venue":"165","numeric_value":24,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"TERMA","id_aggregazione":328}]},"82":{"TERMA":[{"id_w15_data":207107,"id_venue":"165","numeric_value":6,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"TERMA","id_aggregazione":327}]},"83":{"WIND_CLASS":[{"id_w15_data":207105,"id_venue":"165","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":83,"id_parametro":"WIND_CLASS","id_aggregazione":0}]}},"166":{"48":{"SKY_CONDIT":[{"id_w15_data":207148,"id_venue":"166","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"SKY_CONDIT","id_aggregazione":0}]},"64":{"SKY_CONDIT":[{"id_w15_data":207149,"id_venue":"166","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":64,"id_parametro":"SKY_CONDIT","id_aggregazione":0}]},"65":{"SKY_CONDIT":[{"id_w15_data":207150,"id_venue":"166","numeric_value":1,"id_trend":null,"id_w15":238,"id_time_layouts":65,"id_parametro":"SKY_CONDIT","id_aggregazione":0}]},"81":{"SKY_CONDIT":[{"id_w15_data":207151,"id_venue":"166","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":81,"id_parametro":"SKY_CONDIT","id_aggregazione":0}]},"82":{"SKY_CONDIT":[{"id_w15_data":207152,"id_venue":"166","numeric_value":1,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"SKY_CONDIT","id_aggregazione":0}]}},"170":{"48":{"SKY_CONDIT":[{"id_w15_data":207153,"id_venue":"170","numeric_value":22,"id_trend":1,"id_w15":238,"id_time_layouts":48,"id_parametro":"SKY_CONDIT","id_aggregazione":0}]},"64":{"SKY_CONDIT":[{"id_w15_data":207154,"id_venue":"170","numeric_value":16,"id_trend":null,"id_w15":238,"id_time_layouts":64,"id_parametro":"SKY_CONDIT","id_aggregazione":0}]},"65":{"SKY_CONDIT":[{"id_w15_data":207155,"id_venue":"170","numeric_value":22,"id_trend":1,"id_w15":238,"id_time_layouts":65,"id_parametro":"SKY_CONDIT","id_aggregazione":0}]},"81":{"SKY_CONDIT":[{"id_w15_data":207156,"id_venue":"170","numeric_value":16,"id_trend":null,"id_w15":238,"id_time_layouts":81,"id_parametro":"SKY_CONDIT","id_aggregazione":0}]},"82":{"SKY_CONDIT":[{"id_w15_data":207157,"id_venue":"170","numeric_value":22,"id_trend":1,"id_w15":238,"id_time_layouts":82,"id_parametro":"SKY_CONDIT","id_aggregazione":0}]}}}})
let state = ref(store.state)
let ready = ref(false)
let readonly = ref(true)
let today = ref('')
let icons = ref([])
let countdown = ref(0)

const props = defineProps({
    id: {
        type: String,
        default: () => ''
    },
})

let tabsDate = ref({  
  0: '',
  1: '',
  2: ''
})

const icon_blacklist = [ 10, 12, 1, 26 ]
const venue_terma = [ 55, 59, 157, 158, 159, 165 ]
const tl_12h = [48, 64, 65, 81, 82]


function createDate(){
  let today = dateToString(new Date(parchi.value.data_emissione))
  let tomorrow = dateToString(new Date(new Date(parchi.value.data_emissione).setDate(new Date(parchi.value.data_emissione).getDate()+1)))
  let afterTomorrow = dateToString(new Date(new Date(parchi.value.data_emissione).setDate(new Date(parchi.value.data_emissione).getDate()+2)))
  //let afterafterTomorrow = dateToString(new Date(new Date(corriere.value.data_emissione).setDate(new Date(corriere.value.data_emissione).getDate()+3)))
  
  tabsDate.value = {
    0: `${today}`,
    1: `${tomorrow}`,
    2: `${afterTomorrow}`
  }
}

let venue_rif = ref({
  55: 'Caselle',
  59: 'Torino',
	157: 'Nichelino',
  158: 'Candiolo',
  159: 'Orbassano',
  165: 'Venaria',
	166: 'Parco di Stupinigi',
  170: 'Parco de La Mandria'
})

const vento_rif = ref( [
        {"numeric_value":0,"description": "Calma di vento"},
        {"numeric_value":1,"description":"Debole"},
        {"numeric_value":2,"description":"Moderato"},
        {"numeric_value":3,"description":"Forte"},
        {"numeric_value":4,"description":"Molto forte"}
    ])


let selected_venue = ref(165)

let actions = ref({
  sending:false,
  reopening: false,
})

onMounted(() => {
  parchi_id.value = props.id
  fetchData()
})


async function fetchIcons () {
  const response = await fetch('/api/w05/sky_conditions/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}


async function fetchForecastComuni () {
  const response = await fetch('/api/w35/forecast_comuni/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}


async function fetchData() {
  today.value = dateToString(new Date())
  ready.value = false
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  fetchParchi(parchi_id.value).then(response => {
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
    
    parchi.value = data
    readonly.value = (parchi.value.status === '1' || parchi.value.status === '2' || !state.value.username)

    let rearrangeparchidata = rearrange(
      parchi.value['w15data_set'],
        "id_venue",
        pippo=>rearrange(pippo, "id_time_layouts", 
        pippo2=>rearrange(pippo2, "id_parametro", (arr: any[]) => arr))
        )
    parchi.value['w15_data'] = rearrangeparchidata   
    createDate() 
  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })

  fetchIcons().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero delle icone`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(data => {
    icons.value = data.filter(icon => !icon_blacklist.includes(icon.id_sky_condition)).map(icon => {
      if (icon.classes.length > 0) {
        icon.id_parametro = icon.classes[0].id_parametro
        icon.ordinamento = icon.classes[0].ordinamento
        delete icon.classes
      } else {
        icon.id_parametro = null
        icon.ordinamento = null
      }
      return icon
    })
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

  fetchForecastComuni().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero delle icone`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(data => {
    if (Object.keys(data).length == 0){
      toast.open(
        {
          message: `Non trovo i dati prodotti dalle Aree Meteo, utilizzo la first guess di default`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
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
}

async function fetchParchi(id: string | number) {
  const response = await fetch('/api/w15/bulletins/' + id + '/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}




function getDateFormatted(rawString: string, time = true) {
  return api.getDateFormatted(rawString, time)
}

function saveW15(newValue: null, id_w15: any, campo: null) {
  const payload = { }
  payload['id_w15'] = id_w15
  payload['username'] = store.state.username
  bulkUpdateW15(payload).then((response) => {
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
  }).then(data => {
    toast.open(
      {
        message: 'Dato salvato',
        type: 'success',
        position: 'top-left'
      }
    )
    parchi.value.last_update = data.last_update
    parchi.value.username = (store.state.username || "")
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


function saveW15Data(newValue: any,id_w15_data: any,campo: string) {
  let myIdW15 = parchi.value.w15data_set.find((w15data: { id_w15_data: any }) => {
    return w15data.id_w15_data === id_w15_data
  })
  if(myIdW15){
    const payload = { }
    myIdW15[campo] = parseInt(newValue)
    payload[campo] = newValue
    fetchPatch(myIdW15.id_w15_data, 'data', payload).then((response) => {
      if (!response.ok) {
        toast.open(
          {
            message: 'Errore nel salvataggio',
            type: 'error',
            position: 'top-left'
          }
        )
      } else {
        saveW15(null, parchi.value.id_w15, null)
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
}

function remove() {
  if (
    confirm('Vuoi davvero cancellare questo bollettino?')
  ) {
    api.fetchBulletinDelete(parchi_id.value, 'w15/bulletins', store).then(response => {
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



function setParchi(id_w15_data: any, campo: any){
  if(window.event && window.event.target !== null){
    let new_value = (window.event.target as HTMLInputElement).value
    saveW15Data(new_value, id_w15_data, campo)
  }
}


async function fetchParchiAction(action: any) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w15/bulletins/${parchi_id.value}/${action}/`
  )
  return response
}

function execute(action: string, reroute: any, message: any) {
  actions.value[action + 'ing'] = true
  fetchParchiAction(action).then(response => {
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
      router.push({ path: `/w15/${data.id_w15}` })
      parchi_id.value = data.id_w15
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

async function fetchPatch(id: any, endpoint: string, payload: {}) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w15/${endpoint}/${id}/`,
    {
      method: 'PATCH',
      body: JSON.stringify(payload)
    }
  )
  return response
}

async function bulkUpdateW15(payload: {}) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w15/bulletins/bulk_update/`,
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
    Object.keys(value_data).forEach(key => value_data[key] = func(value_data[key]))
  }
  if (!Object.values(value_data).some(item => item != undefined)) value_data = {}
  return value_data
}

function dateToString(date){
  const yy = date.getFullYear()
  const mm = date.getMonth() + 1
  const dd = date.getDate()
  return [yy, (mm>9 ? '' : '0') + mm, (dd>9 ? '' : '0') + dd].join('-')
}

</script>

<style scoped>

  table {border: 1px solid;}

  th {max-width: 10px; text-align: left;border: 1px dotted;background-color: rgb(213, 222, 227);}

  td {max-width: 10px; text-align: left;border: 1px dotted;}

</style>