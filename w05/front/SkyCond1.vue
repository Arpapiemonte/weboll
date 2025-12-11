// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="my-3">
    <div class="row">
      <h3>Sky condition</h3>
    </div>
    <div class="row">
      <div class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th scope="col">
                Località
              </th>
              <th scope="col">
                SkyCondition<br>
              </th>
              <th
                scope="col"
                class="text-center"
              >
                <img
                  v-if="t_min_locked & !readonly"
                  role="button"
                  title="Sblocca temperature minime"
                  src="~bootstrap-icons/icons/lock-fill.svg"
                  alt="lock icon"
                  width="18"
                  height="18"
                  @click="t_min_locked = false"
                > 
                <img
                  v-else-if="!readonly"
                  role="button"
                  title="Blocca temperature minime"
                  src="~bootstrap-icons/icons/unlock-fill.svg"
                  alt="unlock icon"
                  width="18"
                  height="18"
                  @click="t_min_locked = true"
                > 
                Tmin
                <TermaArrows
                  :venue-selection="venueSelection"
                  :readonly="readonly || t_min_locked"
                  @increase="termaStep(0,1)"
                  @decrease="termaStep(0,-1)"
                />
              </th>
              <th
                scope="col"
                class="text-center"
              >
                Tmax
                <TermaArrows
                  :venue-selection="venueSelection"
                  :readonly="readonly"
                  @increase="termaStep(1,1)"
                  @decrease="termaStep(1,-1)"
                />
              </th>
              <th
                v-if="!readonly"
                scope="col"
                class="text-center"
              >
                <button
                  type="button"
                  class="btn btn-link"
                  aria-label="Clear"
                  :disabled="venueSelection.length == Object.keys(selectedVenues).length || readonly"
                  @click="setAll(true)"
                >
                  Tutte
                </button>
                <button
                  type="button"
                  class="btn btn-link"
                  aria-label="Clear"
                  :disabled="venueSelection.length === 0 || readonly"
                  @click="setAll(false)"
                >
                  Resetta
                </button>
                <button
                  type="button"
                  class="btn btn-link"
                  aria-label="Clear"
                  :disabled="venueSelection.length == Object.keys(selectedVenues).length || readonly"
                  @click="setAlpi(true)"
                >
                  Alpi
                </button>
                <button
                  type="button"
                  class="btn btn-link"
                  aria-label="Clear"
                  :disabled="venueSelection.length == Object.keys(selectedVenues).length || readonly"
                  @click="setPianure(true)"
                >
                  Pianure
                </button>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(data, id) in venue_data"
              :key="id"
            >
              <th scope="row">
                {{ id }} {{ venueNames[id] }}
              </th>
              <Cell
                v-if="'SKY_CONDIT' in data"
                :readonly="readonly || (venueSelection.length > 1)"
                :data="data.SKY_CONDIT[0]"
                :icons="icons"
                :history="history"
                :validity="validity"
                @set-level="setLevel"
              />
              <td v-else />
              <template v-if="'TERMA' in data">
                <td class="text-left">
                  <Terma
                    :readonly="readonly || t_min_locked"
                    :data="data.TERMA[0]"
                    :history="history"
                    :validity="validity"
                    @set-level="setLevel"
                  />
                  <template v-if="'TERMA_700' in data">
                    <MeteoArrow :id-trend="venue_data[67].TERMA[0].id_trend" />
                    <dl
                      class="mt-4"
                    >
                      <dt />
                      <dd>
                        <Terma
                          :readonly="readonly || t_min_locked"
                          :data="data.TERMA_700[0]"
                          :history="history"
                          :validity="validity"
                          @set-level="setLevel"
                        />
                      </dd>
                      <dt />
                      <dd>
                        <Terma
                          :readonly="readonly || t_min_locked"
                          :data="data.TERMA_1500[0]"
                          :history="history"
                          :validity="validity"
                          @set-level="setLevel"
                        />
                      </dd>
                      <dt />
                      <dd>
                        <Terma
                          :readonly="readonly || t_min_locked"
                          :data="data.TERMA_2000[0]"
                          :history="history"
                          :validity="validity"
                          @set-level="setLevel"
                        />
                      </dd>
                    </dl>
                  </template>
                </td>
                <td class="text-left">
                  <Terma
                    :readonly="readonly"
                    :data="data.TERMA[1]"
                    :history="history"
                    :validity="validity"
                    @set-level="setLevel"
                  />
                  <template v-if="'TERMA_700' in data">
                    <MeteoArrow :id-trend="venue_data[67].TERMA[1].id_trend" />
                    <dl 
                      class="mt-4"
                    >
                      <dt />
                      <dd>
                        <Terma
                          :readonly="readonly"
                          :data="data.TERMA_700[1]"
                          :history="history"
                          :validity="validity"
                          @set-level="setLevel"
                        />
                        700 m
                      </dd>
                      <dt />
                      <dd>
                        <Terma
                          :readonly="readonly"
                          :data="data.TERMA_1500[1]"
                          :history="history"
                          :validity="validity"
                          @set-level="setLevel"
                        />
                        1500 m
                      </dd>
                      <dt />
                      <dd>
                        <Terma
                          :readonly="readonly"
                          :data="data.TERMA_2000[1]"
                          :history="history"
                          :validity="validity"
                          @set-level="setLevel"
                        />
                        2000 m
                      </dd>
                    </dl>
                  </template>
                </td>
              </template>
              <td
                v-else
                colspan="2"
              />
              <td
                v-if="!readonly"
                class="text-center"
              >
                <input
                  :checked="selectedVenues[id]"
                  class="form-check-input"
                  type="checkbox"
                  value=""
                  :disabled="readonly"
                  @change="$emit('setVenue', id, $event.target.checked)"
                >
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import Cell from './Cell.vue'
import Terma from './Terma.vue'
import TermaArrows from './TermaArrows.vue'
import SkyCond from './SkyCond.js'
import MeteoArrow from './MeteoArrow.vue'

