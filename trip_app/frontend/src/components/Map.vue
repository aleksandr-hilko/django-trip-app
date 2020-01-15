<template>
  <div class="simple">
    <p>Trip details</p>
    <div id="top_div">
      <l-map :zoom="zoom" :center="center">
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <l-marker
          v-for="marker in markers"
          :key="marker.id"
          :visible="marker.visible"
          :lat-lng="marker.position"
          :icon="marker.icon"
        ></l-marker>
      </l-map>
    </div>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import L from "leaflet";

export default {
  name: "Map",
  components: {
    LMap,
    LTileLayer,
    LMarker
  },
  props: {
    marker_to: {
      type: [Object, Array],
      custom: true,
      default: () => []
    },
    marker_from: {
      type: [Object, Array],
      custom: true,
      default: () => []
    }
  },
  computed: {
    center: function() {
      let center = [53.914097, 27.602164];
      if (this.marker_from) {
        center = this.marker_from;
      }
      return center;
    },
    markers: function() {
      return [
        {
          id: "m1",
          position: this.marker_from,
          visible: this.marker_from.length == 0 ? false : true,
          icon: this.myMarkerIcon
        },
        {
          id: "m2",
          position: this.marker_to,
          visible: this.marker_to.length == 0 ? false : true,
          icon: this.myMarkerIcon
        }
      ];
    }
  },
  data() {
    const myMarkerIcon = L.icon({
      iconUrl: require("leaflet/dist/images/marker-icon.png"),
      shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
      iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png")
    });
    return {
      zoom: 3,
      url: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      myMarkerIcon: myMarkerIcon
    };
  }
};
</script>

<style>
@import "~leaflet/dist/leaflet.css";
div.simple {
  margin-left: 20px;
}
div#top_div {
  height: 50%;
}
div#top_div > div {
  height: 100%;
  width: 400px;
}
p {
  text-align: left;
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  font-weight: bold;
  margin-left: 5px;
}
</style>
