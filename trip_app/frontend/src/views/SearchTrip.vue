<template>
  <div class="search-trip">
    <h3 class="form-header">
      Where do you want to go ?
    </h3>
    <div class="container mb-2 w-25">
      <b-form @submit="onSubmit">
        <b-form-group>
          <autocomplete
            :suggestions="addresses_from"
            :selection.sync="form.value_from"
            :placeholder="'From'"
            @fetch-data="form.value_from = $event"
          />
        </b-form-group>
        <b-form-group>
          <autocomplete
            :suggestions="addresses_to"
            :selection.sync="form.value_to"
            :placeholder="'To'"
            @fetch-data="form.value_to = $event"
          />
        </b-form-group>
        <br>
        <b-form-row>
          <b-form-group class="form-group col-md-6">
            <datepicker
              :bootstrap-styling="true"
              placeholder="Date"
              input-class="bg-light"
              :disabled-dates="disabledDates"
              @selected="form.date = $event"
            />
          </b-form-group>
          <b-form-group class="form-group col-md-6">
            <b-form-input
              :id="'type-time'"
              v-model="form.time"
              :type="'time'"
              placeholder="Time"
            />
          </b-form-group>
        </b-form-row>

        <button
          type="submit"
          class="btn btn-primary"
        >
          Find
        </button>
      </b-form>
    </div>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import Autocomplete from "@/components/Autocomplete.vue";
import Datepicker from "vuejs-datepicker";
import _ from "underscore";
import { BForm, BFormGroup,BFormInput, BFormRow } from "bootstrap-vue";

export default {
  name: "SearchTrip",

  components: {
    Autocomplete,
    Datepicker,
    BFormInput,
    BForm,
    BFormGroup,
    BFormRow
  },

  data() {
    return {
      addresses_from: [],
      addresses_to: [],
      disabledDates: {
        customPredictor: function(date) {
          let currentDate = new Date();
          if (date < currentDate) {
            return true;
          }
        }
      },
      form: {
        time: "",
        date: "",
        value_from: "",
        value_to: ""
      }
    };
  },
  watch: {
    'form.value_from': _.debounce(function(addr) {
      this.getAddressesFrom(addr);
    }, 500),
    'form.value_to': _.debounce(function(addr) {
      this.getAddressesTo(addr);
    }, 500)
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      alert(JSON.stringify(this.form));
    },

    async getAddressesFrom(query) {
      let endpoint = "/api/geocode/?query=" + query;
      apiService(endpoint).then(data => {
        this.addresses_from = data;
      });
    },
    async getAddressesTo(query) {
      let endpoint = "/api/geocode/?query=" + query;
      apiService(endpoint).then(data => {
        this.addresses_to = data;
      });
    }
  }
};
</script>

<style>
.form-header {
  margin: 50px;
  font-weight: bold;
  font-family: Helvetica, sans-serif;
}
</style>
