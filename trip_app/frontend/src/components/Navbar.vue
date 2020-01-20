<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light my-navbar">
    <div class="container">
      <router-link :to="{ name: 'home' }" class="navbar-brand">Trip Time</router-link>

      <div class="collapse navbar-collapse right-panel">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item mx-1">
            <router-link
              :to="{ name: 'search-trip-form' }"
              class="btn btn-sm btn-outline-success"
            >Find</router-link>
          </li>
          <li class="nav-item mx-1">
            <router-link
              :to="{ name: 'suggest-trip' }"
              class="btn btn-sm btn-outline-success"
            >Suggest Trip</router-link>
          </li>

          <b-nav-item-dropdown id="profile-dropdown" :text="requestUser" class="md-2">
            <b-dropdown-item>Your Trips</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item href="/accounts/logout/">Log out</b-dropdown-item>
          </b-nav-item-dropdown>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import {
  BDropdownItem,
  BNavItemDropdown,
  BDropdownDivider
} from "bootstrap-vue";
export default {
  name: "NavbarComponent",
  components: {
    BDropdownItem,
    BNavItemDropdown,
    BDropdownDivider
  },
  props: {
    requestUser: {
      type: String,
      default: "",
      required: true
    }
  }
};
</script>

<style>
.my-navbar {
  border-bottom: 1px solid #ddd;
}

.navbar-brand {
  font-weight: bold;
  font-size: 130%;
}

.navbar-brand:hover {
  color: #dc3545 !important;
}

#profile-dropdown {
  margin-left: 30px;
}
</style>
