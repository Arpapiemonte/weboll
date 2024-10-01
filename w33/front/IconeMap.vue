// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="sticky-top col-12">
    <svg
      id="Piemonte_vari_layer_480x600"
      version="1.1"
      xmlns:svg="http://www.w3.org/2000/svg"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
      xmlns:cc="http://creativecommons.org/ns#"
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      viewBox="0 0 522.93 556.93"
      style="enable-background:new 0 0 522.93 556.93; transform: translate(-10%);"
      xml:space="preserve"
      width="776"
      height="826.45"
    >
      <use
        :href="'#autostradeMap'"
      />
      <g id="Autostrade">
        <g
          v-if="showAutostrade.a6"
          id="a6"
        >
          <polyline
            id="94"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="227.333,349.685 244.588,366.263 248.131,407.263 251.131,427.263 248.131,441.93 265.667,478.597 		"
            :style="posIcons[94].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#1638DB'"
            @click="autostradaClick"
          />
          <polyline
            id="95"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="265.667,478.597 276.667,482.93 285.667,478.597 292.622,489.166 		"
            :style="posIcons[95].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#1638DB'"
            @click="autostradaClick"
          />
          <polyline
            id="96"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="292.622,489.166 302.711,485.735 308.278,490.927 325.709,492.923 		"
            :style="posIcons[96].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#1638DB'"
            @click="autostradaClick"
          />
          <polyline
            id="97"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="354.472,500.529 338.318,497.882 333.99,493.215 326,493.215 		"
            :style="posIcons[97].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#1638DB'"
            @click="autostradaClick"
          />
        </g>
        <g
          v-if="showAutostrade.a21"
          id="a21"
        >
          <polyline
            id="66"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="242.333,353.597 254.345,361.263 279.667,361.263 		"
            :style="posIcons[66].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F7A706'"
            @click="autostradaClick"
          />
          <polyline
            id="106"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="281.667,362.93 296.226,373.965 310.423,372.93 316.38,366.263 325.333,369.861 		"
            :style="posIcons[106].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F7A706'"
            @click="autostradaClick"
          />
          <polyline
            id="49"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="325.333,369.861 341.858,372.791 366.319,365.18 379.557,366.317 		"
            :style="posIcons[49].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F7A706'"
            @click="autostradaClick"
          />
          <line
            id="107"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            x1="379.644"
            y1="365.18"
            x2="402.628"
            y2="368.723"
            :style="posIcons[107].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F7A706'"
            @click="autostradaClick"
          />
          <polyline
            id="24"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="402.628,368.723 410.254,369.861 430.269,354.123 458.131,341.93 479.333,336.597 		"
            :style="posIcons[24].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F7A706'"
            @click="autostradaClick"
          />
          <line
            id="108"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            x1="479.333"
            y1="336.597"
            x2="514.528"
            y2="336.735"
            :style="posIcons[108].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F7A706'"
            @click="autostradaClick"
          />
        </g>
        <g
          v-if="showAutostrade.a33"
          id="a33"
        >
          <polyline
            id="187"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="217.583,487.597 237.333,466.263 250.53,467.386 255.667,466.386 		"
            :style="posIcons[187].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F91EDA'"
            @click="autostradaClick"
          />
          <line
            id="188"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            x1="254.667"
            y1="425.263"
            x2="276.667"
            y2="425.263"
            :style="posIcons[188].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F91EDA'"
            @click="autostradaClick"
          />
          <polyline
            id="189"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="291.333,417.263 308,390.93 326,370.347 		"
            :style="posIcons[189].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F91EDA'"
            @click="autostradaClick"
          />
        </g>
        <g
          v-if="showAutostrade.a4"
          id="a4"
        >
          <polyline
            id="47"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="259.228,313.135 240.997,323.263 227.333,328.263 		"
            :style="posIcons[47].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#880ED4'"
            @click="autostradaClick"
          />
          <polyline
            id="25"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="294.667,283.795 286.333,297.263 259.228,313.135 		"
            :style="posIcons[25].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#880ED4'"
            @click="autostradaClick"
          />
          <polyline
            id="19"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="294.667,283.465 314.532,259.192 355.867,249.997 364,250.242 		"
            :style="posIcons[19].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#880ED4'"
            @click="autostradaClick"
          />
          <polyline
            id="41"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="364,249.863 379.238,247.824 409.617,247.824 421.188,241.597 442.667,241.597 		"
            :style="posIcons[41].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#880ED4'"
            @click="autostradaClick"
          />
        </g>
        <g
          v-if="showAutostrade.a26"
          id="A7-a26"
        >
          <line
            id="99"
            :style="posIcons[99].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F21111'"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            x1="423.753"
            y1="423.763"
            x2="413.753"
            y2="406.097"
            @click="autostradaClick"
          />
          <line
            id="100"
            :style="posIcons[100].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F21111'"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            x1="384.333"
            y1="441.525"
            x2="384.788"
            y2="427.597"
            @click="autostradaClick"
          />
          <polyline
            id="101"
            :style="posIcons[101].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F21111'"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="384.788,427.597 386.443,410.597 384.426,402.213 412.333,387.93 412.333,372.791 		"
            @click="autostradaClick"
          />
          <polyline
            id="102"
            :style="posIcons[102].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F21111'"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="377.877,397.348 372.667,390.93 372.667,379.263 371.333,364.808 367.144,357.43 365.667,343.54 358.867,328.263 359.406,312.263 		"
            @click="autostradaClick"
          />
          <polyline
            id="103"
            :style="posIcons[103].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F21111'"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="310.423,271.93 318.993,279.651 346.139,287.263 356.667,295.263 		"
            @click="autostradaClick"
          />
          <polyline
            id="104"
            :style="posIcons[104].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F21111'"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="352.413,211.93 367.144,200.263 372.771,194.263 383.415,196.422 		"
            @click="autostradaClick"
          />
          <polyline
            id="103"
            :style="posIcons[103].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F21111'"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="352.413,211.93 346.139,217.93 349.861,231.061 353,244.895 359.414,264.93 356.667,277.597 356.667,298.029 359.406,312.263 		"
            @click="autostradaClick"
          />
          <polyline
            id="105"
            :style="posIcons[105].checked ? 'stroke:#1F1F1F;stroke-opacity:0.95;' : 'stroke:#F21111'"
            style="fill:none;stroke-width:8;stroke-miterlimit:10;"
            points="365.667,194.263 359.414,182.93 367.145,172.263 366,157.473 351.667,145.597 		"
            @click="autostradaClick"
          />
        </g>
      </g>
      <g
        v-if="showAutostrade.a4"
        id="PAL-A4"
      >
        <circle
          style="fill:#FFFFFF;stroke:#461257;stroke-width:2;stroke-miterlimit:10;"
          cx="227.333"
          cy="328.263"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#461257;stroke-width:2;stroke-miterlimit:10;"
          cx="259.228"
          cy="313.135"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#461257;stroke-width:2;stroke-miterlimit:10;"
          cx="294.667"
          cy="283.465"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#461257;stroke-width:2;stroke-miterlimit:10;"
          cx="364"
          cy="249.997"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#461257;stroke-width:2;stroke-miterlimit:10;"
          cx="442.667"
          cy="241.597"
          r="3.543"
        />
      </g>
      <g
        v-if="showAutostrade.a21"
        id="PAL-A21"
      >
        <circle
          style="fill:#FFFFFF;stroke:#D16E02;stroke-width:2;stroke-miterlimit:10;"
          cx="242.333"
          cy="353.597"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#D16E02;stroke-width:2;stroke-miterlimit:10;"
          cx="279.667"
          cy="361.263"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#D16E02;stroke-width:2;stroke-miterlimit:10;"
          cx="325.146"
          cy="369.861"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#D16E02;stroke-width:2;stroke-miterlimit:10;"
          cx="379.644"
          cy="365.18"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#D16E02;stroke-width:2;stroke-miterlimit:10;"
          cx="479.333"
          cy="336.597"
          r="3.543"
        />
        <circle
          style="fill:#231F20;stroke:#D16E02;stroke-width:2;stroke-miterlimit:10;"
          cx="514.528"
          cy="336.735"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#D16E02;stroke-width:2;stroke-miterlimit:10;"
          cx="402.628"
          cy="368.723"
          r="3.543"
        />
      </g>
      <g
        v-if="showAutostrade.a26"
        id="PAL-A7"
      >
        <circle
          style="fill:#FFFFFF;stroke:#AF0909;stroke-width:2;stroke-miterlimit:10;"
          cx="351.667"
          cy="145.597"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#AF0909;stroke-width:2;stroke-miterlimit:10;"
          cx="365.667"
          cy="194.263"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#AF0909;stroke-width:2;stroke-miterlimit:10;"
          cx="383.706"
          cy="195.988"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#AF0909;stroke-width:2;stroke-miterlimit:10;"
          cx="352.413"
          cy="211.93"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#AF0909;stroke-width:2;stroke-miterlimit:10;"
          cx="359.406"
          cy="312.263"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#AF0909;stroke-width:2;stroke-miterlimit:10;"
          cx="310.423"
          cy="271.93"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#AF0909;stroke-width:2;stroke-miterlimit:10;"
          cx="377.877"
          cy="397.348"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#AF0909;stroke-width:2;stroke-miterlimit:10;"
          cx="412.333"
          cy="373.404"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#AF0909;stroke-width:2;stroke-miterlimit:10;"
          cx="384.788"
          cy="443.664"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#AF0909;stroke-width:2;stroke-miterlimit:10;"
          cx="384.788"
          cy="427.597"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#AF0909;stroke-width:2;stroke-miterlimit:10;"
          cx="424.178"
          cy="423.756"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#AF0909;stroke-width:2;stroke-miterlimit:10;"
          cx="413.753"
          cy="406.097"
          r="3.543"
        />
      </g>
      <g
        v-if="showAutostrade.a6"
        id="PAL-A6"
      >
        <circle
          style="fill:#FFFFFF;stroke:#060C7C;stroke-width:2;stroke-miterlimit:10;"
          cx="325.709"
          cy="492.923"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#060C7C;stroke-width:2;stroke-miterlimit:10;"
          cx="292.622"
          cy="489.166"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#060C7C;stroke-width:2;stroke-miterlimit:10;"
          cx="265.667"
          cy="478.597"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#060C7C;stroke-width:2;stroke-miterlimit:10;"
          cx="227.333"
          cy="349.685"
          r="3.543"
        />
        <circle
          style="stroke:#060C7C;stroke-width:2;stroke-miterlimit:10;"
          cx="354.472"
          cy="500.529"
          r="3.543"
        />
      </g>
      <g
        v-if="showAutostrade.a33"
        id="PAL-A33"
      >
        <circle
          style="fill:#FFFFFF;stroke:#970A9E;stroke-width:2;stroke-miterlimit:10;"
          cx="254.667"
          cy="425.263"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#970A9E;stroke-width:2;stroke-miterlimit:10;"
          cx="277.833"
          cy="425.263"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#970A9E;stroke-width:2;stroke-miterlimit:10;"
          cx="291.333"
          cy="417.263"
          r="3.543"
        />
        <circle
          style="fill:#FFFFFF;stroke:#970A9E;stroke-width:2;stroke-miterlimit:10;"
          cx="255.667"
          cy="466.386"
          r="3.543"
        />
        <circle
          style="fill:#231F20;stroke:#970A9E;stroke-width:2;stroke-miterlimit:10;"
          cx="217.331"
          cy="487.623"
          r="3.543"
        />
        <path
          style="fill:#FFFFFF;stroke:#970A9E;stroke-width:2;stroke-miterlimit:10;"
          d="M328.576,371.31
            c-0.69,1.831-2.734,2.756-4.565,2.066c-1.831-0.69-2.756-2.734-2.066-4.565"
        />
      </g>
      <g
        v-for="(pos, key) in posIcons"
        :key="key"
      >
        <image
          v-if="showAutostrade[pos.autostrada]"
          width="35"
          height="35"
          :x="pos.x"
          :y="pos.y"
          :href="`/images/meteo/icons/${values[key]}_${iconfmap[values[key]].sky_condition}.svg`"
          @click="iconClick(key)"
        />
      </g>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

