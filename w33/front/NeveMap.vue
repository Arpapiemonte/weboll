// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="sticky-top">
    <svg
      id="Piemonte_vari_layer_480x600"
      transform="tr"
      version="1.1"
      xmlns:svg="http://www.w3.org/2000/svg"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
      xmlns:cc="http://creativecommons.org/ns#"
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      width="776"
      height="826.45"
      x="0px"
      y="0px"
      viewBox="0 0 522.93 556.93"
      style="enable-background:new 0 0 566.93 566.93; transform: translate(-10%);"
      xml:space="preserve"
    >
      <use
        href="#autostradeMap"
      />
      <g id="Autostrade">
        <g
          v-if="showAutostrade.a6"
          id="a6"
        >
          <polyline
            style="fill:none;stroke:#1638DB;stroke-width:8;stroke-miterlimit:10;"
            points="227.333,349.685 244.588,366.263 248.131,407.263 251.131,427.263 248.131,441.93 265.667,478.597 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[94]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[94].min + ' - ' + heights[94].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#1638DB;stroke-width:8;stroke-miterlimit:10;"
            points="265.667,478.597 276.667,482.93 285.667,478.597 292.622,489.166 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[95]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[95].min + ' - ' + heights[95].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#1638DB;stroke-width:8;stroke-miterlimit:10;"
            points="292.622,489.166 302.711,485.735 308.278,490.927 325.709,492.923 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[96]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[96].min + ' - ' + heights[96].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#1638DB;stroke-width:8;stroke-miterlimit:10;"
            points="354.472,500.529 338.318,497.882 333.99,493.215 326,493.215 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[97]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[97].min + ' - ' + heights[97].max + ' m'"
          />
        </g>
        <g
          v-if="showAutostrade.a21"
          id="a21"
        >
          <polyline
            style="fill:none;stroke:#F7A706;stroke-width:8;stroke-miterlimit:10;"
            points="242.333,353.597 254.345,361.263 279.667,361.263 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[66]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[66].min + ' - ' + heights[66].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#F7A706;stroke-width:8;stroke-miterlimit:10;"
            points="281.667,362.93 296.226,373.965 310.423,372.93 316.38,366.263 325.333,369.861 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[106]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[106].min + ' - ' + heights[106].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#F7A706;stroke-width:8;stroke-miterlimit:10;"
            points="325.333,369.861 341.858,372.791 366.319,365.18 379.557,366.317 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[49]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[49].min + ' - ' + heights[49].max + ' m'"
          />
          <line
            style="fill:none;stroke:#F7A706;stroke-width:8;stroke-miterlimit:10;"
            x1="379.644"
            y1="365.18"
            x2="402.628"
            y2="368.723"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[107]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[107].min + ' - ' + heights[107].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#F7A706;stroke-width:8;stroke-miterlimit:10;"
            points="402.628,368.723 410.254,369.861 430.269,354.123 458.131,341.93 479.333,336.597 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[24]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[24].min + ' - ' + heights[24].max + ' m'"
          />
          <line
            style="fill:none;stroke:#F7A706;stroke-width:8;stroke-miterlimit:10;"
            x1="479.333"
            y1="336.597"
            x2="514.528"
            y2="336.735"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[108]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[108].min + ' - ' + heights[108].max + ' m'"
          />
        </g>
        <g
          v-if="showAutostrade.a33"
          id="a33"
        >
          <polyline
            style="fill:none;stroke:#F91EDA;stroke-width:8;stroke-miterlimit:10;"
            points="217.583,487.597 237.333,466.263 250.53,467.386 255.667,466.386 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[187]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[187].min + ' - ' + heights[187].max + ' m'"
          />
          <line
            style="fill:none;stroke:#F91EDA;stroke-width:8;stroke-miterlimit:10;"
            x1="254.667"
            y1="425.263"
            x2="276.667"
            y2="425.263"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[188]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[188].min + ' - ' + heights[188].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#F91EDA;stroke-width:8;stroke-miterlimit:10;"
            points="291.333,417.263 308,390.93 326,370.347 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[189]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[189].min + ' - ' + heights[189].max + ' m'"
          />
        </g>
        <g
          v-if="showAutostrade.a4"
          id="a4"
        >
          <polyline
            style="fill:none;stroke:#880ED4;stroke-width:8;stroke-miterlimit:10;"
            points="259.228,313.135 240.997,323.263 227.333,328.263 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[47]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[47].min + ' - ' + heights[47].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#880ED4;stroke-width:8;stroke-miterlimit:10;"
            points="294.667,283.795 286.333,297.263 259.228,313.135 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[25]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[25].min + ' - ' + heights[25].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#880ED4;stroke-width:8;stroke-miterlimit:10;"
            points="294.667,283.465 314.532,259.192 355.867,249.997 364,250.242 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[19]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[19].min + ' - ' + heights[19].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#880ED4;stroke-width:8;stroke-miterlimit:10;"
            points="364,249.863 379.238,247.824 409.617,247.824 421.188,241.597 442.667,241.597 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[41]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[41].min + ' - ' + heights[41].max + ' m'"
          />
        </g>
        <g
          v-if="showAutostrade.a26"
          id="A7-a26"
        >
          <line
            style="fill:none;stroke:#F21111;stroke-width:8;stroke-miterlimit:10;"
            x1="423.753"
            y1="423.763"
            x2="413.753"
            y2="406.097"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[99]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[99].min + ' - ' + heights[99].max + ' m'"
          />
          <line
            style="fill:none;stroke:#F21111;stroke-width:8;stroke-miterlimit:10;"
            x1="384.333"
            y1="441.525"
            x2="384.788"
            y2="427.597"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[100]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[100].min + ' - ' + heights[100].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#F21111;stroke-width:8;stroke-miterlimit:10;"
            points="384.788,427.597 386.443,410.597 384.426,402.213 412.333,387.93 412.333,372.791 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[101]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[101].min + ' - ' + heights[101].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#F21111;stroke-width:8;stroke-miterlimit:10;"
            points="377.877,397.348 372.667,390.93 372.667,379.263 371.333,364.808 367.144,357.43 365.667,343.54 358.867,328.263 359.406,312.263 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[102]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[102].min + ' - ' + heights[102].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#F21111;stroke-width:8;stroke-miterlimit:10;"
            points="310.423,271.93 318.993,279.651 346.139,287.263 356.667,295.263 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[103]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[103].min + ' - ' + heights[103].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#F21111;stroke-width:8;stroke-miterlimit:10;"
            points="352.413,211.93 367.144,200.263 372.771,194.263 383.415,196.422 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[104]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[104].min + ' - ' + heights[104].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#F21111;stroke-width:8;stroke-miterlimit:10;"
            points="352.413,211.93 346.139,217.93 349.861,231.061 353,244.895 359.414,264.93 356.667,277.597 356.667,298.029 359.406,312.263 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[103]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[103].min + ' - ' + heights[103].max + ' m'"
          />
          <polyline
            style="fill:none;stroke:#F21111;stroke-width:8;stroke-miterlimit:10;"
            points="365.667,194.263 359.414,182.93 367.145,172.263 366,157.473 351.667,145.597 		"
            data-bs-toggle="popover"
            data-bs-placement="top"
            :title="`<div class='d-flex justify-content-between'>${venueNames[105]}<span role='button' class='closebutton btn-close' data-dismiss='alert' ><span></div>`"
            :data-bs-content="'Altezza Min - Max: ' + heights[105].min + ' - ' + heights[105].max + ' m'"
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
      <foreignObject
        v-for="(pos, key) in posIcons"
        :key="key"
        :x="pos.x"
        :y="pos.y"
        :width="((showAutostrade[pos.autostrada] && values[key].showInputBox) || cumulatedSnowValidity[key]) ? '58' : '0'"
        :height="((showAutostrade[pos.autostrada] && values[key].showInputBox) || cumulatedSnowValidity[key]) ? '18' : '0'"
      >
        <form
          v-if="(showAutostrade[pos.autostrada] && values[key].showInputBox) || cumulatedSnowValidity[key]"
          style="line-height: 0;"
        >
          <input
            type="Number"
            data-bs-toggle="tooltip"
            data-bs-placement="top"
            :value="values[key].cumulated_snow"
            :disabled="readonly"
            style="height: 1.5em; width: 2em; font-size: 12px; background-color: white;"
            :style="cumulatedSnowValidity[key] ? ' border: #FFA500; border:2.5px solid #FFA500;' : 'border: #0000ff; border:1px solid #0000ff;'"
            @change="setCumulatedSnow(key)"
          >
          <SnowLevelInput
            :measure="values[key].snow_level"
            :idvenue="key"
            :readonly="readonly"
            :refresher="refresher"
            :tabmode="false"
            :snow-level-info="snowLevelInfo[key]"
            @setmeasure="setSnowLevel"
          />
        </form>
      </foreignObject>
    </svg>
  </div>
