<template>
  <div class="container w-50">
    <div>
      <div class="navigationDetails">
        <p class="depTime">Departure time - {{trip.dep_time}}</p>
        <p>Start point - {{trip.start_point['properties']['address']}}</p>
        <p>Destination point - {{trip.dest_point['properties']['address']}}</p>
      </div>

      <hr />

      <p>Price - {{trip.price}}</p>
      <p>Driver - {{trip.driver}}</p>
      <p v-if="trip.description">{{trip.description}}</p>
      <p v-if="trip.man_approve">You can book this trip after driver approval</p>
      <p v-else>You can book this trip without driver approval</p>

      <hr />

      <p>{{trip.free_seats}} free seats in this car</p>

      <p v-if="isEmptyCar">Nobody has yet booked this trip 😢.</p>
      <div v-else>
        <p>People who have already booked this car:</p>
        <ul>
          <li
            v-for="(passenger, index)  in this.trip.passengers"
            :key="index"
            class="passengers"
          >{{passenger}}</li>
        </ul>
      </div>
    </div>
    <button
      v-if="!isDriver && !isPassenger && !userRequestedTrip && trip.free_seats>0"
      type="button"
      class="btn btn-outline-success btn-lg"
      v-on:click="reserveTrip"
    >Book Trip</button>
    <button
      v-if="!isDriver && isPassenger || userRequestedTrip"
      type="button"
      class="btn btn-outline-danger btn-lg"
      v-on:click="cancelTrip"
    >Cancel reservation</button>
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
      trip: {},
      requestUser: "",
      userRequestedTrip: false
    };
  },
  computed: {
    isEmptyCar: function() {
      return this.trip.passengers.length < 1;
    },
    isDriver: function() {
      return this.requestUser === this.trip.driver;
    },
    isPassenger: function() {
      return this.trip.passengers.includes(this.requestUser);
    }
  },
  methods: {
    setRequestUser() {
      this.requestUser = window.localStorage.getItem("username");
    },
    async setUserRequestedTrip() {
      let endpoint = `/api/trips/${this.id}/requests`;
      let resp = await apiService(endpoint);
      this.userRequestedTrip = false;
      if (resp.valid) {
        const requests = resp.body;
        for (var i = 0; i < requests.length; i++) {
          const request = requests[i];
          if (this.requestUser in request) {
            this.userRequestedTrip = true;
            break;
          }
        }
      }
    },
    showGratefulMessage() {
      console.log(
        "You was added to the passengers list. Thank you for your trust."
      );
    },
    async getTrip() {
      let endpoint = `/api/trips/${this.id}/`;
      let resp = await apiService(endpoint);
      if (resp.valid) {
        this.trip = resp.body;
      } else {
        console.log(resp);
      }
    },
    async reserveTrip() {
      let endpoint = `/api/trips/${this.id}/reserve/`;
      let resp = await apiService(endpoint, "POST");
      if (resp.valid) {
        if (resp.body.status == "Approved") {
          this.userRequestedTrip = true;
          this.trip.passengers.push(this.requestUser);
          this.showGratefulMessage();
        }
        if (resp.body.status == "Active") {
          this.userRequestedTrip = true;
        }
      } else {
        console.log(resp);
      }
    },
    async cancelTrip() {
      console.log("cancel");
    }
  },
  created() {
    this.getTrip();
    this.setRequestUser();
    this.setUserRequestedTrip();
  }
};
</script>

<style>
.navigationDetails {
  margin-top: 40px;
}
.depTime {
  margin-bottom: 20px;
}
hr {
  margin-bottom: 30px;
}
button {
  margin-top: 50px;
}
li.passengers {
  font-weight: bold;
  float: left;
}
</style>


