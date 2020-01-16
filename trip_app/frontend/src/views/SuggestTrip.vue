<template>
  <div class="search-trip">
    <div class="container mb-2 w-50">
      <h4>Suggest your trip</h4>
      <div class="content">
        <b-form @submit="onSubmit">
          <div class="navigation">
            <p class="form-header">Start and destination places</p>
            <b-form-group>
              <vue-bootstrap-typeahead
                v-model="form.start_point"
                :data="addr_from"
                placeholder="From"
                @hit="form.start_point = $event"
              />
              <small v-if="errors.start_point" class="text-danger">{{ errors.start_point }}</small>
            </b-form-group>
            <b-form-group>
              <vue-bootstrap-typeahead
                v-model="form.dest_point"
                :data="addr_to"
                placeholder="To"
                @hit="form.dest_point = $event"
              />
              <small v-if="errors.dest_point" class="text-danger">{{ errors.dest_point }}</small>
            </b-form-group>
          </div>

          <b-form-group>
            <form-date-time
              @selectedDate="form.datetime = $event"
              :error="this.errors.datetime"
              :header="'Date and Time'"
            ></form-date-time>
          </b-form-group>

          <div class="otherDetails">
            <b-form-group>
              <label for="price" class="form-header">Price</label>
              <b-form-input id="price" :type="'number'" v-model="form.price"></b-form-input>
              <small v-if="errors.price" class="text-danger">{{ this.errors.price }}</small>
            </b-form-group>

            <b-form-group>
              <label for="num-passengers" class="form-header">Number of passengers</label>
              <b-form-input id="num-passengers" :type="'number'" v-model="form.num_seats"></b-form-input>
              <small v-if="errors.num_seats" class="text-danger">{{ errors.num_seats }}</small>
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

        <Map :marker_to="this.selected_to" :marker_from="this.selected_from"></Map>
      </div>
      <small v-if="errors.geocode" class="text-danger">{{ errors.geocode }}</small>
    </div>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import VueBootstrapTypeahead from "@/components/VueBootstrapTypeahead.vue";
import FormDateTime from "@/components/DateTime.vue";
import Map from "@/components/Map.vue";
import dateformat from "dateformat";

import _ from "underscore";
import {
  BForm,
  BFormGroup,
  BFormInput,
  BFormCheckbox,
  BFormTextarea
} from "bootstrap-vue";

export default {
  name: "SuggestTripForm",

  components: {
    BFormInput,
    BForm,
    BFormGroup,
    BFormCheckbox,
    BFormTextarea,
    VueBootstrapTypeahead,
    FormDateTime,
    Map
  },

  data() {
    return {
      addr_coord_from: {},
      addr_coord_to: {},
      addr_from: [],
      addr_to: [],
      form: {
        datetime: "",
        start_point: "",
        dest_point: "",
        price: "",
        num_seats: "",
        man_approve: true,
        description: ""
      },
      errors: {
        datetime: "",
        start_point: "",
        dest_point: "",
        price: "",
        num_seats: "",
        geocode: ""
      }
    };
  },
  computed: {
    selected_to: function() {
      return this.addr_coord_to[this.form.dest_point];
    },
    selected_from: function() {
      return this.addr_coord_from[this.form.start_point];
    }
  },
  watch: {
    "form.start_point": _.debounce(function(addr) {
      this.setAddressesFrom(addr);
    }, 500),
    "form.dest_point": _.debounce(function(addr) {
      this.setAddressesTo(addr);
    }, 500)
  },
  methods: {
    _getTripDataFromForm() {
      return {
        dep_time: `${dateformat(
          this.form.datetime,
          "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"
        )}`,
        start_point: {
          address: this.form.start_point
        },
        dest_point: {
          address: this.form.dest_point
        },
        price: this.form.price,
        man_approve: this.form.man_approve,
        num_seats: this.form.num_seats,
        description: this.form.description
      };
    },
    _isFormFieldEmpty() {
      let isEmpty = false;
      let required_fields = [
        "datetime",
        "start_point",
        "dest_point",
        "price",
        "num_seats"
      ];
      for (var i = 0; i < required_fields.length; i++) {
        let field = required_fields[i];
        if (!this.form[field]) {
          isEmpty = true;
          this.errors[field] = `Please fill this field `;
        } else {
          this.errors[field] = "";
        }
      }
      return isEmpty;
    },
    _isValidTime() {
      let isValid = true;
      let cur_date = new Date();
      if (cur_date > this.form.datetime) {
        isValid = false;
        this.errors.datetime = "Time have passed. Please change it. ";
      } else {
        this.errors.datetime = "";
      }
      return isValid;
    },
    isValidForm() {
      console.log("form is empty", this._isFormFieldEmpty());
      console.log("time is valid", this._isValidTime());
      return !this._isFormFieldEmpty() && this._isValidTime();
    },
    _showServerFormFieldsErrors(serverErrors) {
      for (let err in serverErrors) {
        if (err in this.errors) {
          let error_text = "";
          try {
            error_text = serverErrors[err]["non_field_errors"][0];
          } catch (error) {
            error_text = serverErrors[err][0];
          }
          this.errors[err] = error_text;
        }
      }
    },
    _hideFormErrors() {
      for (let error in this.errors) {
        this.errors[error] = "";
      }
    },

    async onSubmit(evt) {
      evt.preventDefault();
      let isValid = await this.isValidForm();
      if (isValid) {
        console.log("valid form");
        this._hideFormErrors();
        let trip_data = this._getTripDataFromForm();
        let endpoint = `/api/trips/`;
        let resp = await apiService(endpoint, "POST", trip_data);

        if (resp.valid) {
          await this.$router.push({
            name: "trip",
            params: { id: resp.body.id.toString() }
          });
        } else if (resp.status === 400) {
          let errors = resp.body;
          this._showServerFormFieldsErrors(errors);
          console.log(errors);
        } else if (resp.status === 500) {
          console.log("here");
          this.errors.geocode =
            "We are sorry. Geocode servise is not available. Please try resubmit form.";
        } else {
          console.log(resp);
        }
      }
    },

    async setAddressesFrom(query) {
      let endpoint = `/api/geocode/?query=${query}`;
      let resp = await apiService(endpoint);
      if (resp.valid) {
        this.addr_coord_from = resp.body;
        this.addr_from = Object.keys(resp.body);
      } else {
        console.log(resp);
      }
    },
    async setAddressesTo(query) {
      let endpoint = `/api/geocode/?query=${query}`;
      let resp = await apiService(endpoint);
      if (resp.valid) {
        this.addr_coord_to = resp.body;
        this.addr_to = Object.keys(resp.body);
      } else {
        console.log(resp);
      }
    }
  }
};
</script>

<style>
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

h4 {
  float: left;
  margin: 20px 5px 10px 5px;
}

div.content {
  display: flex;
  width: 100%;
}
</style>
