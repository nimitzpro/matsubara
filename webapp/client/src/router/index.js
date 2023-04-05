import { createRouter, createWebHistory } from 'vue-router'
// import GenPlaylists from '../components/GenPlaylists.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../components/Search.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../components/About.vue')
    },
    {
      path: '/genplaylists',
      name: 'genplaylists',
      component: () => import('../components/GenPlaylists.vue'),
      // props: true
    }
  ]
})

export default router
