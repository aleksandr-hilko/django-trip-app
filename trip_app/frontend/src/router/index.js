import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import SearchTrip from "../views/SearchTrip.vue";
import SuggestTrip from "../views/SuggestTrip.vue";

Vue.use(VueRouter);

export default new VueRouter({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    {
      // with props: true, the slug parameter gets passed as a prop to the component
      path: "/search-trip/",
      name: "search-trip",
      component: SearchTrip
    },
    {
      // the ? sign makes the slug parameter optional
      path: "/suggest-trip/",
      name: "suggest-trip",
      component: SuggestTrip
    }
  ]
});
