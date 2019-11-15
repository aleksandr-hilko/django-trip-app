<template>
  <div
    style="position:relative"
    class="dropdown"
    v-bind:class="{ show: openSuggestion }"
  >
    <input
      class="form-control"
      type="text"
      v-model="selection"
      :placeholder="placeholder"
      @keydown.enter="enter"
      @keydown.down="down"
      @keydown.up="up"
      @input="change"
      v-on:input="$emit('fetch-data', selection)"
    />
    <div
      class="dropdown-menu"
      v-bind:class="{ show: openSuggestion }"
      style="width:100%"
      aria-labelledby="dropdownMenu2"
    >
      <button
        v-for="(suggestion, item) in matches"
        v-bind:key="item"
        v-bind:class="{ active: isActive(item) }"
        @click="suggestionClick(item)"
        class="dropdown-item"
        type="button"
      >
        {{ suggestion }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Autocomplete",
  data() {
    return {
      isHovered: false,
      show: false,
      current: 0
    };
  },
  props: {
    suggestions: {
      type: Array,
      required: true
    },
    selection: {
      type: String,
      required: true,
      twoWay: true
    },
    placeholder: String
  },
  computed: {
    matches() {
      return this.suggestions;
    },
    openSuggestion() {
      return (
        this.selection !== "" && this.matches.length != 0 && this.show === true
      );
    }
  },
  methods: {
    enter() {
      this.selection = this.matches[this.current];
      this.show = false;
    },
    up() {
      if (this.current > 0) this.current--;
    },
    down() {
      if (this.current < this.matches.length - 1) this.current++;
    },
    isActive(index) {
      return index === this.current;
    },
    change() {
      if (this.show == false) {
        this.show = true;
        this.current = 0;
      }
    },
    suggestionClick(index) {
      this.selection = this.matches[index];
      this.show = false;
    }
  }
};
</script>
