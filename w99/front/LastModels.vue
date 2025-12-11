// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    class="row"
  > 
    <div
      class="col-md-12 mb-3"
    >
      <div class="row">
        <div class="col-md-12 mb-3">
          <div v-if="countfetch>0">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th
                    class="text-center"
                    style="width: 4em;"
                    scope="col"
                  >
                    Model name
                  </th>
                  <th
                    class="text-center"
                    style="width: 4em;"
                    scope="col"
                  >
                    Model type
                  </th>
                  <th
                    class="text-center"
                    style="width: 4em;"
                    scope="col"
                  >
                    Date emiss
                  </th>
                  <th
                    class="text-center"
                    style="width: 4em;"
                    scope="col"
                  >
                    Time emiss
                  </th>
                  <th
                    class="text-center"
                    style="width: 4em;"
                    scope="col"
                  >
                    Stations count
                  </th>
                </tr>
              </thead>
              <tr
                v-for="(task, key) in lastmodels"
                :key="task"
              >
                <td
                  class="text-center"
                >
                  {{ renamemodel(lastmodels[key]["model_name"]) }}
                </td>
                <td
                  class="text-center"
                >
                  {{ lastmodels[key]["model_type"] }}
                </td>
                <td
                  class="text-center"
                >
                  {{ lastmodels[key]["date_emiss"] }}
                </td>
                <td
                  class="text-center"
                >
                  {{ lastmodels[key]["time_emiss"] }}
                </td>
                <td
                  class="text-center"
                >
                  {{ lastmodels[key]["count"] }}
                </td>
              </tr>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  export default {
    name: 'LastModels',
  }
</script>

<script setup lang="ts">
import api from '../../src/api'
import { Ref, ref, onMounted, watch, computed } from 'vue'
import { useToast } from 'vue-toast-notification'
const toast = useToast()
const countfetch = ref(0)
const lastmodels: Ref<LastModels> = ref({})

async function fetchLastModels () {
  const response = await fetch('/api/w99/last_models/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchData () {
  countfetch.value = countfetch.value + 1
  fetchLastModels().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero dei models`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json() 
  }).then(data => {
    lastmodels.value = data
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

onMounted(async () => {
  fetchData()
})

function renamemodel(name){
  let new_name = name
  if (name == "LAMIN0063"){
    new_name = "COSMO0045"
  }
  return new_name
}

</script>

<style scoped>

  table {border: 1px solid;}

  th {max-width: 10px; text-align: left;border: 1px dotted;background-color: rgb(213, 222, 227);}

  td {max-width: 10px; text-align: left;border: 1px dotted;}

</style>