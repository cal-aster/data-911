<template>
  <div
    style="
      padding: 0;
      margin: 0;
      width: 100%;
      height: 100%;
      display: flex;
    "
  >
    <city-header
      v-if="city"
      :city="city"
    />
    <v-col
      cols="12"
      lg="6"
      style="
        height: calc(100vh - 142px);
        margin: 80px 0px 62px 0px;
      "
      v-bind:style="{
        padding: $vuetify.breakpoint.smAndDown ? '0 10px' : '0 30px'
      }"
    >
      <city-tabs
        v-on:tab="(v) => { tab = v }"
      />
      <city-pages
        v-if="city"
        :tab="tab"
        :city="city"
      />
    </v-col>
    <v-col
      cols="6"
      style="padding: 0; margin: 0;"
      class="d-none d-md-block"
    >
      <city-map-main
        v-if="city && timedMap"
        :city="city"
        :center="[city.longitude, city.latitude]"
        :zoom="city.zoom"
      />
    </v-col>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        tab: 0,
        city: null,
        timedMap: false
      };
    },
    created() {
      this.load()
    },
    methods: {
      load() {
        this.$http
        .get("/city/" + this.$route.params.id)
        .then(response => {
          this.city = response.data
          setTimeout(() => {
            this.timedMap = true
          }, 200)
        })
      }
    }
  };
</script>