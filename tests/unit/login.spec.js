import { render, fireEvent } from '@testing-library/vue'
import Login from '@/pages/LoginPage.vue'
import App from '@/App.vue'
import '@/bulletins'
import { routes, beforeEach } from '@/router'
import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import api from '@/api'
import { vi } from 'vitest'

vi.mock('@/api')

describe('login', () => {
  it('renders form title', () => {
    // Create a Router instance
    // https://next.router.vuejs.org/api/#createrouter
    // using a HTML5 history.
    // https://next.router.vuejs.org/api/#createwebhistory
    const router = createRouter({
      history: createWebHistory(),
      routes: routes
    })
    const { getByText } = render(Login, {
      global: {
        plugins: [router]
      }
    })
    getByText('Accedi a weboll')
  })
  it('navigates guests to Login when About page is requested', async () => {
    const next = to => { expect(to).toMatch(/^\/login/)}
    const to = {path: '/about'}
    beforeEach(to, undefined, next)
  })
  it('navigates logged-in users to About page', async () => {
    api.login.mockResolvedValue({access: 'xxx'})
    await store.login('user', 'pass')
    const next = to => { expect(to).toBeUndefined()}
    const to = {path: '/about'}
    beforeEach(to, undefined, next)
  })
})
