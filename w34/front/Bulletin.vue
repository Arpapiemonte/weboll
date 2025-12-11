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
          :href="'/api/w34/pdf/' + corriere.id_w34"
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
          v-if="corriere.status === '0' && state.username"
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
          v-if="corriere.status === '1' && state.username && corriere.data_emissione.substring(0, 10) === today"
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
          v-if="corriere.status === '0' && state.username"
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
      <h1>Corriere di Novara {{ corriere.id_w34 }}</h1>
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
          <span v-if="corriere.status === '1'">
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
            :value="getDateFormatted(corriere.data_emissione, false)"
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
            :value="getDateFormatted(corriere.last_update)"
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
            :value="corriere.username"
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
            v-for="(value, key) in corriere.w34_data[328]"
            :key="key"
            class="nav-item"
            role="presentation"
          >
            <button
              class="nav-link"
              :class="{'active' : selected_time_layout === parseInt(key.toString())}"
              type="button"
              role="tab"
              @click="selected_time_layout = parseInt(key.toString())"
            >
              {{ tabsDate[key] }}
            </button>
          </li>
        </ul>
      </div>
    </div>
    <div class="row">
      <div class="col-md-8 mb-3">
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">
                Comune
              </th>
              <th scope="col">
                Tmin
              </th>
              <th scope="col">
                Tmax
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>                    
              <td>
                {{ venue_rif[corriere['w34_data']['327'][selected_time_layout+1]['12'][0].id_venue] }}
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['327'][selected_time_layout+1]['12'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['327'][selected_time_layout+1]['12'][0].id_w34_data, 'numeric_value')"
                >
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['328'][selected_time_layout]['12'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['328'][selected_time_layout]['12'][0].id_w34_data, 'numeric_value')"
                >              
              </td>
            </tr>
            <tr>                    
              <td>
                {{ venue_rif[corriere['w34_data']['327'][selected_time_layout+1]['33'][0].id_venue] }}
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['327'][selected_time_layout+1]['33'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['327'][selected_time_layout+1]['33'][0].id_w34_data, 'numeric_value')"
                >
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['328'][selected_time_layout]['33'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['328'][selected_time_layout]['33'][0].id_w34_data, 'numeric_value')"
                >
              </td>
            </tr>
            <tr>                    
              <td>
                {{ venue_rif[corriere['w34_data']['327'][selected_time_layout+1]['13'][0].id_venue] }}
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['327'][selected_time_layout+1]['13'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['327'][selected_time_layout+1]['13'][0].id_w34_data, 'numeric_value')"
                >
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['328'][selected_time_layout]['13'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['328'][selected_time_layout]['13'][0].id_w34_data, 'numeric_value')"
                >
              </td>
            </tr>
            <tr>                    
              <td>
                {{ venue_rif[corriere['w34_data']['327'][selected_time_layout+1]['50'][0].id_venue] }}
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['327'][selected_time_layout+1]['50'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['327'][selected_time_layout+1]['50'][0].id_w34_data, 'numeric_value')"
                >
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['328'][selected_time_layout]['50'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['328'][selected_time_layout]['50'][0].id_w34_data, 'numeric_value')"
                >
              </td>
            </tr>
            <tr>                    
              <td>
                {{ venue_rif[corriere['w34_data']['327'][selected_time_layout+1]['51'][0].id_venue] }}
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['327'][selected_time_layout+1]['51'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['327'][selected_time_layout+1]['51'][0].id_w34_data, 'numeric_value')"
                >
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['328'][selected_time_layout]['51'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['328'][selected_time_layout]['51'][0].id_w34_data, 'numeric_value')"
                >
              </td>
            </tr>
            <tr>                    
              <td>
                {{ venue_rif[corriere['w34_data']['327'][selected_time_layout+1]['52'][0].id_venue] }}
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['327'][selected_time_layout+1]['52'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['327'][selected_time_layout+1]['52'][0].id_w34_data, 'numeric_value')"
                >
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['328'][selected_time_layout]['52'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['328'][selected_time_layout]['52'][0].id_w34_data, 'numeric_value')"
                >
              </td>
            </tr>
            <tr>                    
              <td>
                {{ venue_rif[corriere['w34_data']['327'][selected_time_layout+1]['63'][0].id_venue] }}
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['327'][selected_time_layout+1]['63'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['327'][selected_time_layout+1]['63'][0].id_w34_data, 'numeric_value')"
                >
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['328'][selected_time_layout]['63'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['328'][selected_time_layout]['63'][0].id_w34_data, 'numeric_value')"
                >
              </td>
            </tr>
            <tr>                    
              <td>
                {{ venue_rif[corriere['w34_data']['327'][selected_time_layout+1]['53'][0].id_venue] }}
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['327'][selected_time_layout+1]['53'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['327'][selected_time_layout+1]['53'][0].id_w34_data, 'numeric_value')"
                >
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['328'][selected_time_layout]['53'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['328'][selected_time_layout]['53'][0].id_w34_data, 'numeric_value')"
                >
              </td>
            </tr>
            <tr>                    
              <td>
                {{ venue_rif[corriere['w34_data']['327'][selected_time_layout+1]['54'][0].id_venue] }}
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['327'][selected_time_layout+1]['54'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['327'][selected_time_layout+1]['54'][0].id_w34_data, 'numeric_value')"
                >
              </td>
              <td>
                <input
                  v-model="corriere['w34_data']['328'][selected_time_layout]['54'][0].numeric_value"
                  type="Number"
                  step="1"
                  class="form-control"
                  title="Neve cumulata"
                  :disabled="readonly"
                  @change="setTermaCorriere(corriere['w34_data']['328'][selected_time_layout]['54'][0].id_w34_data, 'numeric_value')"
                >
              </td>              
            </tr>
          </tbody>
        </table>
      </div>  <!--col-->
      <div class="col-md-4 mb-3">
        <img 
          src="../back/static/images/quote-corr-novara.png"
          class="img-fluid"
          style="height: 576px; width: 349px;"
        >
      </div>  <!--col-->
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'CorriereBulletin',
}
</script>

