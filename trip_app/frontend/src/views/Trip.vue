<template>
  <div class="container">
    <p>{{trip.dep_time}}</p>
    <p>{{trip.start_point['properties']['address']}}</p>
    <p>{{trip.dest_point['properties']['address']}}</p>
    <p>{{trip.price}}</p>
    <p>{{trip.driver}}</p>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";

export default {
  name: "Trip",
  props: {
    id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      trip: {}
    };
  },
  methods: {
    getTrip() {
      let endpoint = `/api/trips/${this.id}/`;
      apiService(endpoint).then(data => {
        if (data) {
          this.trip = data;
        } else {
          this.trip = null;
        }
      });
    }
  },
  created() {
    this.getTrip();
  }
};
</script>


