// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <table class="table">
    <thead>
      <tr>
        <th
          scope="col"
          rowspan="3"
          class="align-middle text-center"
        >
          Zone di<br>allerta
        </th>
        <th
          scope="col"
          :colspan="levels.length * ranges.length"
          class="align-middle text-center"
        >
          {{ title }}
        </th>
      </tr>
      <tr>
        <template
          v-for="level in levels"
          :key="level"
        >
          <th
            scope="col"
            :colspan="ranges.length"
            class="align-middle text-center"
          >
            {{ legend[level] }}
          </th>
        </template>
      </tr>
      <tr>
        <template
          v-for="level in levels"
          :key="level"
        >
          <th
            v-for="range in ranges"
            :key="range"
            scope="col"
            class="align-middle text-center"
          >
            {{ range }}
          </th>
        </template>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="riga in Object.keys(soglie.h6)"
        :key="riga"
      >
        <th scope="row">
          {{ riga }}
        </th>
        <template
          v-for="level in levels"
          :key="level"
        >
          <td
            v-for="range in ranges"
            :key="range"
            :class="classes[level]"
          >
            {{ parseInt(soglie[range][riga][level]) }}
          </td>
        </template>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'TabellaSoglie',
  props: {
    title: {
      type: String,
      default: ""
    },
    soglie: {
      type: Object,
      default: () => { return {} }
    },
    legend: {
      type: Array,
      default: () => []
    },
    levels: {
      type: Array,
      default: () => []
    },
    ranges: {
      type: Array,
      default: () => []
		},
    classes: {
      type: Array,
      default: () => []
		},
	}
}
</script>

<style scoped>
  .pre_all {background-color: #dddddd;}
  .all_0 {background-color: #6EBB00;}
  .all_1 {background-color: #FFFF00;}
  .all_2 {background-color: #FFA500;}
  .all_3 {background-color: #FF0000;}
  .all_4 {background-color: #ffffff;}
</style>
