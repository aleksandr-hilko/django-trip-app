<template>
  <div>
    <p class="form-header">{{ header }}</p>
    <div class="datetime">
      <datepicker
        :bootstrap-styling="true"
        input-class="bg-light"
        :disabled-dates="disabledDates"
        placeholder="DD:MM:YYYY"
        @selected="handleHit($event)"
      />
      <select class="custom-select hours" @change="handleHit" v-model="hour">
        <option
          v-for="(item, index) in hours"
          :key="index"
          :value="index"
          @click="handleHit"
        >{{ item }}</option>
      </select>
      <select class="custom-select minutes" @change="handleHit" v-model="minute">
        <option
          v-for="(item, index) in minutes"
          :key="index"
          :value="index"
          @click="handleHit"
        >{{ item }}</option>
      </select>
    </div>
    <small v-if="error" class="text-danger">{{ error}}</small>
  </div>
</template>

<script>
import Datepicker from "vuejs-datepicker";

export default {
  name: "FormDateTime",

  components: {
    Datepicker
  },
  props: {
    error: {
      type: String,
      default: "",
      required: false
    },
    header: {
      type: String,
      default: "",
      required: false
    }
  },
  data() {
    return {
      date: "",
      time: "",
      disabledDates: {
        customPredictor: function(date) {
          // compare dates without time part
          let currentDate = new Date().setHours(0, 0, 0, 0);
          if (date.setHours(0, 0, 0, 0) < currentDate) {
            return true;
          }
        }
      },
      minutes: ["00", "10", "20", "30", "40", "50"],
      hours: [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24"
      ],
      minute: "",
      hour: ""
    };
  },
  methods: {
    handleHit(event) {
      if (event instanceof Date) {
        this.date = event;
      }
      let form_date = "";
      if (this.date && this.minute && this.hour) {
        form_date = new Date(this.date).setHours(this.hour, this.minute);
      }
      this.$emit("selectedDate", form_date);
    }
  }
};
</script>

<style>
div.datetime {
  display: flex;
}
.vdp-datepicker {
  flex: 2;
}
select {
  flex: 0.2;
}
</style>
