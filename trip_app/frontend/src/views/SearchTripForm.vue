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
                <br>
                <b-form-row>
                    <b-form-group class="form-group">
                        <datepicker
                                :bootstrap-styling="true"
                                placeholder="Date"
                                input-class="bg-light"
                                :disabled-dates="disabledDates"
                                @selected="form.date = $event"
                        />
                        <small
                                v-if="errors.date"
                                class="text-danger"
                        >
                            {{ errors.date }}
                        </small>
                    </b-form-group>
                    <b-form-group class="form-group col-md-6">
                        <b-form-input
                                :id="'type-time'"
                                v-model="form.time"
                                :type="'time'"
                                placeholder="Time"
                        />
                        <small
                                v-if="errors.time"
                                class="text-danger"
                        >
                            {{ errors.time }}
                        </small>
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
    import {apiService} from "@/common/api.service.js";
    import VueBootstrapTypeahead from "@/components/VueBootstrapTypeahead.vue"
    import Datepicker from "vuejs-datepicker";
    import _ from "underscore";
    import {BForm, BFormGroup, BFormInput, BFormRow} from "bootstrap-vue";


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
                    time: "",
                    date: "",
                    from: "",
                    to: ""
                },
                errors: {
                    time: "",
                    date: "",
                    from: "",
                    to: ""
                }
            };
        },
        computed: {
            formDateTime: function () {
                let [hours, minutes] = [0, 0];
                if (this.form.time) {
                    [hours, minutes] = this.form.time.split(":");
                }
                let form_date = new Date(this.form.date)
                return new Date(form_date.setHours(hours, minutes));
            }
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
            _isFormFieldEmpty() {
                let isEmpty = false;
                for (let field in this.form) {
                    if (!this.form[field]) {
                        isEmpty = true;
                        this.errors[field] = `Please fill the ${field} field `;
                    } else {
                        this.errors[field] = ""
                    }
                }
                return isEmpty
            },
            _isValidTime() {
                let isValid = true;
                let cur_date = new Date();
                if (cur_date > this.formDateTime) {
                    isValid = false;
                    this.errors.time = "Time have passed. Please change it. ";
                } else {
                    this.errors.time = "";
                }
                return isValid;
            },

            _isGeoCoded(key) {
                let isGeoCoded = true;
                let query = this.form[key];
                let endpoint = `/api/geocode/?query=${query}`;
                apiService(endpoint).then(data => {
                    if (data.length !== 0) {
                        this.errors[key] = ""
                    } else {
                        isGeoCoded = false;
                        if (!this.errors[key]) {
                            this.errors[key] = "We can't detect this address";
                        }
                    }
                    return isGeoCoded
                })
            },
            isValidForm() {
                return !this._isFormFieldEmpty() &
                    this._isValidTime() &
                    this._isGeoCoded("from") &
                    this._isGeoCoded("to");
            },

            onSubmit(evt) {
                evt.preventDefault();
                if (!this.isValidForm()) {
                    return
                } else {
                    let endpoint = `/api/trips/?addr1=${this.form.from}&addr2=${this.form.to}&time1=${this.formDateTime()}&time2=${this.formDateTime()}`;
                    console.log(endpoint);
                    apiService(endpoint)
                        .then(searchList => {
                            this.$router.push({
                                name: 'search-list',
                                query: {
                                    addr1: this.form.from,
                                    addr2: this.form.from,
                                    time1: this.form.from,
                                    time2: this.form.from,
                                },
                                params: {searchList: searchList}
                            })
                        })
                }
            },
            //   onSubmit() {
            //     // Tell the REST API to create or update a Question Instance
            //     if (!this.question_body) {
            //       this.error = "You can't send an empty question!";
            //     } else if (this.question_body.length > 240) {
            //       this.error = "Ensure this field has no more than 240 characters!";
            //     } else {
            //       let endpoint = "/api/questions/";
            //       let method = "POST";
            //       if (this.slug !== undefined) {
            //         endpoint += `${ this.slug }/`;
            //         method = "PUT";
            //       }
            //       apiService(endpoint, method, { content: this.question_body })
            //         .then(question_data => {
            //           this.$router.push({
            //             name: 'question',
            //             params: { slug: question_data.slug }
            //           })
            //         })
            //     }
            //   }
            // }

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
        margin: 50px;
        font-weight: bold;
    }
</style>
