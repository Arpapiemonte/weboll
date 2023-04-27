import store from '@/store'
import api from '@/api'
import { vi } from 'vitest'

vi.mock('@/api')

describe('store', () => {
  it('starts clean', () => {
    expect(store.state.username).toBeNull()
    expect(store.state.access).toBeNull()
  })
  it('saves data on login', async () => {
    api.login.mockResolvedValue({access: 'xxx'})
    await store.login('user', 'pass')
    expect(store.state.access).toBe('xxx')
    expect(store.state.username).toBe('user')
  })
  it('clears data on logout', () => {
    store.logout()
    expect(store.state.username).toBeNull()
    expect(store.state.access).toBeNull()
  })
})