import { components } from '../../src/types/weboll'

type W33Data = components['schemas']['W33Data']

const props = defineProps<{
  datatab: Array<W33Data>,
  icons: Array<Object>,
  showAutostrade: Object,
  venuesSelected: Array<string>,
  readonly: boolean,
  campoIcon: string
}>()

let posIcons = ref({
  105: {x:320, y:155, autostrada: "a26", checked: false},
  104: {x:365, y:205, autostrada: "a26", checked: false},
  103: {x:310, y:290, autostrada: "a26", checked: false},
  102: {x:370, y:300, autostrada: "a26", checked: false},
  101: {x:420, y:370, autostrada: "a26", checked: false},
  100: {x:340, y:420, autostrada: "a26", checked: false},
  99: {x:430, y:400, autostrada: "a26", checked: false},
  97: {x:340, y:460, autostrada: "a6", checked: false},
  96: {x:290, y:500, autostrada: "a6", checked: false},
  95: {x:250, y:490, autostrada: "a6", checked: false},
  94: {x:200, y:390, autostrada: "a6", checked: false},
  47: {x:210, y:280, autostrada: "a4", checked: false},
  25: {x:250, y:260, autostrada: "a4", checked: false},
  19: {x:290, y:215, autostrada: "a4", checked: false},
  41: {x:410, y:200, autostrada: "a4", checked: false},
  49: {x:320, y:330, autostrada: "a21", checked: false},
  66: {x:245, y:320, autostrada: "a21", checked: false},
  106: {x:285, y:330, autostrada: "a21", checked: false},
  24: {x:420, y:305, autostrada: "a21", checked: false},
  107: {x:385, y:325, autostrada: "a21", checked: false},
  108: {x:480, y:295, autostrada: "a21", checked: false},
  187: {x:190, y:440, autostrada: "a33", checked: false},
  188: {x:265, y:430, autostrada: "a33", checked: false},
  189: {x:320, y:380, autostrada: "a33", checked: false},
})


