import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import SearchTripForm from "../views/SearchTripForm.vue";
import SuggestTrip from "../views/SuggestTrip.vue";
import Trip from "../views/Trip.vue";
import SearchTripList from "../views/SearchTripList.vue";

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
      path: "/search-trip/",
      name: "search-trip-form",
      component: SearchTripForm
    },
    {
      path: "/suggest-trip/",
      name: "suggest-trip",
      component: SuggestTrip
    },
    {
      path: "/search/",
      name: "search-list",
      component: SearchTripList,
      props: true
    },
    {
      path: "/trip/:id",
      name: "trip",
      component: Trip,
      props: true
    }
  ]
});
