// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="container mt-3">
    <LoginForm @successful-login="$router.push(next_path)" />
  </div>
</template>

<script setup lang="ts">
import LoginForm from '@/components/LoginForm.vue'
import { ref, onMounted } from "vue"
import { useRoute } from 'vue-router'

let next_path = ref('/')

onMounted(() => {
  const route = useRoute()
  if ('next' in route.query && typeof route.query.next == 'string') {
    next_path.value = route.query.next
  }
})
</script>
