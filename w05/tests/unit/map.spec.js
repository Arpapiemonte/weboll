// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt

import { render } from '@testing-library/vue'
import MapMeteo from '../../front/MapMeteo.vue'

describe('MapMeteo.vue', () => {
  const selectedVenues = {
    1: true,
    9: true,
    11: true,
    28: true,
    33: false,
    59: false,
    63: false,
    64: false,
    87: false,
    88: false,
    89: false,
    90: false,
    91: false,
    92: false,
    93: false
  }
  const skyCondition = [
    {
      "id_w05_data": 806,
      "numeric_value": "3.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 33,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 807,
      "numeric_value": "3.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 59,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 808,
      "numeric_value": "3.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 63,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 809,
      "numeric_value": "3.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 64,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 883,
      "numeric_value": "3.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 87,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 885,
      "numeric_value": "4.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 88,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 886,
      "numeric_value": "3.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 89,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 916,
      "numeric_value": "9.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 1,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 928,
      "numeric_value": "32.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 92,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 931,
      "numeric_value": "31.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 91,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 932,
      "numeric_value": "23.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 93,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 933,
      "numeric_value": "4.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 9,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 938,
      "numeric_value": "18.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",

      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 28,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 950,
      "numeric_value": "9.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 90,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    },
    {
      "id_w05_data": 958,
      "numeric_value": "23.00",
      "text_value": null,
      "start_valid_time": "2021-11-07T12:00:00",
      "end_valid_time": "2021-11-07T23:59:00",
      "id_w05": 25399,
      "id_venue": 11,
      "id_parametro": "SKY_CONDIT",
      "id_aggregazione": 914,
      "id_trend": null,
      "id_time_layouts": 48
    }
  ]
  const icons = [
    {
      "id_sky_condition": 32,
      "sky_condition": "vel",
      "description": "Veils",
      "description_ita": "Velature",
      "id_parametro": "COP_TOT",
      "ordinamento": 6
    },
    {
      "id_sky_condition": 4,
      "sky_condition": "fog",
      "description": "Fog",
      "description_ita": "Nebbia",
      "id_parametro": "VIS_10M",
      "ordinamento": 2
    },
    {
      "id_sky_condition": 23,
      "sky_condition": "ts",
      "description": "Thunderstorm",
      "description_ita": "Temporali",
      "id_parametro": "STORM",
      "ordinamento": 3
    },
    {
      "id_sky_condition": 18,
      "sky_condition": "r-s",
      "description": "Rain and snow",
      "description_ita": "Pioggia e neve",
      "id_parametro": "PLUV",
      "ordinamento": 5
    },
    {
      "id_sky_condition": 9,
      "sky_condition": "l-s",
      "description": "Light snow",
      "description_ita": "Nevicata debole",
      "id_parametro": "SNOW",
      "ordinamento": 1
    },
    {
      "id_sky_condition": 31,
      "sky_condition": "w-snow",
      "description": "Wind and snow",
      "description_ita": "Vento e neve",
      "id_parametro": "VELV",
      "ordinamento": 3
    }
  ]
  const groupedIcons = {
    "SNOW": [{
      "id_sky_condition": 9,
      "description_ita": "Nevicata debole",
    }],
    "COP_TOT": [{
      "id_sky_condition": 32,
      "description_ita": "Velature",
    }],
    "VIS_10M": [{
      "id_sky_condition": 4,
      "description_ita": "Nebbia",
    }],
    "PLUV": [{
      "id_sky_condition": 18,
      "description_ita": "Pioggia e neve",
    }],
    "VELV": [{
      "id_sky_condition": 31,
      "description_ita": "Vento e neve",
    }],
    "STORM": [{
      "id_sky_condition": 23,
      "description_ita": "Temporali",
    }]
  }
  icons.forEach(icon => { icon.count = skyCondition.filter(s => Math.floor(s.numeric_value) == Math.floor(icon.id_sky_condition)).length })

  it('test data are consistent', () => {
    expect(Object.keys(selectedVenues).length).toEqual(skyCondition.length)
  })

  it('renders the icons and they are clickable', () => {
    const { container, getAllByRole, getAllByTestId } = render(MapMeteo, {
      props: { selectedVenues, icons, skyCondition, groupedIcons }
    })
    expect(getAllByRole('icona').length).toEqual(skyCondition.length)
    expect(container.querySelectorAll('[style="cursor: pointer;"]').length).toEqual(skyCondition.length)
    icons.forEach(icon => { expect(getAllByTestId(Math.floor(icon.id_sky_condition)).length).toEqual(icon.count) })
  })

  it('renders the venue contours if not readonly', () => {
    const { container, getAllByRole } = render(MapMeteo, {
      props: { selectedVenues, icons, skyCondition, groupedIcons }
    })
    expect(getAllByRole('contorno').length).toEqual(skyCondition.length)
    let selected_venues_count = Object.keys(selectedVenues).filter(v => selectedVenues[v]).length
    expect(container.querySelectorAll('.selected').length).toEqual(selected_venues_count)
  })

  it('does not render the venue contours if readonly', () => {
    let readonly = true
    const { container, queryAllByRole } = render(MapMeteo, {
      props: { selectedVenues, icons, skyCondition, readonly, groupedIcons }
    })
    expect(queryAllByRole('contorno').length).toEqual(0)
    expect(container.querySelectorAll('.selected').length).toEqual(0)
  })

  it('icons are not clickable if readonly', () => {
    let readonly = true
    const { container } = render(MapMeteo, {
      props: { selectedVenues, icons, skyCondition, readonly, groupedIcons }
    })
    expect(container.querySelectorAll('[style="cursor: pointer;"]').length).toEqual(0)
  })
})
