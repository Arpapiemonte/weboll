import api from '@/api'

describe('today', () => {
  it('renders correctly', () => {
    const start_valid_time = '2021-09-02 14:00:00'
    //expect(api.getDateFormatted(start_valid_time)).toBe('2/9/2021 ore 14:00')
    expect(api.getDateFormatted_eng(start_valid_time)).toBe('2021-09-02 ore 14:00')
  })
})
