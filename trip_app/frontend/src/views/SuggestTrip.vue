<template>
  <div class="search-trip">
    <div class="container mb-2 w-25">
      <b-form @submit="onSubmit">
        <div class="navigation">
          <p class="form-header">Start and destination places of your trip</p>
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
        </div>
        <div>
          <p class="form-header">Date and time</p>
          <b-form-row>
            <b-form-group class="form-group">
              <datepicker
                :bootstrap-styling="true"
                placeholder="Departure date"
                input-class="bg-light"
                :disabled-dates="disabledDates"
                @selected="form.date = $event"
              />
              <small v-if="errors.date" class="text-danger">{{ errors.date }}</small>
            </b-form-group>
            <b-form-group class="form-group col-md-6">
              <b-form-input :id="type-time" v-model="form.time" :type="'time'" placeholder="Time" />
              <small v-if="errors.time" class="text-danger">{{ errors.time }}</small>
            </b-form-group>
          </b-form-row>
        </div>
        <div class="otherDetails">
          <b-form-group>
            <label :for="price" class="form-header">Price</label>
            <b-form-input :id="price" :type="'number'" v-model="form.price"></b-form-input>
            <small v-if="errors.to" class="text-danger">{{ errors.price }}</small>
          </b-form-group>

          <b-form-group>
            <label :for="num-passengers" class="form-header">Number of passengers</label>
            <b-form-input :id="num-passengers" :type="'number'" v-model="form.num_seats"></b-form-input>
            <small v-if="errors.to" class="text-danger">{{ errors.num_seats }}</small>
          </b-form-group>

          <b-form-group>
            <b-form-checkbox
              id="checkbox"
              v-model="form.man_approve"
              name="checkbox"
              value="true"
              unchecked-value="false"
            >I want manually approve passengers to this trip</b-form-checkbox>
          </b-form-group>

          <b-form-group>
            <b-form-textarea
              id="textarea"
              v-model="form.description"
              placeholder="Enter some specific notes about your trip here"
              rows="3"
              max-rows="6"
            ></b-form-textarea>
          </b-form-group>
        </div>
        <br />
        <button type="submit" class="btn btn-primary">Submit</button>
      </b-form>
    </div>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import VueBootstrapTypeahead from "@/components/VueBootstrapTypeahead.vue";
import Datepicker from "vuejs-datepicker";
import _ from "underscore";
import {
  BForm,
  BFormGroup,
  BFormInput,
  BFormRow,
  BFormCheckbox,
  BFormTextarea
} from "bootstrap-vue";
import dateformat from "dateformat";

export default {
  name: "SuggestTripForm",

  components: {
    Datepicker,
    BFormInput,
    BForm,
    BFormGroup,
    BFormRow,
    BFormCheckbox,
    BFormTextarea,
    VueBootstrapTypeahead
  },

  data() {
    return {
      addresses_from: [],
      addresses_to: [],
      disabledDates: {
        customPredictor: function(date) {
          // compare dates without time part
          let currentDate = new Date().setHours(0, 0, 0, 0);
          if (date.setHours(0, 0, 0, 0) < currentDate) {
            return true;
          }
        }
      },
      form: {
        time: "",
        date: "",
        from: "",
        to: "",
        price: "",
        num_seats: "",
        man_approve: true,
        description: ""
      },
      errors: {
        time: "",
        date: "",
        from: "",
        to: "",
        price: "",
        num_seats: ""
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
    _formDateTime(dateKey, timeKey) {
      let formDate = this.form[dateKey];
      let formTime = this.form[timeKey];
      let [hours, minutes] = [0, 0];
      if (formTime) {
        [hours, minutes] = formTime.split(":");
      } else {
        var today = new Date();
        today.setMinutes(today.getMinutes() + 30);
        [hours, minutes] = [today.getHours(), today.getMinutes()];
      }
      let form_date = new Date(formDate);
      return new Date(form_date.setHours(hours, minutes));
    },
    _getTripDataFromForm() {
      return {
        dep_time: `${dateformat(
          this._formDateTime("date", "time"),
          "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"
        )}`,
        start_point: {
          address: this.form.from
        },
        dest_point: {
          address: this.form.to
        },
        price: this.form.price,
        man_approve: this.form.man_approve,
        num_seats: this.form.num_seats,
        description: this.form.description
      };
    },
    _isFormFieldEmpty() {
      let isEmpty = false;
      for (let field in this.form) {
        console.log(field)
        // allow time only fields to be empty
        if (!this.form[field] && field !== "time") {
          isEmpty = true;
          this.errors[field] = `Please fill this field `;
        } else {
          this.errors[field] = "";
        }
      }
      return isEmpty;
    },
    _isValidTime(dateKey, timeKey) {
      let isValid = true;
      let cur_date = new Date();
      if (cur_date > this._formDateTime(dateKey, timeKey)) {
        isValid = false;
        this.errors[timeKey] = "Time have passed. Please change it. ";
      } else {
        this.errors[timeKey] = "";
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
        this._isValidTime("date", "time") &&
        this._isGeoCoded("from") &&
        this._isGeoCoded("to")
      );
    },

    async onSubmit(evt) {
      evt.preventDefault();
      let isValid = await this.isValidForm();
      if (isValid) {
        let trip_data = this._getTripDataFromForm();
        console.log(trip_data);
        let endpoint = `/api/trips/`;
        apiService(endpoint, "POST", trip_data).then(data => {
          if (data.id) {
            this.$router.push({
              name: "trip",
              params: { id: data.id }
            });
          } else {
            console.log(data);
          }
        });
      }
    },

    async setAddressesFrom(query) {
      let endpoint = `/api/geocode/?query=${query}`;
      apiService(endpoint).then(data => {
        this.addresses_from = data;
      });
    },
    async setAddressesTo(query) {
      let endpoint = `/api/geocode/?query=${query}`;
      apiService(endpoint).then(data => {
        this.addresses_to = data;
      });
    }
  }
};
</script>

<style>
form {
  margin-top: 40px;
}
.form-header {
  margin: 10px 10px 5px 10px;
  text-align: left;
  display: block;
  font-weight: bold;
}

.custom-checkbox > label {
  margin-top: 20px;
  margin-bottom: 20px;
  text-align: left;
  font-weight: bold;
  float: left;
}
</style>
