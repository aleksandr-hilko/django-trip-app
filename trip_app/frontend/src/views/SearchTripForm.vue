<template>
  <div class="search-trip">
    <h3 class="form-header">
      Where do you want to go ?
    </h3>
    <div class="container mb-2 w-25">
      <b-form @submit="onSubmit">
        <b-form-group>
          <vue-bootstrap-typeahead
            v-model="form.from"
            :data="addresses_from"
            placeholder="From"
            @hit="form.from = $event"
          />
          <small
            v-if="errors.from"
            class="text-danger"
          >
            {{ errors.from }}
          </small>
        </b-form-group>
        <b-form-group>
          <vue-bootstrap-typeahead
            v-model="form.to"
            :data="addresses_to"
            placeholder="To"
            @hit="form.to = $event"
          />
          <small
            v-if="errors.to"
            class="text-danger"
          >
            {{ errors.to }}
          </small>
        </b-form-group>
        <h3 class="form-header">
          When do you want to go ?
        </h3>
        <b-form-row>
          <b-form-group class="form-group">
            <datepicker
              :bootstrap-styling="true"
              placeholder="Date 1"
              input-class="bg-light"
              :disabled-dates="disabledDates"
              @selected="form.date1 = $event"
            />
            <small
              v-if="errors.date1"
              class="text-danger"
            >
              {{ errors.date1 }}
            </small>
          </b-form-group>
          <b-form-group class="form-group col-md-6">
            <b-form-input
              :id="'type-time'"
              v-model="form.time1"
              :type="'time'"
              placeholder="Time1"
            />
            <small
              v-if="errors.time1"
              class="text-danger"
            >
              {{ errors.time1 }}
            </small>
          </b-form-group>
        </b-form-row>
        <b-form-row>
          <b-form-group class="form-group">
            <datepicker
              :bootstrap-styling="true"
              placeholder="Date 2"
              input-class="bg-light"
              :disabled-dates="disabledDates"
              @selected="form.date2 = $event"
            />
            <small
              v-if="errors.date2"
              class="text-danger"
            >
              {{ errors.date2 }}
            </small>
          </b-form-group>
          <b-form-group class="form-group col-md-6">
            <b-form-input
              :id="'type-time'"
              v-model="form.time2"
              :type="'time'"
              placeholder="Time2"
            />
            <small
              v-if="errors.time2"
              class="text-danger"
            >
              {{ errors.time2 }}
            </small>
          </b-form-group>
        </b-form-row>
        <br>
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
    import {apiService} from "@/common/api.service.js";
    import VueBootstrapTypeahead from "@/components/VueBootstrapTypeahead.vue"
    import Datepicker from "vuejs-datepicker";
    import _ from "underscore";
    import {BForm, BFormGroup, BFormInput, BFormRow} from "bootstrap-vue";
    import dateformat from "dateformat";


    export default {
        name: "SearchTripForm",

        components: {
            Datepicker,
            BFormInput,
            BForm,
            BFormGroup,
            BFormRow,
            VueBootstrapTypeahead
        },

        data() {
            return {
                addresses_from: [],
                addresses_to: [],
                disabledDates: {
                    customPredictor: function (date) {
                        // compare dates without time part
                        let currentDate = new Date().setHours(0, 0, 0, 0);
                        if (date.setHours(0, 0, 0, 0) < currentDate) {
                            return true;
                        }
                    }
                },
                form: {
                    time1: "",
                    date1: "",
                    time2: "",
                    date2: "",
                    from: "",
                    to: ""
                },
                errors: {
                    time1: "",
                    date1: "",
                    time2: "",
                    date2: "",
                    from: "",
                    to: ""
                }
            };
        },
        watch: {
            'form.from': _.debounce(function (addr) {
                this.setAddressesFrom(addr);
            }, 500),
            'form.to': _.debounce(function (addr) {
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
                }
                else {
                    var today = new Date();
                    today.setMinutes(today.getMinutes() + 30);
                    [hours, minutes] = [today.getHours(), today.getMinutes()];
                }
                let form_date = new Date(formDate);
                return new Date(form_date.setHours(hours, minutes));
            },
            _isFormFieldEmpty() {
                let isEmpty = false;
                for (let field in this.form) {
                    // allow time only fields to be empty
                    if (!this.form[field] && field !== 'time1' && field !== 'time2') {
                        isEmpty = true;
                        this.errors[field] = `Please fill this field `;
                    } else {
                        this.errors[field] = ""
                    }
                }
                return isEmpty
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
                return isGeoCoded
            },
            isValidForm() {
                return !this._isFormFieldEmpty() && this._isValidTime('date1', 'time1') && this._isValidTime('date2', 'time2') && this._isGeoCoded("from") && this._isGeoCoded("to")
            },

            async onSubmit(evt) {
                evt.preventDefault();
                let isValid = await this.isValidForm();
                if (isValid) {
                    let endpoint = `/api/trips/?addr1=${this.form.from}&addr2=${this.form.to}&time1=${dateformat(this._formDateTime('date1', 'time1'), "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'")}&time2=${dateformat(this._formDateTime('date2', 'time2'), "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'")}`;
                    console.log(endpoint);
                    let trips = await apiService(endpoint);
                    await this.$router.push({
                        name: 'search-list',
                        query: {
                            addr1: this.form.from,
                            addr2: this.form.from,
                            time1: this.form.from,
                            time2: this.form.from,
                        },
                        params: {trips: trips.results}
                    })
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
    .form-header {
        margin: 40px;
        font-weight: bold;
    }
</style>
