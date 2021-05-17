export const routes = [
  {
    path: '/',
    name: 'Landing',
    component: () =>
      import(/* webpackChunkName: "layout" */ '@/views/Navigation.vue'),
    children: [
      {
        name: 'City',
        path: '/city/:id',
        component: () =>
          import(/* webpackChunkName: "city" */ '@/components/City/main.vue'),
      },
      {
        name: 'Team',
        path: '/team',
        component: () =>
          import(/* webpackChunkName: "team" */ '@/components/Team/main.vue'),
      },
      {
        name: 'Dashboard',
        path: '/dashboard',
        component: () =>
          import(
            /* webpackChunkName: "dashboard" */ '@/components/Dashboard/main.vue'
          ),
      },
      {
        name: 'Home',
        path: '',
        component: () =>
          import(
            /* webpackChunkName: "landing" */ '@/components/Home/main.vue'
          ),
      },
      {
        name: 'Redirect',
        path: '*',
        redirect: { name: 'Landing' },
      },
    ],
  },
];