</template>

<script lang="ts">
  import SnowLevelInput from './SnowLevelInput.vue'

  export default {
    name: 'NeveMap',
    components: {
      SnowLevelInput,
    }
  }
</script>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Popover } from 'bootstrap'

import { components } from '../../src/types/weboll'

type W33Data = components['schemas']['W33Data']

const icon_snowlist = [ 7, 9, 21, 26, 31, 18, 44 ]

const props = defineProps<{
  datatab: Array<W33Data>,
  showAutostrade: Object,
  cumulatedSnowValidity: Object,
  snowLevelInfo: Object,
  heights: Object,
  readonly: Boolean,
  venueNames: Object,
}>()

let posIcons = ref({
  105: {x:320, y:155, autostrada: "a26"},
  104: {x:360, y:200, autostrada: "a26"},
  103: {x:320, y:270, autostrada: "a26"},
  102: {x:330, y:320, autostrada: "a26"},
  101: {x:400, y:380, autostrada: "a26"},
  100: {x:330, y:440, autostrada: "a26"},
  99: {x:410, y:420, autostrada: "a26"},
  97: {x:330, y:470, autostrada: "a6"},
  96: {x:275, y:500, autostrada: "a6"},
  95: {x:265, y:450, autostrada: "a6"},
  94: {x:200, y:390, autostrada: "a6"},
  47: {x:210, y:300, autostrada: "a4"},
  25: {x:250, y:280, autostrada: "a4"},
  19: {x:300, y:230, autostrada: "a4"},
  41: {x:410, y:220, autostrada: "a4"},
  49: {x:325, y:370, autostrada: "a21"},
  66: {x:230, y:335, autostrada: "a21"},
  106: {x:260, y:355, autostrada: "a21"},
  24: {x:410, y:325, autostrada: "a21"},
  107: {x:360, y:345, autostrada: "a21"},
  108: {x:450, y:305, autostrada: "a21"},
  187: {x:190, y:450, autostrada: "a33"},
  188: {x:265, y:420, autostrada: "a33"},
  189: {x:300, y:390, autostrada: "a33"},
})

