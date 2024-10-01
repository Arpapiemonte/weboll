// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import ToastPlugin from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-bootstrap.css';
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

import './assets/css/style.css';


const app = createApp(App)
app.use(router)
app.use(ToastPlugin)
app.mount('#app')
app.component('Datepicker', Datepicker); // eslint-disable-line vue/multi-word-component-names
