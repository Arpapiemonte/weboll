// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    class="row"
    role="group"
    aria-label="Login"
  >
    <div class="col-md-4 offset-md-4">
      <h1 class="text-center">
        Accedi a weboll
      </h1>
      <form>
        <div class="mb-3">
          <label
            for="inputUsername"
            class="form-label"
          >Nome utente</label>
          <input
            id="inputUsername"
            v-model="username"
            type="text"
            class="form-control"
            placeholder="paolgrep"
            @keyup.enter="login"
          >
        </div>
        <div class="mb-3">
          <label
            for="inputPassword"
            class="form-label"
          >Password</label>
          <input
            id="inputPassword"
            v-model="password"
            type="password"
            class="form-control"
            @keyup.enter="login"
          >
        </div>
        <div
          v-show="errorMessage"
          class="alert-danger my-3 p-2"
        >
          {{ errorMessage }}
        </div>
        <button
          :disabled="username === '' || password === ''"
          type="submit"
          class="btn btn-primary"
          @click="login"
        >
          Accedi
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import store from '../store'

export default {
  name: 'LoginForm',
  emits: ['successfulLogin'],
  data () {
    return {
      username: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    login (e) {
      e.preventDefault();
      if (this.username !== '' && this.password !== '') {
        store.login(this.username, this.password).then((data) => {
          if ('access' in data) {
            this.$emit('successfulLogin', data)
          } else {
            this.errorMessage = `Accesso non riuscito: [${data.detail}]`
            console.error('The username and / or password is incorrect')
          }
        }).catch((error) => {
          this.errorMessage = 'Errore di comunicazione col server.'
          console.error('Communication error:', error)
        })
      } else {
        this.errorMessage = 'Inserisci username e password.'
        console.error('A username and password must be present')
      }
    }
  }
}
</script>
