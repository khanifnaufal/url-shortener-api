import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import StatsView from './views/StatsView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/stats/:shortCode',
    name: 'Stats',
    component: StatsView,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
