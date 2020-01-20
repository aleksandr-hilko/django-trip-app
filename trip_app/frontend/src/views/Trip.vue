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

      <div class="passengers-list" v-else>
        <p>People who have already booked this car:</p>
        <ul>
          <li v-for="(passenger, index) in this.trip.passengers" :key="index">
            <div class="passenger">
              <div>{{passenger}}</div>
            </div>
          </li>
        </ul>
      </div>

      <div v-if="isDriver && activeRequests.length > 0" class="trip-requests">
        <p>Users who want to join to this trip:</p>
        <ul>
          <li v-for="request in activeRequests" :key="request.id" :id="request.id">
            <trip-request
              :request="request"
              @requestApproved="handleApprove($event)"
              @requestDeclined="handleDecline($event)"
            />
          </li>
        </ul>
      </div>

      <p
        v-if="!isDriver && hasActiveRequest"
      >You have requested this trip. Please wait for a driver approval...</p>
    </div>
    <button
      v-if="!isDriver && !hasApprovedRequest && !hasActiveRequest && trip.free_seats>0"
      type="button"
      class="btn btn-outline-success btn-lg"
      v-on:click="reserveTrip"
    >Book Trip</button>
    <button
      v-if="!isDriver && hasActiveRequest"
      type="button"
      class="btn btn-outline-danger btn-lg"
      v-on:click="cancelTrip"
    >Cancel Request</button>
    <button
      v-if="!isDriver && hasApprovedRequest"
      type="button"
      class="btn btn-outline-danger btn-lg"
      v-on:click="cancelTrip"
    >Leave Trip</button>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import TripRequest from "@/components/TripRequest.vue";

export default {
  name: "Trip",
  props: {
    id: {
      type: String,
      required: true
    }
  },
  components: {
    TripRequest
  },
  data() {
    return {
      trip: {},
      activeRequests: [],
      requestUser: "",
      userRequestedTrip: false,
      userRequests: [],
      activeRequestId: "",
      approvedRequestId: ""
    };
  },
  computed: {
    isEmptyCar: function() {
      return this.trip.passengers.length < 1;
    },
    isDriver: function() {
      return this.requestUser === this.trip.driver;
    },
    hasActiveRequest: function() {
      return this.activeRequestId !== "";
    },
    hasApprovedRequest: function() {
      return this.approvedRequestId !== "";
    }
  },
  methods: {
    setRequestUser() {
      this.requestUser = window.localStorage.getItem("username");
    },
    async getUserRequests() {
      let endpoint = `/api/trips/${this.id}/user_requests/`;
      let resp = await apiService(endpoint);
      if (resp.valid) {
        this.userRequests = resp.body;
        let activeRequest = this.userRequests.find(r => r.status === "Active");
        let approvedRequest = this.userRequests.find(
          r => r.status === "Approved"
        );
        this.activeRequestId = activeRequest ? activeRequest.id : "";
        this.approvedRequestId = approvedRequest ? approvedRequest.id : "";
      } else {
        console.log(resp);
      }
    },
    async getActiveTripRequests() {
      if (this.isDriver) {
        let endpoint = `/api/trips/${this.id}/requests/?status=1`;
        let resp = await apiService(endpoint);
        if (resp.valid) {
          this.activeRequests = resp.body;
        } else {
          console.log(resp);
        }
      } else {
        console.log("resp");
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
          this.approvedRequestId = resp.body.id;
          this.trip.passengers.push(this.requestUser);
          this.trip.free_seats--;
          this.showGratefulMessage();
        }
        if (resp.body.status == "Active") {
          this.activeRequestId = resp.body.id;
        }
      } else {
        console.log(resp);
      }
    },
    handleApprove(event) {
      this.activeRequests.splice(this.activeRequests.indexOf(event), 1);
      this.trip.passengers.push(event.user);
      this.trip.free_seats--;
    },
    handleDecline(event) {
      this.activeRequests.splice(this.activeRequests.indexOf(event), 1);
    },

    async cancelTrip() {
      let request_id = this.activeRequestId || this.approvedRequestId;
      let endpoint = `/api/trip-requests/${request_id}/cancel/`;
      let resp = await apiService(endpoint, "POST");
      if (resp.valid) {
        if (this.approvedRequestId) {
          this.trip.passengers.splice(
            this.trip.passengers.indexOf(this.requestUser),
            1
          );
          this.trip.free_seats++;
        }
        this.activeRequestId = "";
        this.approvedRequestId = "";
      } else {
        console.log(resp);
      }
    }
  },
  async created() {
    await this.getTrip();
    await this.setRequestUser();
    await this.getUserRequests();
    await this.getActiveTripRequests();
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
button.btn-lg {
  margin-top: 50px;
}
li {
  margin-top: 10px;
}
li > div.passenger {
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  width: 50%;
}

li > div.request {
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  width: 50%;
}
</style>