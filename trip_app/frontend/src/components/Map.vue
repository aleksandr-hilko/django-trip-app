<template>
  <div class="simple">
    <p>Trip details</p>
    <div id="top_div">
      <l-map
        :zoom="zoom"
        :center="center"
        @update:zoom="zoomUpdated"
        @update:center="centerUpdated"
        @update:bounds="boundsUpdated"
      >
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <l-marker
          v-for="marker in markers"
          :key="marker.id"
          :visible="marker.visible"
          :lat-lng="marker.position"
         
        ></l-marker>
        <l-polyline v-if="haveTwoPoints" :lat-lngs="polylinelatlngs" :color="polylineColor"></l-polyline>
      </l-map>
    </div>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker, LPolyline } from "vue2-leaflet";
import 'leaflet/dist/leaflet.css';
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.webpack.css';
import L from "leaflet";
import 'leaflet-defaulticon-compatibility';

// L.Icon.Default.imagePath = '';
// L.Icon.Default.mergeOptions({
//     iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
//     iconUrl: require('leaflet/dist/images/marker-icon.png'),
//     shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
// });

// delete L.Icon.Default.prototype._getIconUrl
// L.Icon.Default.imagePath = ''
// L.Icon.Default.mergeOptions({
//   iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
//   iconUrl: require('leaflet/dist/images/marker-icon.png'),
//   shadowUrl: require('leaflet/dist/images/marker-shadow.png')
// })


export default {
  name: "Map",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPolyline
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
      if (this.haveTwoPoints()) {
        return center;
      } else if (this.marker_to.length != 0 || this.marker_from.length != 0) {
        center = this.marker_to.length != 0 ? this.marker_to : this.marker_from;
      }
      return center;
    },
    markers: function() {
      return [
        {
          id: "m1",
          position: this.marker_from,
          visible: this.marker_from.length == 0 ? false : true,
        
        },
        {
          id: "m2",
          position: this.marker_to,
          visible: this.marker_to.length == 0 ? false : true,
         
        }
      ];
    },
    polylinelatlngs: function() {
      return [this.marker_from, this.marker_to];
    }
  },
  methods: {
    haveTwoPoints() {
      return this.marker_to.length != 0 && this.marker_from.length != 0;
    },
    zoomUpdated(zoom) {
      this.zoom = zoom;
    },
    centerUpdated(center) {
      this.center = center;
    },
    boundsUpdated(bounds) {
      this.bounds = bounds;
    }
  },
  data() {
    const myMarkerIcon = L.icon({
      iconUrl:
        "https://raw.githubusercontent.com/iconic/open-iconic/master/png/map-marker-8x.png",
      iconSize: [32, 32],
      iconAnchor: [16, 32]
    });
    return {
      zoom: 3,
      url: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      myMarkerIcon: myMarkerIcon,
      polylineColor: "green"
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