<script setup lang="ts">
import { Ref, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toast-notification'

import api from '../../src/api'
import store from '../../src/store'

import { components } from '../../src/types/weboll'
import type { W34_data } from "../types"

const router = useRouter()
const toast = useToast()

type W34Full = components['schemas']['W34'] & { w34_data: W34_data } & { w34data_set: components['schemas']['W34Data'][] } 

type ArrayTransformer = (arr: Array<any>) => any
// reactive properties
let corriere_id = ref('')
let corriere: Ref<W34Full> = ref({
    "id_w34": 237,
    "seq_num": 125,
    "data_emissione": "2023-02-16T01:00:00",
    "status": "1",
    "last_update": "2023-02-16T09:57:28.733410",
    "username": "weboll",
    "id_w34_parent": null,
    "w34data_set": [
        {
            "id_w34_data": 197003,
            "id_venue": "33",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 68,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197004,
            "id_venue": "33",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 67,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197006,
            "id_venue": "33",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 85,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197007,
            "id_venue": "33",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 84,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197008,
            "id_venue": "33",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 102,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197009,
            "id_venue": "33",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 101,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197010,
            "id_venue": "13",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 68,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197011,
            "id_venue": "13",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 67,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197012,
            "id_venue": "13",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 85,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197013,
            "id_venue": "13",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 84,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197014,
            "id_venue": "13",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 102,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197015,
            "id_venue": "13",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 101,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197016,
            "id_venue": "50",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 68,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197017,
            "id_venue": "50",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 67,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197018,
            "id_venue": "50",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 85,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197019,
            "id_venue": "50",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 84,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197020,
            "id_venue": "50",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 102,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197021,
            "id_venue": "50",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 101,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197022,
            "id_venue": "51",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 68,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197023,
            "id_venue": "51",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 67,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197024,
            "id_venue": "51",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 85,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197025,
            "id_venue": "51",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 84,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197026,
            "id_venue": "51",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 102,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197027,
            "id_venue": "51",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 101,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197028,
            "id_venue": "52",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 68,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197029,
            "id_venue": "52",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 67,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197030,
            "id_venue": "52",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 85,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197031,
            "id_venue": "52",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 84,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197032,
            "id_venue": "52",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 102,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197033,
            "id_venue": "52",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 101,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197034,
            "id_venue": "53",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 68,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197035,
            "id_venue": "53",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 67,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197036,
            "id_venue": "53",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 85,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197037,
            "id_venue": "53",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 84,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197038,
            "id_venue": "53",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 102,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197039,
            "id_venue": "53",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 101,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197040,
            "id_venue": "54",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 68,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197041,
            "id_venue": "54",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 67,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197042,
            "id_venue": "54",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 85,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197043,
            "id_venue": "54",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 84,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197044,
            "id_venue": "54",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 102,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197045,
            "id_venue": "54",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 101,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197046,
            "id_venue": "63",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 68,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197047,
            "id_venue": "63",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 67,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197048,
            "id_venue": "63",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 85,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197049,
            "id_venue": "63",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 84,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197050,
            "id_venue": "63",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 102,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197051,
            "id_venue": "63",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 101,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197052,
            "id_venue": "12",
            "numeric_value": -1,
            "id_w34": 237,
            "id_time_layouts": 68,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197053,
            "id_venue": "12",
            "numeric_value": 10,
            "id_w34": 237,
            "id_time_layouts": 67,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197054,
            "id_venue": "12",
            "numeric_value": -2,
            "id_w34": 237,
            "id_time_layouts": 85,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197055,
            "id_venue": "12",
            "numeric_value": 11,
            "id_w34": 237,
            "id_time_layouts": 84,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        },
        {
            "id_w34_data": 197056,
            "id_venue": "12",
            "numeric_value": -3,
            "id_w34": 237,
            "id_time_layouts": 102,
            "id_parametro": "TERMA",
            "id_aggregazione": 327
        },
        {
            "id_w34_data": 197057,
            "id_venue": "12",
            "numeric_value": 12,
            "id_w34": 237,
            "id_time_layouts": 101,
            "id_parametro": "TERMA",
            "id_aggregazione": 328
        }
    ],
    "w34_data": {
        "327": {
            "68": {
                "12": [
                    {
                        "id_w34_data": 197052,
                        "id_venue": "12",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 68,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "13": [
                    {
                        "id_w34_data": 197010,
                        "id_venue": "13",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 68,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "33": [
                    {
                        "id_w34_data": 197003,
                        "id_venue": "33",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 68,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "50": [
                    {
                        "id_w34_data": 197016,
                        "id_venue": "50",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 68,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "51": [
                    {
                        "id_w34_data": 197022,
                        "id_venue": "51",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 68,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "52": [
                    {
                        "id_w34_data": 197028,
                        "id_venue": "52",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 68,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "53": [
                    {
                        "id_w34_data": 197034,
                        "id_venue": "53",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 68,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "54": [
                    {
                        "id_w34_data": 197040,
                        "id_venue": "54",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 68,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "63": [
                    {
                        "id_w34_data": 197046,
                        "id_venue": "63",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 68,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ]
            },
            "85": {
                "12": [
                    {
                        "id_w34_data": 197054,
                        "id_venue": "12",
                        "numeric_value": -2,
                        "id_w34": 237,
                        "id_time_layouts": 85,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "13": [
                    {
                        "id_w34_data": 197012,
                        "id_venue": "13",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 85,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "33": [
                    {
                        "id_w34_data": 197006,
                        "id_venue": "33",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 85,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "50": [
                    {
                        "id_w34_data": 197018,
                        "id_venue": "50",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 85,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "51": [
                    {
                        "id_w34_data": 197024,
                        "id_venue": "51",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 85,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "52": [
                    {
                        "id_w34_data": 197030,
                        "id_venue": "52",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 85,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "53": [
                    {
                        "id_w34_data": 197036,
                        "id_venue": "53",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 85,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "54": [
                    {
                        "id_w34_data": 197042,
                        "id_venue": "54",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 85,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "63": [
                    {
                        "id_w34_data": 197048,
                        "id_venue": "63",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 85,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ]
            },
            "102": {
                "12": [
                    {
                        "id_w34_data": 197056,
                        "id_venue": "12",
                        "numeric_value": -3,
                        "id_w34": 237,
                        "id_time_layouts": 102,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "13": [
                    {
                        "id_w34_data": 197014,
                        "id_venue": "13",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 102,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "33": [
                    {
                        "id_w34_data": 197008,
                        "id_venue": "33",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 102,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "50": [
                    {
                        "id_w34_data": 197020,
                        "id_venue": "50",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 102,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "51": [
                    {
                        "id_w34_data": 197026,
                        "id_venue": "51",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 102,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "52": [
                    {
                        "id_w34_data": 197032,
                        "id_venue": "52",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 102,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "53": [
                    {
                        "id_w34_data": 197038,
                        "id_venue": "53",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 102,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "54": [
                    {
                        "id_w34_data": 197044,
                        "id_venue": "54",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 102,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ],
                "63": [
                    {
                        "id_w34_data": 197050,
                        "id_venue": "63",
                        "numeric_value": -1,
                        "id_w34": 237,
                        "id_time_layouts": 102,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 327
                    }
                ]
            }
        },
        "328": {
            "67": {
                "12": [
                    {
                        "id_w34_data": 197053,
                        "id_venue": "12",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 67,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "13": [
                    {
                        "id_w34_data": 197011,
                        "id_venue": "13",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 67,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "33": [
                    {
                        "id_w34_data": 197004,
                        "id_venue": "33",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 67,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "50": [
                    {
                        "id_w34_data": 197017,
                        "id_venue": "50",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 67,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "51": [
                    {
                        "id_w34_data": 197023,
                        "id_venue": "51",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 67,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "52": [
                    {
                        "id_w34_data": 197029,
                        "id_venue": "52",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 67,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "53": [
                    {
                        "id_w34_data": 197035,
                        "id_venue": "53",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 67,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "54": [
                    {
                        "id_w34_data": 197041,
                        "id_venue": "54",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 67,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "63": [
                    {
                        "id_w34_data": 197047,
                        "id_venue": "63",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 67,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ]
            },
            "84": {
                "12": [
                    {
                        "id_w34_data": 197055,
                        "id_venue": "12",
                        "numeric_value": 11,
                        "id_w34": 237,
                        "id_time_layouts": 84,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "13": [
                    {
                        "id_w34_data": 197013,
                        "id_venue": "13",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 84,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "33": [
                    {
                        "id_w34_data": 197007,
                        "id_venue": "33",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 84,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "50": [
                    {
                        "id_w34_data": 197019,
                        "id_venue": "50",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 84,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "51": [
                    {
                        "id_w34_data": 197025,
                        "id_venue": "51",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 84,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "52": [
                    {
                        "id_w34_data": 197031,
                        "id_venue": "52",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 84,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "53": [
                    {
                        "id_w34_data": 197037,
                        "id_venue": "53",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 84,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "54": [
                    {
                        "id_w34_data": 197043,
                        "id_venue": "54",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 84,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "63": [
                    {
                        "id_w34_data": 197049,
                        "id_venue": "63",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 84,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ]
            },
            "101": {
                "12": [
                    {
                        "id_w34_data": 197057,
                        "id_venue": "12",
                        "numeric_value": 12,
                        "id_w34": 237,
                        "id_time_layouts": 101,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "13": [
                    {
                        "id_w34_data": 197015,
                        "id_venue": "13",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 101,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "33": [
                    {
                        "id_w34_data": 197009,
                        "id_venue": "33",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 101,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "50": [
                    {
                        "id_w34_data": 197021,
                        "id_venue": "50",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 101,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "51": [
                    {
                        "id_w34_data": 197027,
                        "id_venue": "51",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 101,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "52": [
                    {
                        "id_w34_data": 197033,
                        "id_venue": "52",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 101,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "53": [
                    {
                        "id_w34_data": 197039,
                        "id_venue": "53",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 101,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "54": [
                    {
                        "id_w34_data": 197045,
                        "id_venue": "54",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 101,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ],
                "63": [
                    {
                        "id_w34_data": 197051,
                        "id_venue": "63",
                        "numeric_value": 10,
                        "id_w34": 237,
                        "id_time_layouts": 101,
                        "id_parametro": "TERMA",
                        "id_aggregazione": 328
                    }
                ]
            }
        }
    }
})
let state = ref(store.state)
let ready = ref(false)
let readonly = ref(true)
let today = ref('')

const props = defineProps({
    id: {
        type: String,
        default: () => ''
    },
})

let venue_rif = ref({
  33: 'Novara',
  13: 'Arona',
  50: 'Borgomanero',
	51: 'Mottarone',
  52: 'Omegna',
  63: 'Verbania',
	12: 'Domodossola',
  53: 'Macugnaga',
  54: 'Formazza'
})

let selected_time_layout = ref(67)

let tabsDate = ref({  
  67: '',
  68: '',
  84: '',
  85: '',
  101: '',
  102: '',
})

function createTabsDate(){
  //let today = dateToString(new Date(corriere.value.data_emissione))
  let tomorrow = dateToString(new Date(new Date(corriere.value.data_emissione).setDate(new Date(corriere.value.data_emissione).getDate()+1)))
  let afterTomorrow = dateToString(new Date(new Date(corriere.value.data_emissione).setDate(new Date(corriere.value.data_emissione).getDate()+2)))
  let afterafterTomorrow = dateToString(new Date(new Date(corriere.value.data_emissione).setDate(new Date(corriere.value.data_emissione).getDate()+3)))
  
  tabsDate.value = {
    67: `${tomorrow}`,
    68: `${tomorrow}`,
    84: `${afterTomorrow}`,
    85: `${afterTomorrow}`,
    101: `${afterafterTomorrow}`,
    102: `${afterafterTomorrow}`,
  }
}

let actions = ref({
  sending:false,
  reopening: false,
})

onMounted(() => {
  corriere_id.value = props.id
  fetchData()
})

async function fetchData() {
  today.value = dateToString(new Date())
  ready.value = false
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  fetchCorriere(corriere_id.value).then(response => {
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
    
    corriere.value = data
    readonly.value = (corriere.value.status === '1' || corriere.value.status === '2' || !state.value.username)

    let rearrangecorrieredata = rearrange(
      corriere.value['w34data_set'],
          "id_aggregazione",
          pippo=>rearrange(pippo, "id_time_layouts", 
          pippo2=>rearrange(pippo2, "id_venue", (arr: any[]) => arr))
          )
    corriere.value['w34_data'] = rearrangecorrieredata    
    createTabsDate()
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

async function fetchCorriere(id: string | number) {
  const response = await fetch('/api/w34/bulletins/' + id + '/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}


function getDateFormatted(rawString: string, time = true) {
  return api.getDateFormatted(rawString, time)
}

function saveW34(newValue: null, id_w34: any, campo: null) {
  const payload = { }
  payload['id_w34'] = id_w34
  payload['username'] = store.state.username
  bulkUpdateW34(payload).then((response) => {
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
    corriere.value.last_update = data.last_update
    corriere.value.username = (store.state.username || "")
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


function saveW34Data(newValue: any,id_w34_data: any,campo: string) {
  let myIdW34 = corriere.value.w34data_set.find((w34data: { id_w34_data: any }) => {
    return w34data.id_w34_data === id_w34_data
  })
  if(myIdW34){
    const payload = { }
    myIdW34[campo] = parseInt(newValue)
    payload[campo] = newValue
    fetchPatch(myIdW34.id_w34_data, 'data', payload).then((response) => {
      if (!response.ok) {
        toast.open(
          {
            message: 'Errore nel salvataggio',
            type: 'error',
            position: 'top-left'
          }
        )
      } else {
        saveW34(null, corriere.value.id_w34, null)
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
    api.fetchBulletinDelete(corriere_id.value, 'w34/bulletins', store).then(response => {
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

function setTermaCorriere(id_w34_data: any, campo: any){
  if(window.event && window.event.target !== null){
    let new_value = (window.event.target as HTMLInputElement).value
    saveW34Data(new_value, id_w34_data, campo)
  }
}

async function fetchCorriereAction(action: any) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w34/bulletins/${corriere_id.value}/${action}/`
  )
  return response
}

function execute(action: string, reroute: any, message: any) {
  actions.value[action + 'ing'] = true
  fetchCorriereAction(action).then(response => {
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
      router.push({ path: `/w34/${data.id_w34}` })
      corriere_id.value = data.id_w34
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
    `/api/w34/${endpoint}/${id}/`,
    {
      method: 'PATCH',
      body: JSON.stringify(payload)
    }
  )
  return response
}

async function bulkUpdateW34(payload: {}) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w34/bulletins/bulk_update/`,
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