export default {
  name: 'SkyCond1',
  components: {
    Cell,
    Terma,
    TermaArrows,
    MeteoArrow,
  },
  mixins: [SkyCond],
  props: {
    cieli: {
      type: Array,
      default: () => [{}, {}, {}]
    },
    index: {
      type: Number,
      default: 1
    },
    selectedVenues: {
      type: Object,
      default: () => {
        return {
          1: false,
          9: false,
          11: false,
          28: false,
          33: false,
          59: false,
          63: false,
          64: false,
          87: false,
          88: false,
          89: false,
          90: false,
          91: false,
          92: false,
          93: false
        }
      }
    },
    icons: {
      type: Array,
      default: () => []
    },
    readonly: {
      type: Boolean,
      default: false
    },
    history: {
      type: Object,
      default: () => { return { cursor: -1, snapshots: [] } }
    },
    venueNames: {
      type: Array,
      default: () => []
    },
    validity: {
      type: Object,
      default: () => { return {} }
    },
  },
  emits: ["setVenue"],
  data() {
    return {
      t_min_locked: true
    }
  },
  computed: {
    venue_data() {
      let vd = { }
      // SKY_CONDIT pomeriggio
      this.rearrange1(this.cieli[0], vd, 'SKY_CONDIT')
      // TERMA minime e massime
      this.rearrange2(this.cieli[1], this.cieli[2], vd, 'TERMA')
      this.rearrange2(this.cieli[1], this.cieli[2], vd, 'TERMA_700')
      this.rearrange2(this.cieli[1], this.cieli[2], vd, 'TERMA_1500')
      this.rearrange2(this.cieli[1], this.cieli[2], vd, 'TERMA_2000')
      return vd
    }
  }
}
</script>
