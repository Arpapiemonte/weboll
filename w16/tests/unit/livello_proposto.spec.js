import { mount } from '@vue/test-utils'
import AreaOzono from '../../front/AreaOzono.vue'

describe('AreaOzono.vue', () => {
  const levels = [
    {
      id_ozono_livelli: 1,
      livelli: 0,
      rgb: "0:255:0",
      soglia_inferiore_mxd: 0,
      soglia_inferiore_mx8: 0
    },
    {
      id_ozono_livelli: 2,
      livelli: 1,
      rgb: "255:255:0",
      soglia_inferiore_mxd: 180,
      soglia_inferiore_mx8: 110
    },
    {
      id_ozono_livelli: 3,
      livelli: 2,
      rgb: "255:165:0",
      soglia_inferiore_mxd: 240,
      soglia_inferiore_mx8: 140
    },
    {
      id_ozono_livelli: 4,
      livelli: 3,
      rgb: "255.00.00",
      soglia_inferiore_mxd: 360,
      soglia_inferiore_mx8: 220
    }
  ]
  const value = {
    level :1,
    id_w16_data: 64128,
    w16data1: {
      mx8: {},
      mxd: {}
    }
  }
  const readonly = true
  const wrapper = mount(AreaOzono, {
    propsData: { levels, value, readonly }
  })

  const reference_mxd = {
    0: 0,
    179: 0,
    180: 0,
    181: 1,
    239: 1,
    240: 1,
    241: 2,
    359: 2,
    360: 2,
    361: 3,
    999: 3
  }
  Object.keys(reference_mxd).forEach(k => {
    it(`proposes level ${reference_mxd[k]} for mxd value = ${k}`, () => {
      expect(wrapper.vm.livello_proposto_mxd(k)).toEqual(reference_mxd[k])
    })
  })

  const reference_mx8 = {
    0: 0,
    109: 0,
    110: 0,
    111: 1,
    139: 1,
    140: 1,
    141: 2,
    219: 2,
    220: 2,
    221: 3,
    999: 3
  }
  Object.keys(reference_mx8).forEach(k => {
    it(`proposes level ${reference_mx8[k]} for mx8 value = ${k}`, () => {
      expect(wrapper.vm.livello_proposto_mx8(k)).toEqual(reference_mx8[k])
    })
  })
})
