<template>
  <div class="search-trip">
    <div class="container mb-2 w-25">
      <b-form @submit="onSubmit">
        <h3 class="form-header">Where do you want to go ?</h3>
        <b-form-group>
          <vue-bootstrap-typeahead
            v-model="form.from"
            :data="addresses_from"
            placeholder="From"
            @hit="form.from = $event"
          />
          <small v-if="errors.from" class="text-danger">{{ errors.from }}</small>
        </b-form-group>
        <b-form-group>
          <vue-bootstrap-typeahead
            v-model="form.to"
            :data="addresses_to"
            placeholder="To"
            @hit="form.to = $event"
          />
          <small v-if="errors.to" class="text-danger">{{ errors.to }}</small>
        </b-form-group>
        <h3 class="form-header">When do you want to go ?</h3>

        <form-date-time
          @selectedDate="form.datetime1 = $event"
          :error="this.errors.datetime1"
          :header="'The earliest apt date'"
        ></form-date-time>
        <form-date-time
          @selectedDate="form.datetime2 = $event"
          :error="this.errors.datetime2"
          :header="'The latest apt date'"
        ></form-date-time>

        <br />
        <button type="submit" class="btn btn-primary">Find</button>
      </b-form>
    </div>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import VueBootstrapTypeahead from "@/components/VueBootstrapTypeahead.vue";
import FormDateTime from "@/components/DateTime.vue";
import _ from "underscore";
import { BForm, BFormGroup } from "bootstrap-vue";
import dateformat from "dateformat";

export default {
  name: "SearchTripForm",

  components: {
    BForm,
    BFormGroup,
    VueBootstrapTypeahead,
    FormDateTime
  },

  data() {
    return {
      addresses_from: [],
      addresses_to: [],
      form: {
        datetime1: "",
        datetime2: "",
        from: "",
        to: ""
      },
      errors: {
        datetime1: "",
        datetime2: "",
        from: "",
        to: ""
      }
    };
  },
  watch: {
    "form.from": _.debounce(function(addr) {
      this.setAddressesFrom(addr);
    }, 500),
    "form.to": _.debounce(function(addr) {
      this.setAddressesTo(addr);
    }, 500)
  },
  methods: {
    _isFormFieldEmpty() {
      let isEmpty = false;
      for (let field in this.form) {
        // allow time only fields to be empty
        if (!this.form[field]) {
          isEmpty = true;
          this.errors[field] = `Please fill this field `;
        } else {
          this.errors[field] = "";
        }
      }
      return isEmpty;
    },
    _isValidTime(datetime) {
      let isValid = true;
      let cur_date = new Date();
      if (cur_date > this.form[datetime]) {
        isValid = false;
        this.errors[datetime] = "Time have passed. Please change it. ";
      } else {
        this.errors[datetime] = "";
      }
      return isValid;
    },

    _isGeoCoded(key) {
      let isGeoCoded = true;
      let query = this.form[key];
      let endpoint = `/api/geocode/?query=${query}`;
      let geoData = apiService(endpoint);
      isGeoCoded = true;
      if (geoData.length !== 0) {
        this.errors[key] = "";
      } else {
        if (!this.errors[key]) {
          this.errors[key] = "We can't detect this address";
        }
        isGeoCoded = false;
      }
      return isGeoCoded;
    },
    isValidForm() {
      return (
        !this._isFormFieldEmpty() &&
        this._isValidTime("datetime1") &&
        this._isValidTime("datetime2") &&
        this._isGeoCoded("from") &&
        this._isGeoCoded("to")
      );
    },

    async onSubmit(evt) {
      evt.preventDefault();
      let isValid = await this.isValidForm();
      if (isValid) {
        await this.$router.push({
          name: "search-list",
          query: {
            addr1: this.form.from,
            addr2: this.form.to,
            time1: `${dateformat(
              this.form.datetime1,
              "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"
            )}`,
            time2: `${dateformat(
              this.form.datetime2,
              "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"
            )}`
          }
        });
      }
    },

    async setAddressesFrom(query) {
      let endpoint = `/api/geocode/?query=${query}`;
      let resp = await apiService(endpoint);
      if (resp.valid) {
        this.addresses_from = Object.keys(resp.body);
      } else {
        console.log(resp);
      }
    },
    async setAddressesTo(query) {
      let endpoint = `/api/geocode/?query=${query}`;
      let resp = await apiService(endpoint);
      if (resp.valid) {
        this.addresses_to = Object.keys(resp.body);
      } else {
        console.log(resp);
      }
    }
  }
};
</script>

<style>
.form-header {
  margin: 40px;
  font-weight: bold;
}
</style>
