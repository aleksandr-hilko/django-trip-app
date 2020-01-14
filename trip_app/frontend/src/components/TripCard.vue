<template>
  <div class="card w-50">
    <div class="card-body" @click="openDistinctTrip">
      <p class="card-text">{{data.dep_time}}</p>
      <div class="direction">
        <p class="card-text">{{data.start_point['properties']['address']}}</p>
        <p class="card-text">{{data.dest_point['properties']['address']}}</p>
      </div>
      <p class="card-text">{{data.price}}</p>
    </div>
    <div class="card-footer">
      <p class="card-text">{{data.driver}}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "TripCard",
  props: {
    data: {}
  },
  methods: {
      openDistinctTrip() {  
        console.log(this.data)   
        this.$router.push({
              name: "trip",
              params: { id: this.data.id.toString() }
            })
      }
  }
};
</script>

<style>
.card {
  margin: 0 auto;
  font-weight: bold;
  margin-bottom: 20px;
}
.card-body {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}
.direction {
  margin-left: 20px;
  text-align: left;
  flex-grow: 2;
}
.card-footer {
  text-align: left;
}
</style>


