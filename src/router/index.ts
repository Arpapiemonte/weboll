// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
import { createWebHistory, createRouter } from 'vue-router'
import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import store from '../store'

const main_routes = [  {
  path: '/',
  name: 'Home',
  component: () => import('../pages/HomePage.vue')
},
{
  path: '/about',
  name: 'About',
  component: () => import('../pages/AboutPage.vue')
},
{
  path: '/login',
  name: 'login',
  component: () => import('../pages/LoginPage.vue')
},
{
  path: '/w30/model/:modelname',
  name: 'model',
  component: () => import('../../w30/front/Model.vue')
}]

window.bulletins_list.forEach(bulletin => {
  main_routes.push({
    name: `${bulletin.id}_list`,
    path: `/${bulletin.id}`,
    component: () => import(`../../${bulletin.id}/front/Bulletins.vue`)
  })
  main_routes.push({
    name: `${bulletin.id}_detail`,
    path: `/${bulletin.id}/:id`,
    component: () => import(`../../${bulletin.id}/front/Bulletin.vue`)
  })
})

export const routes = main_routes

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export function beforeEach(to: RouteLocationNormalized, _: RouteLocationNormalized, next: NavigationGuardNext) {
  const PUBLIC_PATHS = ['/', '/login'];
  bulletins_list.forEach(bulletin => {PUBLIC_PATHS.push('/' + bulletin.id)})
  store.load()
  const re = /\/w\d\d\/\d/;
  if (re.test(to.path)) PUBLIC_PATHS.push(to.path);
  const unAuthenticatedAndPrivatePage = (path: string) => (!PUBLIC_PATHS.includes(path) && !store.state.username)
  if (unAuthenticatedAndPrivatePage(to.path)) {
    next(`/login?next=${to.path}`);
  } else {
    next();
  }
}

router.beforeEach((to, from, next) => beforeEach(to, from, next))

export default router
