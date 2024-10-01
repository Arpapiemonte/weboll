// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name: string) {
  let cookieValue = ''
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

export default {
  async login(username: string, password: string) {
    const payload = { username, password }
    const response = await fetch(
      '/api/token/',
      {
        method: 'POST',
        credentials: "same-origin",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }
    )
    return response.json()
  },
  fetch_wrapper(access: string, uri: string, options: (object|undefined)=undefined) {
    return fetch(uri, {
      ...options,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${access}`,
        accept: 'application/json',
        'X-CSRFTOKEN': getCookie('csrftoken')
      }
    })
  },
  async fetchBulletinDelete (id: string, endpoint: string, store: {state: {access: string}}) {
    const response = await this.fetch_wrapper(
      store.state.access,
      `/api/${endpoint}/${id}/`,
      {
        method: 'DELETE'
      }
    )
    return response
  },
  async fetchBulletins (endpoint: string, page: number) {
    const response = await fetch(`/api/${endpoint}/?page=${page + 1}`, {
      headers: {
        'accept': 'application/json'
      }
    })
    return response
  },
  async fetchBulletinsFilter(endpoint: string, options: {page: number, year: number, month: number}) {
    const response = await fetch(
      `/api/${endpoint}/?page=${options.page + 1}&year=${options.year}&month=${
        options.month
      }`,
      {
        headers: {
          'accept': 'application/json'
        },
      }
    )
    return response
  },
  getDateFormatted(rawString: string, time = true, days = 0) {
    const rawDate = new Date(rawString)
    rawDate.setDate(rawDate.getDate() + days)
    const dateDay = rawDate.getDate()
    const dateMonth = rawDate.getMonth() + 1
    const dateYear = rawDate.getFullYear()
    if (time) {
      const dateHour = rawDate.getHours()
      let dateMinutes
      if (rawDate.getMinutes() < 10){
        dateMinutes = "0" + rawDate.getMinutes()
      } else {
        dateMinutes = "" + rawDate.getMinutes()
      }
      return dateDay + "/" + dateMonth + "/" + dateYear + " ore " + dateHour + ":" + dateMinutes
    } else {
      return dateDay + "/" + dateMonth + "/" + dateYear
    }
  }
}
