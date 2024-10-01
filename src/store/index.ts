// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
import api from '../api'
import { reactive } from 'vue';

function delete_cookie(name: string, path: string | null, domain: string | null): void {
  document.cookie = name + "=" +
    ((path) ? ";path="+path:"")+
    ((domain)?";domain="+domain:"") +
    ";expires=Thu, 01 Jan 1970 00:00:01 GMT";
}

type State = {
    username: string | null,
    access: string | null
}
type StateKeys = keyof State
const keys = {
  username: 'USERNAME',
  access: 'ACCESS_TOKEN'
}
const state: State = {
  username: null,
  access: null
}
export default {
  debug: false,
  state: reactive(state),
  clear() {
    if (this.debug) console.log('store.clear')
    delete_cookie('csrftoken', null, null)
    delete_cookie('sessionid', null, null)
    Object.keys(this.state).forEach(k => {
      this.state[k as StateKeys] = null
    })
  },
  save() {
    if (this.debug) console.log('store.save')
    Object.keys(this.state).forEach(k => {
      const value = this.state[k as StateKeys]
      if (value != null) {
        window.localStorage.setItem(keys[k as StateKeys], value)
      } else {
        window.localStorage.removeItem(keys[k as StateKeys])
      }
    })
  },
  load() {
    if (this.debug) console.log('store.load')
    if (this.debug) console.log(this.state)
    Object.keys(this.state).forEach(k => {
      this.state[k as StateKeys] = window.localStorage.getItem(keys[k as StateKeys])
    })
  },
  login(username: string, password: string) {
    if (this.debug) console.log('store.login')
    const promise = api.login(username, password).then((data) => {
      if (this.debug) console.log('received data =', data)
      if ('access' in data) {
        this.state.username = username
        this.state.access = data.access
        this.save()
        if (this.debug) console.log('logged in:', this.state.username)
      } else {
        this.clear()
        this.save()
      }
      return data
    })
    return promise
  },
  logout() {
    if (this.debug) console.log('store.logout')
    this.clear()
    this.save()
    if (this.debug) console.log('logged out:', this.state.username)
    return true
  }
}