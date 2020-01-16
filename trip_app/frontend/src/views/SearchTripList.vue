<template>
  <div class="suggest-trip">
    <div class="container mt-2">
      <h3>On this page you should be able to list of trips</h3>
      <trip-card v-for="(trip, item) in trips" :key="item" :data="trip"></trip-card>
      <div class="my-4">
        <p v-show="loadingTrips">...loading...</p>
        <button v-show="next" @click="getTrips" class="btn btn-sm btn-outline-success">Load More</button>
      </div>
    </div>
  </div>
</template>

<script>
import TripCard from "@/components/TripCard.vue";
import { apiService } from "@/common/api.service.js";

export default {
  name: "SearchTripList",
  components: {
    TripCard
  },
  props: {
    trips: {
      type: [Object, Array],
      required: false,
      default: () => []
    },
    next: {
      type: String,
      default: "",
      required: false
    },
    previous: {
      type: String,
      default: "",
      required: false
    }
  },
  data() {
    return {
      loadingTrips: false
    };
  },
  methods: {
    async getTrips() {
      console.log(this.next);
      if (this.next) {
        this.loadingTrips = true;
        let resp = await apiService(this.next);
        if (resp.valid) {
          let body = resp.body;
          this.trips.push(...body.results);
          this.loadingTrips = false;
          if (body.next) {
            this.next = body.next;
          } else {
            this.next = null;
          }
        }
      }
    }
  },

  async beforeRouteEnter(to, from, next) {
    console.log(to);
    console.log(from);
    console.log(next);
    if (from.name === "search-trip-form") {
      return next();
    }
    let endpoint = `/api/trips/?addr1=${to.query.addr1}&addr2=${to.query.addr2}&time1=${to.query.time1}&time2=${to.query.time2}`;
    let resp = await apiService(endpoint);
    if (resp.valid) {
      return next(
        vm => (
          (vm.trips = resp.body.results),
          (vm.next = resp.body.next),
          (vm.previous = resp.body.previous)
        )
      );
    }
  }
};
</script>
