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
    <city-header v-if="city" :city="city" />
    <v-col
      cols="12"
      lg="6"
      xl="4"
      style="
        height: calc(100vh - 142px);
        margin: 80px 0px 62px 0px;
      "
      v-bind:style="{
        padding: $vuetify.breakpoint.smAndDown ? '0 10px' : '0 30px',
      }"
    >
      <tabs-list
        v-on:tab="
          (v) => {
            tab = v;
          }
        "
      />
      <tabs-pages v-if="city" :tab="tab" :city="city" />
    </v-col>
    <v-col
      v-if="$vuetify.breakpoint.lgAndUp"
      cols="6"
      xl="8"
      style="padding: 0; margin: 0;"
    >
      <city-map
        v-if="city && timedMap"
        :city="city"
        :center="[city.longitude, city.latitude]"
        :zoom="city.zoom"
      />
    </v-col>
  </div>
</template>

<script>
import CityHeader from './header.vue';
import TabsList from './tabs.vue';
import TabsPages from './pages.vue';
import CityMap from './map/main.vue';

export default {
  components: {
    CityHeader,
    TabsList,
    TabsPages,
    CityMap,
  },
  data() {
    return {
      tab: 0,
      city: null,
      timedMap: false,
    };
  },
  metaInfo() {
    return {
      title: `Data911 - ${this.city.city}, ${this.city.state}`,
      htmlAttrs: {
        lang: 'en',
      },
    };
  },
  created() {
    this.load();
  },
  methods: {
    load() {
      this.$http.get('/city/' + this.$route.params.id).then((response) => {
        this.city = response.data;
        setTimeout(() => {
          this.timedMap = true;
        }, 200);
      });
    },
  },
};
</script>
