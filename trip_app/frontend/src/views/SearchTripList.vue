<template>
  <div class="suggest-trip">
    <div v-if="count !== 0" class="container mt-2">
      <h5 class="trips-count">{{count}} trips were found per your request </h5>
      <div class="trip-list">
        <trip-card v-for="(trip, item) in trips" :key="item" :data="trip"></trip-card>
        <div class="my-4">
          <p v-show="loadingTrips">...loading...</p>
          <button v-show="next" @click="getTrips" class="btn btn-sm btn-outline-success">Load More</button>
        </div>
      </div>
    </div>
    <h5 class="no-trips" v-else>We are sorry. No trips were found per your request.</h5>
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
    count: {
      type: String,
      default: "",
      required: false
    },
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
    if (from.name === "search-trip-form") {
      return next();
    }
    let endpoint = `/api/trips/?addr1=${to.query.addr1}&addr2=${to.query.addr2}&time1=${to.query.time1}&time2=${to.query.time2}`;
    let resp = await apiService(endpoint);
    if (resp.valid) {
      return next(
        vm => (
          (vm.count = resp.body.count),
          (vm.trips = resp.body.results),
          (vm.next = resp.body.next),
          (vm.previous = resp.body.previous)
        )
      );
    }
  }
};
</script>

<style>
h5.no-trips {
  margin-top: 20px;
}
.trips-count {
  margin: 20px 0px 20px 0px;
}
</style>
