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
  data() {
    return {
      trips: null,
      next: null,
      previous: null,
      loadingTrips: false
    };
  },
  methods: {
    getTrips() {
      console.log(this.next);
      if (this.next) {
        this.loadingTrips = true;
        apiService(this.next).then(data => {
          this.trips.push(...data.results);
          this.loadingTrips = false;
          if (data.next) {
            this.next = data.next;
          } else {
            this.next = null;
          }
        });
      }
    }
  },

  beforeRouteEnter(to, from, next) {
    let endpoint = `/api/trips/?addr1=${to.query.addr1}&addr2=${to.query.addr2}&time1=${to.query.time1}&time2=${to.query.time2}`;
    let trips = apiService(endpoint);
    apiService(endpoint).then(trips => {
      return next(
        vm => (
          (vm.trips = trips.results),
          (vm.next = trips.next),
          (vm.previous = trips.previous)
        )
      );
    });
  }
};
</script>
