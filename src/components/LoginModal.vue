// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    id="loginModal"
    class="modal"
    tabindex="-1"
    aria-labelledby="loginModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5
            id="loginLabel"
            class="modal-title"
          >
            Login
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          />
        </div>
        <div class="modal-body">
          <LoginForm @successful-login="loginModal.hide()" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap'

import LoginForm from '@/components/LoginForm.vue'

export default {
  name: 'LoginModal',
  components: {
    LoginForm,
  },
  data () {
    this.loginModal = null
    return {}
  },
  mounted() {
    this.loginModal = new Modal(document.getElementById('loginModal'))
  },
  methods: {
    show(){
      this.loginModal.show()
    },
    hide(){
      this.loginModal.hide()
    }
  }
}
</script>
