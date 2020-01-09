<template>
  <div class="suggest-trip">
    <div class="container mt-2">
      <h3>On this page you should be able to list of trips</h3>
      <trip-card
        v-for="(trip, item) in trips"
        :key="item"
        :data="trip"></trip-card>
    </div>
  </div>
</template>

<script>
    import TripCard from '@/components/TripCard.vue'

    export default {
        name: "SearchTripList",
        components: {
            TripCard
  },
        props: {
            trips: {
                type: Array,
                required: true,
            }
        },
    };
</script>
