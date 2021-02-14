export const routes = [
  {
    path: "/",
    name: "Landing",
    component: () => import("@/views/Navigation.vue"),
    children: [
      {
        name: "City",
        path: "/city/:id",
        component: () => import(/* webpackChunkName: "lazy" */ "@/components/City/main.vue")
      },
      {
        name: "Team",
        path: "/team",
        component: () => import(/* webpackChunkName: "lazy" */ "@/components/Team/main.vue"),
      },
      {
        name: "Dashboard",
        path: "/dashboard",
        component: () => import(/* webpackChunkName: "lazy" */ "@/components/Dashboard/main.vue")
      },
      {
        name: "Home",
        path: "",
        component: () => import(/* webpackChunkName: "lazy" */ "@/components/Home/main.vue")
      },
      {
        name: "Redirect",
        path: "*",
        redirect: { name: "Landing" }
      }
    ]
  }
];