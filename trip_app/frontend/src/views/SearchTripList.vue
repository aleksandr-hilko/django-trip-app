<template>
  <div class="suggest-trip">
    <div class="container mt-2">
      <h3>On this page you should be able to list of trips</h3>
      <p
        v-for="(trip, item) in trips"
        :key="item">{{ trip.driver }}</p>
    </div>
  </div>
</template>

<script>
    export default {
        name: "SearchTripList",
        props: {
            trips: {
                type: Array,
                required: true,

            }

        },
    };
</script>