let popovers = ref([])
let refresher = ref(0)

onMounted(() => {
  initializePopovers()
})


async function initializePopovers() {
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  popovers.value = popoverTriggerList.map(function (popoverTriggerEl) {
    return new Popover(popoverTriggerEl, { html: true })
  })

  popoverTriggerList.forEach(popover => {
    popover.addEventListener('shown.bs.popover', function () {
      let closebuttons = document.getElementsByClassName('closebutton')
      for(let closebutton of closebuttons){
        closebutton.addEventListener('click', function () {
          popovers.value.find(p => p["_element"] === popover).hide()
        })
      }
    })
  })
}

const emit = defineEmits<{
  setNeve: [id_venue: number, campo: string,  new_value: number]
}>()

const values = computed(() => {
  let values = {}
  props.datatab.forEach(e => {
    values[e.id_venue] = {
      cumulated_snow: e.cumulated_snow,
      snow_level: e.snow_level,
      showInputBox: icon_snowlist.includes(e.id_sky_condition)
    }
  })
  return values
})

function forceUpdate(){
  refresher.value += 1
}

function setSnowLevel(id_venue, new_value){
  emit('setNeve', parseInt(id_venue), 'snow_level', new_value)
  forceUpdate()
}

function setCumulatedSnow(id_venue){
  if(window.event && window.event.target !== null){
    emit('setNeve', parseInt(id_venue), 'cumulated_snow', parseInt((window.event.target as HTMLInputElement).value))
  }
}


</script>

<style>
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  input[type="Number"] {
    appearance: textfield;
  }
</style>
