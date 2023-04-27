import Meteo from '../../front/Bulletin.vue'
import { vi } from 'vitest'

// trick to ignore some files we do not need
vi.mock("vue-toast-notification/dist/theme-bootstrap.css");

describe('Meteo page', () => {
  it('watches terma_data', () => {
    // assemble a fake meteo object to mimick the Meteo component properties
    // that need to be accessible to the function to be tested
    let meteo = {
      terma_67: {
        "33": {
          "id_w05_data": 1107,
          "numeric_value": "10.00"
        },
        "50": {
          "id_w05_data": 1107,
          "numeric_value": "10.00"
        },
        "51": {
          "id_w05_data": 1107,
          "numeric_value": "10.00"
        },
        "67": {
          "id_w05_data": 1107,
          "numeric_value": "10.00"
        },
        "68": {
          "id_w05_data": 1107,
          "numeric_value": "10.00"
        },
        "84": {
          "id_w05_data": 1107,
          "numeric_value": "10.00"
        },
        "85": {
          "id_w05_data": 1107,
          "numeric_value": "10.00"
        },
        "101": {
          "id_w05_data": 1107,
          "numeric_value": "10.00"
        },
        "102": {
          "id_w05_data": 1107,
          "numeric_value": "10.00"
        }
      },
      trend: Meteo.methods.trend,
      watch_terma_delta: Meteo.watch.terma_delta
    }

    // random terma_delta
    meteo.watch_terma_delta([[1,-6],[-3,4],[-2,-2],[0,0]])
    let id_trends = Object.values(meteo.terma_67).map(v => v.id_trend)
    expect(id_trends).toEqual([ undefined, 2, undefined, 1, 2, 2, 2, 0, 0 ])
    //                             33            51

    // all negative terma_delta
    meteo.watch_terma_delta([[1,-6],[-6,-6],[-2,-2],[-6,-6]])
    id_trends = Object.values(meteo.terma_67).map(v => v.id_trend)
    expect(id_trends).toEqual([ undefined, 2, undefined, 2, 2, 2, 2, 2, 2 ])

    // all positive terma_delta
    meteo.watch_terma_delta([[1,+6],[+6,+6],[+2,+2],[+6,+6]])
    id_trends = Object.values(meteo.terma_67).map(v => v.id_trend)
    expect(id_trends).toEqual([ undefined, 1, undefined, 1, 1, 1, 1, 1, 1 ])
  })
})
