<template>
  <transition mode="out-in">
    <router-view />
  </transition>
</template>

<script>
import Vue from "vue";
import PerfectScrollbar from "vue2-perfect-scrollbar";
import "vue2-perfect-scrollbar/dist/vue2-perfect-scrollbar.css";
Vue.use(PerfectScrollbar);

export default {
  name: "app",
  created: function() {
    this.$http.interceptors.response.use(response => {
      return response;
    });
  },
  mounted() {
    this.$store.dispatch("dashboard");
  }
};
</script>

<style>
@import "./styles/index.scss";
</style>
