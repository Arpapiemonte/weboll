// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="table-responsive">
    <table class="table">
      <thead>
        <tr>
          <th scope="col">
            Zona di<br>allerta
          </th>
          <th scope="col">
            Massimo<br>allerta
          </th>
          <th
            v-if="!scenario"
            scope="col"
          >
            Classe<br>temporali
          </th>
          <th
            v-for="parametro in titoli_parametri"
            :key="parametro"
            scope="col"
          >
            {{ parametro }}
          </th>
          <th
            v-if="scenario"
            scope="col"
            class="col-7"
          >
            Scenario atteso
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="area in w23data"
          :key="area.id_w23_data"
        >
          <th scope="row">
            {{ area.id_w23_zone.nome_zona }}
          </th>
          <td :style="`background-color: ${pericoloMassimo[area.id_w23_zone.id_w23_zone].colore_html};`">
            {{ pericoloMassimo[area.id_w23_zone.id_w23_zone].id_w23_pericolo }}
          </td>
          <td
            v-if="!scenario"
            :style="`background-color: ${coloreriskstorm[area.id_w23_zone.nome_zona].colore_html};`"
          >
            {{ coloreriskstorm[area.id_w23_zone.nome_zona].rischio_temporali }}
          </td>
          <template
            v-for="parametro in listaParametri"
            :key="parametro"
          >
            <td
              v-if="readonly"
              :style="`background-color: ${area[parametro].colore_html};`"
            >
              {{ area[parametro].id_w23_pericolo }}
            </td>
            <SelectPericolo
              v-else
              :area="area"
              :campo="parametro"
              :pericoli="pericoli_applicabili[parametro.split('_')[0]]"
              @change-pericolo="changePericolo"
            />
          </template>
          <template v-if="scenario">
            <td v-if="!readonly">
              <datalist id="scenari">
                <option
                  v-for="eff in effetti"
                  :key="eff.id_w23_effettiterritorio"
                  :value="eff.descrizione"
                >
                  {{ eff.descrizione }}
                </option>
              </datalist>
              <input
                v-model="area.scenario_atteso"
                onfocus="if (this.value.trim()==='-') this.value=''"
                size="55"
                list="scenari"
                @change="$emit('saveData', area.scenario_atteso, area.id_w23_zone.id_w23_zone, 'scenario_atteso')"
              >
            </td>
            <td v-else>
              {{ area.scenario_atteso }}
            </td>
          </template>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import SelectPericolo from './SelectPericolo.vue'

export default {
  name: 'TabellaAllerta',
  components: {
    SelectPericolo
  },
  props: {
    pericoloMassimo:  {
      type: Object,
      default: null
    },
    w23data:  {
      type: Object,
      default: null
    },
    listaParametri: {
      type: Array,
      default: () => []
    },
    pericoli: {
      type: Array,
      default: () => []
    },
    effetti: {
      type: Array,
      default: () => []
    },
    readonly: {
      type: Boolean,
      default: false
    },
    scenario: {
      type: Boolean,
      default: false
    },
    coloreriskstorm:  {
      type: Object,
      default: null
    },
  },
  emits: ['saveData', 'saveDataPericolo'],
  computed: {
    titoli_parametri () {
      return this.listaParametri.map(p => p[0].toUpperCase() + p.slice(1, p.search('_')))
    },
    pericoli_applicabili () {
      const no_bianco = this.pericoli.filter(pericolo => pericolo.id_w23_pericolo !== 'BIANCO')
      const no_bianco_no_rosso = this.pericoli.filter(pericolo => pericolo.id_w23_pericolo !== 'BIANCO' && pericolo.id_w23_pericolo !== 'ROSSO')
      return {
        idrogeologico: no_bianco,
        idraulico: no_bianco,
        temporali: no_bianco_no_rosso,
        neve: no_bianco,
        valanghe: this.pericoli
      }
    }
  },
  methods: {
    changePericolo(newValue, id_w23_zone, campo) {
      this.$emit('saveDataPericolo', newValue, id_w23_zone, campo)
    }
  }
}
</script>
