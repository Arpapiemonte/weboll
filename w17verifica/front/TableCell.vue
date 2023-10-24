// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  {{ meteoclasses[value].description }}
</template>

<script setup lang="ts">
const props = defineProps<{
    meteoclasses: Object,
    value: number,
}>()
</script>
