// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt

<template>
  <div
    id="levelModal"
    class="modal"
    tabindex="-1"
    aria-labelledby="iconModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5
            id="iconModalLabel"
            class="modal-title"
          >
            Cambia il livello per l'area {{ String.fromCharCode(64 + Number(selectedVenue)) }}
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
            class="btn-group"
            role="group"
            aria-label="Icons"
          >
            <button
              v-for="level in levels"
              :key="level.id_ozono_livelli"
              type="button"
              class="btn btn-outline-dark"
              @click="$emit('setSelectedLevel', level.id_ozono_livelli)"
            >
              <svg
                width="75"
                height="60"
                viewBox="0 0 750 600"
              >
                <rect
                  x="0"
                  y="0"
                  width="750"
                  height="600"
                  :fill="level.color"
                />
              </svg>
              {{ level.livelli }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LevelModal',
  props: {
    selectedVenue:  {
      type: Number,
      default: null
    },
    levels: {
      type: Array,
      default: () => []
    }
  },
  emits: ['setSelectedLevel']
}
</script>