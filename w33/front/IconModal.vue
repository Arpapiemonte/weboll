// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div>
    <svg
      width="0"
      height="0"
    >
      <defs>
        <symbol
          v-for="icon in icons"
          :id="'id_' + icon.id_sky_condition"
          :key="icon.id_sky_condition"
          width="750"
          height="600"
          viewBox="0 0 750 600"
        >
          <title>{{ icon.description_ita }}</title>
          <image
            width="750"
            height="600"
            :href="`/images/meteo/icons/${icon.id_sky_condition}_${icon.sky_condition}.svg`"
          />
        </symbol>
      </defs>
    </svg>
  </div>
  <div
    id="iconModal"
    class="modal"
    tabindex="-1"
    aria-labelledby="iconModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg shift-modal">
      <div class="modal-content">
        <div class="modal-header">
          <h5
            id="iconModalLabel"
            class="modal-title"
          >
            Cambia l'icona per {{ venuesSelected }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          />
        </div>
        <div class="modal-body">
          <div
            class="row"
            role="group"
            aria-label="Icons"
          >
            <div
              v-for="(icon_group, id_parametro) in iconClasses"
              :key="id_parametro"
            >
              <h5
                class="mt-3"
              >
                {{ icon_group }}
              </h5>
              <button
                v-for="icon in groupedIcons[id_parametro]"
                :key="icon.id_sky_condition"
                type="button"
                class="btn btn-outline-dark col"
                @click="setIcon(icon.id_sky_condition)"
              >
                <svg
                  width="75"
                  height="60"
                  viewBox="0 0 750 600"
                >
                  <use
                    :href="'#id_' + icon.id_sky_condition"
                    x="0"
                    y="0"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { Icons, GroupedIcons } from "../types"

const props = defineProps<{
    venuesSelected: Array<String>,
    icons: Icons,
}>()

const emit = defineEmits(['setIcon'])

const iconClasses = {
    COP_TOT: "Copertura nuvolosa totale",
    PLUV: "Livello pioggia sui 10 minuti",
    SNOW: "Neve( cm)",
    STORM: "Classe temporali",
    VELV: "Velocita' vento (vettoriale)",
    VIS_10M: "Visibility 10 minutes average (max 50 km)"
}

const groupedIcons = computed(() => {
    let result : GroupedIcons = {}
    props.icons.forEach(icon => {
        let parametro = icon.id_parametro
        if(parametro !== null){
            if(!result[parametro]){
                result[parametro] = []
            }
            result[parametro].push(icon)
            result[parametro].sort((a,b) => a.ordinamento - b.ordinamento)
        }
    })
    return result
})

function setIcon(id_sky_condition){
  console.log("setIcon")
    emit('setIcon', id_sky_condition)
}

</script>

<style>
.shift-modal {
   right: 20%;
}
</style>