watch(() => props.venuesSelected, (new_venues) => {
  for(const tratto in posIcons.value){
    posIcons.value[tratto].checked = false
  }
  new_venues.forEach(e => {
    posIcons.value[e].checked = true
  })
}, {deep: true})

const emit = defineEmits<{
  openModal: [],
  updateVenueSelected: [venuesSelected: number[]]
}>()

const values = computed(() => {
  let values = {}
  props.datatab.forEach(e => {
    values[e.id_venue] = e[props.campoIcon]
  })
  return values
})

const iconfmap = computed(() => {
  let iconfmap = {}
  props.icons.forEach(e => {
    iconfmap[e.id_sky_condition] = e
  });
  return iconfmap
})


function iconClick(key){
  if(!props.readonly){
    let oneSelected = false
    for(const tratto in posIcons.value){
      if(posIcons.value[tratto].checked){
        oneSelected = true
      }
    }

    if(oneSelected){
      emit('openModal')
    }else{
      posIcons.value[key].checked = !posIcons.value[key].checked
      let venuesSelected : Array<number> = []
      venuesSelected.push(parseInt(key))
      emit('updateVenueSelected', venuesSelected)
      emit('openModal')
    }


  }
}

function autostradaClick(){
  if(window.event && !props.readonly){
    const tratto_id = (window.event.target as HTMLInputElement).id

    let venuesSelected : Array<number> = []

    posIcons.value[tratto_id].checked = !posIcons.value[tratto_id].checked
    for(const tratto in posIcons.value){
      if(posIcons.value[tratto].checked){
        venuesSelected.push(parseInt(tratto))
      }
    }

    emit('updateVenueSelected', venuesSelected)
  }
}
</script>
