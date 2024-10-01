// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
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
        <div class="col-8">
          <h4 class="text-center">Refresh forecast comuni tasks {{ countfetch }}</h4>
        </div>
        <div 
          v-if="is_started"
          class="col-4"
        >
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12 mb-3">
          <table class="table table-striped">
            <thead>
              <tr>
                <th
                  class="text-center"
                  style="width: 4em;"
                  scope="col"
                >
                  Date created
                </th>
                <th
                  class="text-center"
                  style="width: 4em;"
                  scope="col"
                >
                  Date done
                </th>
                <th
                  class="text-center"
                  style="width: 4em;"
                  scope="col"
                >
                  Status
                </th>
                <th
                  class="text-center"
                  style="width: 4em;"
                  scope="col"
                >
                  Result
                </th>
              </tr>
            </thead>
            <tr
              v-for="(task, key) in tasks"
              :key="task"
            >
              <td
                class="text-center"
              >
                {{ tasks[key]["date_created"] }}
              </td>
              <td
                class="text-center"
              >
                {{ tasks[key]["date_done"] }}
              </td>
              <td
                class="text-center"
                :style="tasks[key]['status'] == 'SUCCESS'?'background-color:green':'background-color:yellow'"
              >
                {{ tasks[key]["status"] }}
              </td>
              <td
                width="50%"
              >
                <p v-html="tasks[key]['result'].replaceAll('\\n', '<br>').replaceAll('\\', '')"></p>
              </td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  export default {
    name: 'TasksBulletins',
  }
</script>

<script setup lang="ts">
import api from '../../src/api'
import { Ref, ref, onMounted, watch, computed } from 'vue'
import { useToast } from 'vue-toast-notification'
const toast = useToast()
const countfetch = ref(0)
const tasks: Ref<DjangoCeleryResultsTaskresult> = ref({})

async function fetchTasks () {
  const response = await fetch('/api/w35/tasks/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchData () {
  countfetch.value = countfetch.value + 1
  fetchTasks().then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero dei task`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json() 
  }).then(data => {
    tasks.value = data
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
  fetchDataTimeout()
})

const is_started = computed(() => {
  if (Object.keys(tasks.value).length > 0){
    for (const [key, value] of Object.entries(tasks.value)) {
      // console.log("is_started", key, value, value.status)
      if (value.status == 'STARTED'){
        //console.log("is_started ritorna true c'è il record STARTED")
        return true
      }
    }
    // console.log("is_started ritorna false non c'è nessun record a STARTED")
    return false
  }else{
    // console.log("is_started ritorna true tasks è vuoto")
    return true
  }
})

function fetchDataTimeout(){
  // console.log("fetchDataTimeout")
  if (is_started.value){
    // console.log("fetchDataTimeout is_started è true")
    fetchData()
    setTimeout(() => {
      fetchDataTimeout()
    }, 2000);
  }
}
</script>

<style scoped>

  table {border: 1px solid;}

  th {max-width: 10px; text-align: left;border: 1px dotted;background-color: rgb(213, 222, 227);}

  td {max-width: 10px; text-align: left;border: 1px dotted;}

</style>