<template>
  <div class="request">
    <div class="request-user">{{request.user}}</div>
    <div class="buttons">
      <button type="button" v-on:click="approveRequest" class="btn btn-outline-success">approve</button>
      <button type="button" v-on:click="declineRequest" class="btn btn-outline-danger">decline</button>
    </div>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";

export default {
  name: "TripRequest",
  props: {
    request: {
      type: Object,
      required: true,
      default: () => {}
    }
  },
  methods: {
    async approveRequest() {
      let endpoint = `/api/trip-requests/${this.request.id}/approve/`;
      let resp = await apiService(endpoint, "POST");
      if (resp.valid) {
        if (resp.body.status == "Approved") {
          this.$emit("requestApproved", this.request);
        }
      } else {
        console.log(resp);
      }
    },
    async declineRequest() {
      let endpoint = `/api/trip-requests/${this.request.id}/decline/`;
      let resp = await apiService(endpoint, "POST");
      if (resp.valid) {
        if (resp.body.status == "Declined") {
          this.$emit("requestDeclined", this.request);
        }
      } else {
        console.log(resp);
      }
    }
  }
};
</script>

<style>
li > div.request {
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  width: 50%;
}
.buttons button {
  margin-left: 10px;
}
</style>