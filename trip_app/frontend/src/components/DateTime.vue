<template>
  <div class="datetime">
    <div>
      <p class="form-header">Date and time</p>
      <b-form-row>
        <b-form-group class="form-group">
          <datepicker
            :bootstrap-styling="true"
            placeholder="Departure date"
            input-class="bg-light"
            :disabled-dates="disabledDates"
            @selected="date = $event"
          />
          <small v-if="errors.date" class="text-danger">{{ errors.date }}</small>
        </b-form-group>
        <b-form-group class="form-group col-md-6">
          <b-form-input :id="type-time" v-model="time" :type="'time'" placeholder="Time" />
          <small v-if="errors.time" class="text-danger">{{ errors.time }}</small>
        </b-form-group>
      </b-form-row>
    </div>
  </div>
</template>

<script>
import Datepicker from "vuejs-datepicker";
import { BFormGroup, BFormInput, BFormRow } from "bootstrap-vue";
import dateformat from "dateformat";

export default {
  name: "DateTime",

  components: {
    Datepicker,
    BFormInput
  },
  disabledDates: {
    customPredictor: function(date) {
      // compare dates without time part
      let currentDate = new Date().setHours(0, 0, 0, 0);
      if (date.setHours(0, 0, 0, 0) < currentDate) {
        return true;
      }
    }
  },
  methods: {
    _formDateTime() {
      let formDate = this.form.date;
      let formTime = this.form.time;
      let [hours, minutes] = [0, 0];
      if (formTime) {
        [hours, minutes] = formTime.split(":");
      } else {
        var today = new Date();
        today.setMinutes(today.getMinutes() + 30);
        [hours, minutes] = [today.getHours(), today.getMinutes()];
      }
      let form_date = new Date(formDate);
      this.$emit('hit', new Date(form_date.setHours(hours, minutes)))
      return new Date(form_date.setHours(hours, minutes));
    }
  },
  data() {
    return {
      date: "",
      time: ""
    };
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
